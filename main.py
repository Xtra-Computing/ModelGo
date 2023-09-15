import logging, gc
from works import Work

from license_parser import Parser
from reuse_methods import *

#logging.basicConfig(level=logging.DEBUG)

par = Parser("licenses_description.yml")

wiki_text = Work('Wikipedia', 'data', 'raw', 'CC-BY-SA-4.0') # Corpus, https://en.wikipedia.org/wiki/Wikipedia:Copyrights
stack_exchange_text = Work('StackExchange', 'data', 'raw', 'CC-BY-SA-4.0') # Corpus, https://stackexchange.com/
free_law_text = Work('FreeLaw', 'data', 'raw', 'CC-BY-ND-4.0') # Corpus, https://free.law/
arxiv_text = Work('arxiv', 'data', 'raw', 'CC-BY-NC-SA-4.0') # Corpus, https://info.arxiv.org/help/license/index.html
pubmed_text = Work('PubMed', 'data', 'raw', 'CC-BY-NC-ND-4.0') # Corpus, https://www.ncbi.nlm.nih.gov/pmc/tools/textmining/
deep_sequoia_text = Work('Deep-sequoia', 'data', 'raw', 'LGPL-LR') # Corpus, http://deep-sequoia.inria.fr/

midjourney_img = Work('Midjourney_gen', 'data', 'raw', 'CC-BY-NC-4.0') # Image, https://docs.midjourney.com/docs/terms-of-service
flickr_img = Work('Flickr', 'data', 'raw', 'CC-BY-NC-SA') # Image, https://www.flickr.com/creativecommons/
stocksnap_img = Work('StockSnap', 'data', 'raw', 'CC0-1.0') # Image, https://stocksnap.io/license
wikimedia_img = Work('Wikimedia', 'data', 'raw', 'CC-BY-SA-4.0') # Image, https://commons.wikimedia.org/wiki/Main_Page
open_clipart_img = Work('OpenClipart', 'data', 'raw', 'CC0-1.0') # Image, https://openclipart.org/share

ccmixter = Work('ccMixter', 'data', 'raw', 'CC-BY-NC-4.0') # Music, https://ccmixter.org/terms 
jamendo = Work('Jamendo', 'data', 'raw', 'CC-BY-NC-ND-4.0') # Music, https://www.jamendo.com/legal/creative-commons

thingverse = Work('Thingverse', 'data', 'raw', 'CC-BY-NC-SA-4.0') # 3D Model, https://www.thingiverse.com/thing:4850246
vimeo = Work('Vimeo', 'data', 'raw', 'CC-BY-NC-ND-4.0') # Video, https://vimeo.com/creativecommons

baize_model = Work('Baize', 'model', 'raw', 'GPL-3.0') # Chatbot, https://github.com/project-baize/baize-chatbot
stable_diffusion_mode = Work('StableDiffusion', 'model', 'raw', 'CreativeML-OpenRAIL-M') # Text2Image, https://huggingface.co/runwayml/stable-diffusion-v1-5
whisper_model = Work('Whisper', 'model', 'raw', 'MIT') # Voice2Text, https://github.com/openai/whisper
maskformer_model = Work('MaskFormer', 'model', 'raw', 'CC-BY-NC-4.0') # Image Segmentation, https://github.com/facebookresearch/MaskFormer/tree/da3e60d85fdeedcb31476b5edd7d328826ce56cc
xclip_model = Work('X-Clip', 'model', 'raw', 'MIT') # Video2Text, https://huggingface.co/microsoft/xclip-base-patch32
i2vgen_model = Work('I2VGen-XL', 'model', 'raw', 'CC-BY-NC-ND') # Image2Video, https://huggingface.co/damo-vilab/MS-Image2Video
bigtranslate_model = Work('BigTranslate', 'model', 'raw', 'GPL-3.0') # Text Translation, https://huggingface.co/James-WYang/BigTranslate
bert_model = Work('BERT', 'model', 'raw', 'Apache-2.0') # Text, https://huggingface.co/bert-base-uncased

# Register License for above works
works = [ob for ob in gc.get_objects() if isinstance(ob, Work)]
par.register_license(works)

# CASE1:
# Translate the corpus in 'dsl1' by 'translator' (model or algorithm) then combinated the tranlated corpus with 'dsl2'
def case1(dsl1, translator, dsl2):
    translated = [embed(ds, translator) for ds in dsl1]
    reused = combine(translated + dsl2)
    par.analysis(reused, open_policy='sell')
    reused.summary()
    
    return

case1([arxiv_text, stack_exchange_text], bigtranslate_model, [deep_sequoia_text])


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
