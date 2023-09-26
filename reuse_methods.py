from works import Work
from license_parser import Parser
from collections import defaultdict
import logging
from copy import deepcopy

""" <reuse_methods.py>
    This file contains the definitions of reuse methods. 
    Note that, all of these methods are not released with the new work by default.
    Therefore, the new (work, usage) tuple will be added to new_work's auxworks rather than subworks.
    Except that some of the reuse methods inevitably incorporates the original works (e.g. amalgamate).
    For combination, original works will be added to mixworks.
    You can manually combine these works for future license analysis based on preset open policy, or analyze them one by one.
"""


default_parser = Parser("licenses_description.yml")
"""
        Use a work (model/data/algorithm) or list of works ([model, data, algorithm]).
NOTE:   You can input list of works, the first work will compute the target output to construct a new work,
        other works the new work are bundled as a combination, which will be released together.
        For example, model output (aka prediction), algorithm (like SGD), data (input samples) as the bundle, meanwhile
        the model, algorithm and data will be the auxworks of the predction work.
        You can also use output_as to specify the output type and form (internal mimatching may exist and be ignore)
        
        The single work as input means only the resulting output will be released, it is the predtions in this case.
        The aux works will not be released with this work.
"""
def use(works, aux_works=None, output_as:Work=None, license_name:str=None) -> Work:
    if isinstance(works, Work):
        works = [works] # Convert to list
    if isinstance(aux_works, Work):
        aux_works = [aux_works]

    if output_as is None:
        output_as = Work('dummy', 'data', 'raw') # Default output as raw data
    new_work = new_reused_work(works, 'U', license_name, output_as)

    for w in works:
        new_work.subworks += reuse_method_spread(w, 'use') # 'use' of this work relied on the 'use' of all mixworks
    if aux_works:
        for aw in aux_works:
            new_work.auxworks += reuse_method_spread(aw, 'use')

    logging.debug(f"Use {','.join([w.name for w in works])} with auxworks {','.join([aw.name for aw in aux_works])}")
    
    return new_work

# Copy a work, this copy method will be applied to all mixworks, but the subworks will be skipped.
def naive_copy(work:Work, license_name:str=None) -> Work:
    new_work = new_reused_work([work], 'CP', license_name)
    # All mixworks will be copied, we can consider the new work as a new combination, subworks will NOT be copied
    new_work.mixworks = reuse_method_spread(work, 'copy')
    
    logging.debug(f"Copy {work.name}")
    #else:
    #    new_work.assign_license(work.license_name) # Retain the license of original work
    return new_work

"""
    Combine multiple works to constrct a new work
"""
def combine(works:list, license_name:str=None) -> Work:
    if len(works) <= 1:
        logging.warning(f"Not enough works to combine")
        return None

    # The license name will not be set here, remain 'TBD', call analysis
    new_work = new_reused_work(works, 'C', license_name)

    for w in works:
        if new_work.type == 'mix':
            new_work.mixworks.append((w, 'combine_mix')) # use 'combine_mix' if the resulting work is a combination with mix types, this distinction is useful for copyleft data licenses.
        else:
            new_work.mixworks.append((w, 'combine')) # Recursive mixworks are not be included
    logging.debug(f"Combine {','.join([w.name for w in works])}")

    return new_work

def amalgamate(works:list, license_name:str=None) -> Work:
    if len(works) <= 1:
        logging.warning(f"Not enough works to amalgamate")
        return None
    if all(w.type == works[0].type for w in works):
        if all(w.form == 'raw' for w in works):
            new_work = new_reused_work(works, 'A', license_name)
            # The modified works are regarded as 'subworks' of the new work (will be share with this work)
            new_work.subworks = [(w, 'modify') for w in works] #TODO: How about work type = mix? How about spread to mixworks?
            return new_work
        else:
            logging.error("The amalgamation of works only support raw form")
    else:
        logging.error("Different types of works used for amalgamation")
    return None

# Distill knowledge from old models to new models
def distill(works, dest_work:Work=None, aux_works=None, license_name:str=None):
    if isinstance(works, Work):
        works = [works] # Convert to list
    if isinstance(aux_works, Work):
        aux_works = [aux_works]

    if dest_work: # The target model for distillation
        if dest_work.type != 'model':
            logging.error("The type of destination work of distillation must be a model")
            return
        else:
            new_work = deepcopy(dest_work) # The distilled knowledge directly transfered to the destination model
            new_work.name = get_new_work_name(works+[dest_work], 'D') # Rename the dest_work, for example, D_work1_work2
            new_work.subworks += reuse_method_spread(dest_work, 'train') # Add the dest_work to the subworks of new work
            new_work.license_name = 'TBD' # Reset the license name of new work
    else:
        if all(w.type != 'model' for w in works):
            logging.error("At least one of the works used for distillation needs to be 'model' type")
            return
        else:
            dummy_model_works = Work('dummy', 'model', 'raw') # We suppose the new work is a raw form model if the dest_model is not provided
            new_work = new_reused_work(works, 'D', license_name, dummy_model_works) 
    
    for w in works:
        new_work.auxworks += reuse_method_spread(w, 'distill') # NOTE: Accumulation '+=' must be placed here because there may be another auxworks in dest_works
    if aux_works:
        for aw in aux_works:
            new_work.auxworks += reuse_method_spread(aw, 'distill')
    return new_work

'''
    Similar with use(), the difference is all input works are considered released with result in use(), but
    in generate(), all input works will not be released with result. If you just want to get the inference result of a model, please call generate() rather than use().
    NOTE: Most licenses have no restrictions on the output of models or algorithms.
'''
def generate(works, aux_works=None, output_as:Work=None, license_name:str=None) -> Work:
    if isinstance(works, Work):
        works = [works] # Convert to list
    if isinstance(aux_works, Work):
        aux_works = [aux_works]

    if output_as is None:
        output_as = Work('dummy', 'data', 'raw') # Default output as raw data
    new_work = new_reused_work(works, 'G', license_name, output_as)

    for w in works:
        new_work.auxworks += reuse_method_spread(w, 'generate') # 'generate' of this work relied on the 'use' of all mixworks
    if aux_works:
        for aw in aux_works:
            new_work.auxworks += reuse_method_spread(aw, 'generate')

    logging.debug(f"Generate {','.join([w.name for w in works])} with auxworks {','.join([aw.name for aw in aux_works])}")
    return new_work

# Embed works (corpus, image or other data samples) using aux_works (model or algorithm)
def embed(works, aux_works=None, output_as:Work=None, license_name:str=None) -> Work:
    if isinstance(works, Work):
        works = [works] # Convert to list
    if isinstance(aux_works, Work):
        aux_works = [aux_works]
    if output_as is None:
        output_as = Work('dummy', 'data', 'raw') # Default output as raw data
    new_work = new_reused_work(works, 'E', license_name, output_as)
    
    for w in works:
        new_work.subworks += reuse_method_spread(w, 'embed') # 'embed' of this work relied on the 'embed' of all mixworks
    if aux_works: # Model like feature extractor, translator
        for aw in aux_works:
            new_work.auxworks += reuse_method_spread(aw, 'use')
    return new_work

# NOTE: To prevent loop, destination model should not be in works.
# You can just leave dest_work=None to create a new work
def train(works, dest_work:Work=None, aux_works=None, license_name:str=None) -> Work:
    if isinstance(works, Work):
        works = [works] # Convert to list
    if isinstance(aux_works, Work):
        aux_works = [aux_works]
    if dest_work:
        if dest_work.type != 'model':
            logging.error("The type of destination work of train must be a model")
            return
        else:
            new_work = deepcopy(dest_work) # This training procedure is applied to the destination model
            new_work.name = get_new_work_name(works+[dest_work], 'T') # Rename the dest_work, for example, T_work1_work2
            new_work = deepcopy(dest_work) # The distilled knowledge directly transfered to the destination model
            new_work.subworks += reuse_method_spread(dest_work, 'modify') # Add the dest_work to the subworks of new work
            new_work.license_name = 'TBD' # Reset the license name of new work
    else:
        dummy_model_works = Work('dummy', 'model', 'raw') # We suppose the new work is a raw form model if the dest_model is not provided
        new_work = new_reused_work(works, 'T', license_name, dummy_model_works) 

    for w in works:
        if w.type == 'model':
            # The model in input will be regarded as the initial model and will be added as subworks of new work, NOTE: Accumulation '+=' must be placed here because there may be another subworks in dest_works
            new_work.subworks += reuse_method_spread(w, 'train')
        else:
            # The software and data in input will be regarded as auxworks of the new work and will not be released with the new work
            new_work.auxworks += reuse_method_spread(w, 'train')
    if aux_works:
        for aw in aux_works:
            new_work.auxworks += reuse_method_spread(aw, 'train')

    return new_work

# Finetune is a kind of train
def finetune(work, data, aux_works=None):
    aux_works = [data] + aux_works if aux_works else [data]
    return train(work, aux_works=aux_works)

def group_by_work_type(works:list):
    work_index = defaultdict(list)
    for idx, w in enumerate(works):
        work_index[w.type].append(idx)
    return work_index['model'], work_index['data'], work_index['algorithm'], work_index['mix']

def get_new_work_name(works:list, specifier:str) -> str:
    if specifier:
        return '_'.join([specifier] + [w.name for w in works]) # i.e., C_model1_model2
    return get_new_work_name(works, 'UNK') # i.e. UNK_model1_model2

# If all works have same work type, return this type, otherwise, return 'mix'
def get_new_work_type(works:list) -> str:
    all_work_type = []
    for w in works:
        if w.type == 'mix':
            for (work, type) in w.mixworks:
                all_work_type.append(type)
        else:
            all_work_type.append(w.type)
    all_work_type = list(set(all_work_type))
    
    if len(all_work_type) == 1:
        # Combination of works with same type will result new work in same type
        new_work_type = all_work_type[0]
    else:
        new_work_type = 'mix'
    return new_work_type

# Deal with the new work form, compatibility: raw > binary > saas
def get_new_work_form(works:list) -> str:
    all_work_form = [w.form for w in works]
    for comp_form  in ['saas', 'binary', 'raw']: # This order is matter
        if comp_form in all_work_form:
            new_work_form = comp_form
            break
    return new_work_form

# Create new work. NOTE: The license name will not be set here, remain 'TBD', call analysis to determine
# You can specify which licenses you want to grant to this work and the type, form of new work
def new_reused_work(works:list, specifier:str=None, assign_license_name:str=None, output_as:Work=None) -> Work:
    new_work_name = get_new_work_name(works, specifier)
    new_work_type = output_as.type if output_as else get_new_work_type(works)
    new_work_form = output_as.form if output_as else get_new_work_form(works)
    new_work = Work(new_work_name, new_work_type, new_work_form)
    if assign_license_name:
        new_work.assign_license(assign_license_name)
    return new_work

# Deal with the spread of reusing method of mixworks, this work or the mixworks of this work will be returned
def reuse_method_spread(work:Work, method:str) -> list:
    spreaded_works = []
    if work.is_include_mixworks():
        spreaded_works += [(mw, method) for mw in work.find_mixworks()] # Spread to all mixworks
    else:
        spreaded_works.append((work, method))
    return spreaded_works
