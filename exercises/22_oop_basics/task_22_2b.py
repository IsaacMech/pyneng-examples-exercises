# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

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
    def send_config_commands(self, command_list):
        if type(command_list) == type(''):
            command_list = [command_list]
        self._write_line('conf t')
        result = self.connection.read_until(b'#')
        for command in command_list:
            self._write_line(command)
            result += self.connection.read_until(b'#')
        self._write_line('end')
        return (result + self.connection.read_until(b'#')).decode()
    def __del__(self):
        self.connection.close()
    def __exit__(self):
        self.__del__(self)

if __name__ == '__main__':
    with open('devices.yaml', 'r') as fileh:
        devices = yaml.safe_load(fileh)
    for device in devices:
        print(CiscoTelnet(**device).send_config_commands(['interface FastEthernet0/1', 'no shutdown']))
