import sys
from tabulate import tabulate
from task_25_4 import DBHandler

assert len(sys.argv) == 1 or len(sys.argv) == 3,'программа принимает на вход либо 2 аргумента, либо никаких аргументов'

def dhcp_sort(data):
    active = []
    inactive = []
    for row in data:
        if row[-1]:
            active.append(row)
        else:
            inactive.append(row)
    return active, inactive

def print_result(active, inactive):
    if active:
        print('Активные записи:')
        print(tabulate(active))
    if inactive:
        print('Неактивные записи:')
        print(tabulate(inactive))

db = DBHandler('dhcp_snooping.db')
available = [ x[0] for x in db.get_data('pragma_table_info("dhcp")', sel_col='name')]

if len(sys.argv) == 1:
    print('В таблице dhcp такие записи:')
    print_result(*dhcp_sort(db.get_data('dhcp')))
elif sys.argv[1] in available:
    print('Информация об устройствах с такими параметрами:', sys.argv[1], sys.argv[2])
    print_result(*dhcp_sort(db.get_data('dhcp', sys.argv[1], sys.argv[2])))
else:
    print('Данный параметр не поддерживается.')
    print('Допустимые значения параметров:', ', '.join(available))

