from works import Work
from license_parser import Parser
from collections import defaultdict
import logging

default_parser = Parser("licenses_description.yml")


def group_by_work_type(works:list):
    work_index = defaultdict(list)
    for idx, w in enumerate(works):
        work_index[w.type].append(idx)
    return work_index['model'], work_index['data'], work_index['algorithm'], work_index['mix']



"""
        Use a work (model/data/algorithm) or list of works ([model, data, algorithm]).
NOTE:   You can input list of works, the first work will compute the target output to construct a new work,
        other works the new work are bundled as a combination, which will be released together.
        For example, model output (aka prediction), algorithm (like SGD), data (input samples) as the bundle, meanwhile
        the model, algorithm and data will be the subworks of the predction work.
        You can also use output_as to specify the output type and form (internal mimatching may exist and be ignore)
        
        The single work as input means only the resulting output will be released, it is the predtions in this case.
        The aux works will not be released with this work.
"""
def use(works, aux_works, output_as=None):
    if isinstance(works, Work):
        works = [works] # Convert to list
    midx, didx, aidx, midx = group_by_work_type(works)

    new_work_name = '_'.join(['use'] + [w.name for w in works]) # i.e., use_model1_data1

    # Case1: [data1, data2, ...] -> new data work, or [alg1, alg2, ...] -> new alg work
    if len(didx) == len(works) or len(aidx) == len(works):
        new_work_type = works[0].type 
        new_Work = Work



    

    # We automatically interpret the type of the output ??
    

    if isinstance(works, list):
        parser = works[0].parser
    else:
        parser = works.parser
        works = [works]
    
    return

def combine(works:list, license_name:str=None):
    if len(works) <= 1:
        logging.warning(f"Not enough works to combine")
        return None
    
    # Deal with the new work name
    new_work_name = '_'.join(['C'] + [w.name for w in works]) # i.e., C_model1_model2

    # Deal with the new work type
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

    # Deal with the new work form, compatibility: raw > binary > saas
    all_work_form = [w.form for w in works]
    for comp_form  in ['saas', 'binary', 'raw']: # This order is matter
        if comp_form in all_work_form:
            new_work_form = comp_form
            break

    # The license name will not be set here, remain 'TBD', call analysis
    new_work = Work(new_work_name, new_work_type, new_work_form)
    if license_name:
        new_work.assign_license(license_name)
    new_work.mixworks = [(w, 'combine') for w in works]
    logging.debug(f"Combine {','.join([w.name for w in works])}")

    return new_work


    #licenses = [work.analysis() for work in works]
    #default_parser.license_merge()
    #new_work_name = 'Combine_'.join([work.name for work in works])
    # Mix Type?

"""
parser_mode:
 'fine': The reuse method is subdivided into several smaller steps,
 'coarse': Consider reuse methods as a whole.
"""

"""
def naive_copy(work:Work, parser_mode='coarse'):
    report = work.reuse("copy")
    return report

def train(model:Work, data:Work, algorithm:Work, parser_mode='coarse'):
    # model: target training model, data: training data, algorithm: train algorithm (such as SGD)

    if parser_mode == 'fine':
        data_report = data.reuse("use")
        output_report = model.reuse("use", reports_dict={"in": data_report})
        alg_report = algorithm.reuse("use", reports_dict={"in": output_report})
        trained_model_report = model.reuse("modify", reports_dict={"in": alg_report})

    if parser_mode == 'coarse':
        data_report = data.reuse("use")
        alg_report = algorithm.reuse("use")
        trained_model_report = model.reuse("train")

    return data_report, alg_report, trained_model_report

def embed(model, data):
    pass
"""
