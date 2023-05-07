import sys
from tabulate import tabulate
from task_25_2 import DBHandler

assert len(sys.argv) == 1 or len(sys.argv) == 3,'программа принимает на вход либо 2 аргумента, либо никаких аргументов'

if len(sys.argv) == 1:
    print('В таблице dhcp такие записи:')
    print(tabulate(DBHandler('dhcp_snooping.db').get_data('dhcp')))
else:
    print('Информация об устройствах с такими параметрами:', sys.argv[1],sys.argv[2])
    print(tabulate(DBHandler('dhcp_snooping.db').get_data('dhcp', sys.argv[1],sys.argv[2])))

