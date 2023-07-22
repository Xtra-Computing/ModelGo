import logging
from works import Work, EVENT

#model1 = Work("myModel", "model", "raw", "CreativeML-OpenRAIL-M")
#report2 = model1.reuse("use")

from license_parser import Parser
from reuse_methods import *

#logging.basicConfig(level=logging.DEBUG)

par = Parser("licenses_description.yml")
work1 = Work('my1', 'software', 'raw', 'Unlicense')
work2 = Work('my2', 'data', 'raw', 'Apache-2.0')
work3 = Work('my3', 'model', 'binary', 'CC-BY-SA-3.0')
par.register_license([work1, work2, work3])

new_work = combine([work1, work3])
new_work2 = combine([new_work, work2], 'CC-BY-SA-3.0')
par.analysis(new_work2, open_policy='sell')
#par.analysis(new_work)
new_work2.summary()
logging.debug(f"MAIN DEBUG ------- new1: {new_work.license_name}, new2: {new_work2.license_name}")



#print(par.licenses_dict["CreativeML-OpenRAIL-M"].meta["terms"])

"""
import yaml

with open("licenses_description.yml", "r") as file:
    yaml_data = yaml.safe_load(file) # list of dict

print(yaml_data[0])
print(type(yaml_data))
"""