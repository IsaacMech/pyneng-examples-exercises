import sys
from tabulate import tabulate
from task_25_3 import DBHandler

assert len(sys.argv) == 1 or len(sys.argv) == 3,'программа принимает на вход либо 2 аргумента, либо никаких аргументов'

db = DBHandler('dhcp_snooping.db')
available = [ x[0] for x in db.get_data('pragma_table_info("dhcp")', sel_col='name')]

if len(sys.argv) == 1:
    print('В таблице dhcp такие записи:')
    print(tabulate(db.get_data('dhcp')))
#    print(tabulate(db.get_data('switches')))
elif sys.argv[1] in available:
    print('Информация об устройствах с такими параметрами:', sys.argv[1], sys.argv[2])
    print(tabulate(db.get_data('dhcp', sys.argv[1], sys.argv[2])))
else:
    print('Данный параметр не поддерживается.')
    print('Допустимые значения параметров:', ', '.join(available))

