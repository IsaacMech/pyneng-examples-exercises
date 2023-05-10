import textfsm
import glob
import yaml
from datetime import datetime, timedelta
from task_25_5a import DBHandler
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
        dt = datetime.now()
        for result in parse_command_output('sh_ip_dhcp_snooping.template', fileh.read()):
            dhcp_data.append(tuple(result + [switch, 1, dt.strftime("%Y-%m-%d %H:%M:%S")]))
switches_data = []
with open('switches.yml', 'r') as fileh:
    switches_data = list(yaml.safe_load(fileh)['switches'].items())

data_dict = { 'switches': switches_data, 'dhcp': dhcp_data }

db.update_data('dhcp', [('active', 0)])
db.add_data_dict(data_dict)

for row in db.get_data('dhcp', 'active', '0'):
    week_ago = dt - timedelta(days=7)
    row_date = datetime.strptime(row[-1], '%Y-%m-%d %H:%M:%S')
    if row_date < week_ago:
        db.remove_data('dhcp', [('mac', row[0]), ('interface', row[-4]), ('switch', row[-3])])
