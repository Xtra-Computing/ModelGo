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
        

if __name__ == '__main__':
    unittest.main()