import textfsm
import glob
import yaml
from task_25_3 import DBHandler
from pprint import pprint

try:
    db = DBHandler('dhcp_snooping.db')
except:
    print('База данных не существует. Перед добавлением данных, ее надо создать')
    exit()

dhcp_snoop = glob.glob("*_dhcp_snooping.txt")

def parse_command_output(template, command_output):
    with open(template, 'r') as fileh:
        fsm = textfsm.TextFSM(fileh)
        return fsm.ParseText(command_output)

dhcp_data = []
for file in dhcp_snoop:
    with open(file, 'r') as fileh:
        switch = file.split('_')[0]
        for result in parse_command_output('sh_ip_dhcp_snooping.template', fileh.read()):
            dhcp_data.append(tuple(result + [switch, 1]))
switches_data = []
with open('switches.yml', 'r') as fileh:
    switches_data = list(yaml.safe_load(fileh)['switches'].items())

data_dict = { 'switches': switches_data, 'dhcp': dhcp_data }

db.update_data('dhcp', [('active', 0)])
db.add_data_dict(data_dict)
