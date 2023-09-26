import logging, gc
from works import Work

from license_parser import Parser
from reuse_methods import *

#logging.basicConfig(level=logging.DEBUG)

par = Parser("licenses_description.yml")

# 6 Corpus, 5 Image DS, 2 Music DS, 1 3D DS, 1 Video DS, 10 Models

wiki_text = Work('Wikipedia', 'data', 'raw', 'CC-BY-SA-4.0') # Corpus, https://en.wikipedia.org/wiki/Wikipedia:Copyrights
stack_exchange_text = Work('StackExchange', 'data', 'raw', 'CC-BY-SA-4.0') # Corpus, https://stackexchange.com/
free_law_text = Work('FreeLaw', 'data', 'raw', 'CC-BY-ND-4.0') # Corpus, https://free.law/
arxiv_text = Work('arXiv', 'data', 'raw', 'CC-BY-NC-SA-4.0') # Corpus, https://info.arxiv.org/help/license/index.html
pubmed_text = Work('PubMed', 'data', 'raw', 'CC-BY-NC-ND-4.0') # Corpus, https://www.ncbi.nlm.nih.gov/pmc/tools/textmining/
deep_sequoia_text = Work('Deep-sequoia', 'data', 'raw', 'LGPL-LR') # Corpus, http://deep-sequoia.inria.fr/

midjourney_img = Work('Midjourney_gen', 'data', 'raw', 'CC-BY-NC-4.0') # Image, https://docs.midjourney.com/docs/terms-of-service
flickr_img = Work('Flickr', 'data', 'raw', 'CC-BY-NC-SA-4.0') # Image, https://www.flickr.com/creativecommons/
stocksnap_img = Work('StockSnap', 'data', 'raw', 'CC0-1.0') # Image, https://stocksnap.io/license
wikimedia_img = Work('Wikimedia', 'data', 'raw', 'CC-BY-SA-4.0') # Image, https://commons.wikimedia.org/wiki/Main_Page
open_clipart_img = Work('OpenClipart', 'data', 'raw', 'CC0-1.0') # Image, https://openclipart.org/share

ccmixter_music = Work('ccMixter', 'data', 'raw', 'CC-BY-NC-4.0') # Music, https://ccmixter.org/terms 
jamendo_music = Work('Jamendo', 'data', 'raw', 'CC-BY-NC-ND-4.0') # Music, https://www.jamendo.com/legal/creative-commons

thingverse_3d = Work('Thingverse', 'data', 'raw', 'CC-BY-NC-SA-4.0') # 3D Model, https://www.thingiverse.com/thing:4850246
vimeo_video = Work('Vimeo', 'data', 'raw', 'CC-BY-NC-ND-4.0') # Video, https://vimeo.com/creativecommons

baize_model = Work('Baize', 'model', 'raw', 'GPL-3.0') # Chatbot, https://github.com/project-baize/baize-chatbot
stable_diffusion_mode = Work('StableDiffusion', 'model', 'raw', 'CreativeML-OpenRAIL-M') # Text2Image, https://huggingface.co/runwayml/stable-diffusion-v1-5
whisper_model = Work('Whisper', 'model', 'raw', 'MIT') # Voice2Text, https://github.com/openai/whisper
maskformer_model = Work('MaskFormer', 'model', 'raw', 'CC-BY-NC-4.0') # Image Segmentation, https://github.com/facebookresearch/MaskFormer/tree/da3e60d85fdeedcb31476b5edd7d328826ce56cc
detr_model = Work('DETR', 'model', 'raw', 'Apache-2.0') #Image Segmentation https://github.com/facebookresearch/detr
xclip_model = Work('X-Clip', 'model', 'raw', 'MIT') # Video2Text, https://huggingface.co/microsoft/xclip-base-patch32
i2vgen_model = Work('I2VGen-XL', 'model', 'raw', 'CC-BY-NC-ND-4.0') # Image2Video, https://huggingface.co/damo-vilab/MS-Image2Video
bigtranslate_model = Work('BigTranslate', 'model', 'raw', 'GPL-3.0') # Text Translation, https://huggingface.co/James-WYang/BigTranslate
bert_model = Work('BERT', 'model', 'raw', 'Apache-2.0') # Text, https://huggingface.co/bert-base-uncased
bloom_model = Work('BLOOM', 'model', 'raw', 'BigScience-BLOOM-RAIL-1.0') # Text Generation, https://huggingface.co/bigscience/bloom
llama2_model = Work('Llama2', 'model', 'raw', 'Llama2') # Text Generation, https://huggingface.co/meta-llama/Llama-2-7b

# Register License for above works
works = [ob for ob in gc.get_objects() if isinstance(ob, Work)]
par.register_license(works)

# CASE1: Combination of corpus
# Translate the corpus in 'dsl1' by 'translator' (model or algorithm) then combinated the tranlated corpus with 'dsl2'
def case1(dsl1, translator, dsl2):
    translated = [embed(ds, translator) for ds in dsl1]
    reused = combine(translated + dsl2)
    par.analysis(reused, open_policy='sell')
    reused.summary()
    return reused 

# CASE2: MoE of Models
# MoE of models in 'model_list' and fine-tuned 'model' with 'data'
def case2(model_list, data, model):
    tuned = finetune(model, data)
    reused = combine(model_list + [tuned])
    #reused.form = 'saas'
    par.analysis(reused, open_policy='share')
    reused.summary()
    return reused

# CASE3: Generation Pipeline
# Pipeline of several generation models
def case3(model_list, data, release_with_models=False):
    gen_data = data # Init Generation data as input data
    for model in model_list:
        gen_data = generate(model, gen_data)
    if release_with_models:
        reused = combine(model_list+[gen_data])
    else:
        reused = gen_data
    par.analysis(reused, open_policy='sell')
    reused.summary()
    return reused

# CASE4: Transfer learning and Weights Averaging
# Amalgamate of models like FedAvg
def case4(distill_from, distill_data, distill_to, model_list):
    distilled = distill(distill_from, distill_to, distill_data)
    reused = amalgamate([distilled] + model_list)
    par.analysis(reused, open_policy='sell')
    reused.summary()
    return reused

# CASE5: Hybrid reuse and data remix
# Remix works in remix1, then remix the pipeline output and remix2, collect these remixed results then share
def case5(remix1, pipelined, remix2):
    mixed1 = amalgamate(remix1)
    mixed2 = amalgamate(remix2 + [pipelined])
    reused = combine([mixed1, mixed2])
    par.analysis(reused, open_policy='share')
    reused.summary()
    print(mixed2.license_name)
    return reused


#case1([arxiv_text, stack_exchange_text], bigtranslate_model, [deep_sequoia_text, free_law_text])
#case1([deep_sequoia_text, pubmed_text], bigtranslate_model, [bigtranslate_model])
#case2([baize_model, bloom_model], wiki_text, bert_model) # NLP task
#case2([detr_model, i2vgen_model], flickr_img, maskformer_model) # Input=Image
#case3([whisper_model, baize_model, stable_diffusion_mode, i2vgen_model], jamendo_music, False) # Music->Text->Image->Video
#case4(i2vgen_model, wikimedia_img, xclip_model, [maskformer_model, whisper_model]) # Multimodal models
case4(bloom_model, wiki_text, bert_model, [llama2_model, bigtranslate_model]) # NLP models
#case5([stocksnap_img, midjourney_img], case3([whisper_model, baize_model, stable_diffusion_mode, i2vgen_model], ccmixter_music, False), [vimeo_video])
#thingverse_3d

"""
par.register_license([work1, work2, work3, work4])

new_work = combine([work1, work2, work4])
result = par.analysis(new_work, open_policy='sell')
if result:
    new_work.summary()
else:
    print('Error :(')
"""
#new_work = amalgamate([work1, work2])
#new_work = train([work1, work4])
#new_work2 = amalgamate([new_work, work2])
#new_work3 = combine([new_work2, work3, work4])
#print(work4.license.meta['terms'])
#par.analysis(new_work3, open_policy='sell')
#new_work3.summary()
