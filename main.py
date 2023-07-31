import logging
from works import Work

from license_parser import Parser
from reuse_methods import *

#logging.basicConfig(level=logging.DEBUG)

par = Parser("licenses_description.yml")
work1 = Work('my1', 'model', 'binary', 'AFL-3.0')
work2 = Work('my2', 'model', 'raw', 'CreativeML-OpenRAIL-M')
work3 = Work('my3', 'software', 'raw', 'Unlicense')
work4 = Work('my4', 'data', 'raw', 'CC-BY-SA-4.0')

par.register_license([work1, work2, work3, work4])

#new_work = amalgamate([work1, work2])
new_work = train([work1, work4])
new_work2 = amalgamate([new_work, work2])
new_work3 = combine([new_work2, work3, work4])
print(work4.license.meta['terms'])
par.analysis(new_work3, open_policy='sell')
new_work3.summary()
