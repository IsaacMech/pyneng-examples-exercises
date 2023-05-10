from task_25_6 import DBHandler
import textfsm
import yaml
from tabulate import tabulate
from datetime import datetime, timedelta

def dhcp_sort(data):
    active = []
    inactive = []
    for row in data:
        if row[-2]:
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

def parse_command_output(template, command_output):
    with open(template, 'r') as fileh:
        fsm = textfsm.TextFSM(fileh)
        return fsm.ParseText(command_output)

def create_db(filename, schema):
    assert type(filename) == str and type(schema) == str
    try:
        DBHandler(filename)
        print('Файл уже существует.')
    except:
        DBHandler(filename, create=True).create_schema(from_file=schema)

def add_data_switches(db_file, filename):
    db = DBHandler(db_file)
    switches_data = []
    for file in filename:
        with open(file, 'r') as fileh:
            switches_data += list(yaml.safe_load(fileh)['switches'].items())
    data_dict = { 'switches': switches_data }
    db.add_data_dict(data_dict)
    
def add_data(db_file, filename):
    if type(filename) == str:
        filename = [filename]
    db = DBHandler(db_file)
    dhcp_data = []
    for file in filename:
        with open(file, 'r') as fileh:
            switch = file.split('/')[-1].split('\\')[-1].split('_')[0]
            dt = datetime.now()
            for result in parse_command_output('sh_ip_dhcp_snooping.template', fileh.read()):
                dhcp_data.append(tuple(result + [switch, 1, dt.strftime("%Y-%m-%d %H:%M:%S")]))
    data_dict = { 'dhcp': dhcp_data }
    
    db.update_data('dhcp', [('active', 0)])
    db.add_data_dict(data_dict)
    
    for row in db.get_data('dhcp', 'active', '0'):
        week_ago = dt - timedelta(days=7)
        row_date = datetime.strptime(row[-1], '%Y-%m-%d %H:%M:%S')
        if row_date < week_ago:
            db.remove_data('dhcp', [('mac', row[0]), ('interface', row[-4]), ('switch', row[-3])])

def get_data(db_file, key, value):
    db = DBHandler(db_file)
    available = [ x[0] for x in db.get_data('pragma_table_info("dhcp")', sel_col='name')]
    if key in available:
        print_result(*dhcp_sort(db.get_data('dhcp', key, value)))
    else:
        print('Данный параметр не поддерживается.')
        print('Допустимые значения параметров:', ', '.join(available))

def get_all_data(db_file):
    db = DBHandler(db_file)
    print_result(*dhcp_sort(db.get_data('dhcp')))