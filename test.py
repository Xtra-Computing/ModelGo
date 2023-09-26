import unittest
from license_parser import Parser
from works import Work
from reuse_methods import *

class TestModelGO(unittest.TestCase):
    parser = Parser("licenses_description.yml")
    
    def setUp(self):
        pass

    def test_license_register(self):
        work1 = Work('mywork1', 'data', 'raw', 'CC-BY-SA-3.0')
        work2 = Work('mywork2', 'data', 'raw', 'cC-by-Sa-3.0') # Case insensitive
        self.parser.register_license(work1)
        self.parser.register_license(work2)
        self.assertEqual(work1.license.short_id, 'CC-BY-SA-3.0')
        self.assertEqual(work2.license.short_id, 'CC-BY-SA-3.0')

    def test_combine(self):
        work1 = Work('mydata', 'data', 'raw', 'CC-BY-SA-3.0')
        work2 = Work('myalg', 'software', 'saas', 'Apache-2.0')
        work3 = Work('mymodel', 'model', 'raw', 'Unlicense')
        work4 = Work('mymodel2', 'model', 'binary', 'CreativeML-OpenRAIL-M')
        self.parser.register_license([work1, work2, work3, work4])

        model1_model2 = combine([work3, work4])
        self.assertEqual(model1_model2.form, 'binary') # raw + binary -> binary
        self.assertEqual(model1_model2.type, 'model') # model + mdoel -> model

        data_alg = combine([work1, work2])
        self.assertEqual(data_alg.form, 'saas') # raw + saas -> saas
        self.assertEqual(data_alg.type, 'mix') # data + software -> mix
        
        #data_model2 = combine([work1, work4])
        #self.assertEqual(data_model2.form, 'binary') # raw + binary -> binary

class TestMLP(unittest.TestCase):
    parser = Parser("licenses_description.yml")

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

    
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()