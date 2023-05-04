# -*- coding: utf-8 -*-

"""
Задание 22.2a

Скопировать класс CiscoTelnet из задания 22.2 и изменить
метод send_show_command добавив три параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей,
  полученный после обработки с помощью TextFSM.
  При parse=True должен возвращаться список словарей, а parse=False обычный вывод.
  Значение по умолчанию - True.
* templates - путь к каталогу с шаблонами. Значение по умолчанию - "templates"
* index - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"


Пример создания экземпляра класса:

In [1]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_22_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command("sh ip int br", parse=True)
Out[4]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'}]

In [5]: r1.send_show_command("sh ip int br", parse=False)
Out[5]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status
Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up
up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up...'


"""
import yaml
from textfsm import clitable
from telnetlib import Telnet
from time import sleep

def parse_command_dynamic(command_output, attributes_dict, index_file='index', templ_path='templates'):
    clit = clitable.CliTable(index_file, templ_path)
    result = []
    clit.ParseCmd(command_output, attributes_dict)
    for row in clit:
        result.append(dict(zip(clit.header, row)))
    return result

class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.connection = Telnet(ip)
        self._logpass(username, password)
        self._enable(secret)
    def __enter__(self, ip, username, password, secret):
        self.__init__(ip, username, password, secret)
    def _logpass(self, username, password):
        self.connection.read_until(b'User')
        self._write_line(username)
        self.connection.read_until(b'Pass')
        self._write_line(password)
        self.connection.read_until(b'>')
    def _enable(self, secret):
        self._write_line('enable')
        self.connection.read_until(b'Pass')
        self._write_line(secret)
        self.connection.read_until(b'#')
    def _write_line(self, line):
        self.connection.write(line.encode('ascii') + b'\n')
    def send_show_command(self, line, parse=True, templates='templates', index='index'):
        self._write_line(line)
        result = self.connection.read_until(b'#').decode()
        if parse:
            result = parse_command_dynamic(result, { 'Vendor': 'cisco_ios', 'Command': line }, index, templates)
        return result
    def __del__(self):
        self.connection.close()
    def __exit__(self):
        self.__del__(self)

if __name__ == '__main__':
    with open('devices.yaml', 'r') as fileh:
        devices = yaml.safe_load(fileh)
    for device in devices:
        print(CiscoTelnet(**device).send_show_command('sh ip int br'))
