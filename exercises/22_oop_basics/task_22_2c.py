# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

"""
import yaml
import re
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
    _regex = re.compile(r'%\s+(.+)\r\n')
    def __init__(self, ip, username, password, secret):
        self.connection = Telnet(ip)
        self.ip = ip
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
    def send_config_commands(self, command_list, strict=True):
        if type(command_list) == type(''):
            command_list = [command_list]
        self._write_line('conf t')
        result = self.connection.read_until(b'#').decode()
        for command in command_list:
            try:
                self._write_line(command)
                temp = self.connection.read_until(b'#').decode()
                if '%' in temp:
                    raise Exception
                result += temp
            except Exception:
                err = self._regex.search(temp)[1]
                error_text = f'При выполнении команды "{command}" на устройстве {self.ip} возникла ошибка -> {err}'
                if strict:
                    raise ValueError(error_text)
                print(error_text)
                result += temp
                continue
        self._write_line('end')
        return result + self.connection.read_until(b'#').decode()
    def __del__(self):
        self.connection.close()
    def __exit__(self):
        self.__del__(self)

if __name__ == '__main__':
    with open('devices.yaml', 'r') as fileh:
        devices = yaml.safe_load(fileh)
    for device in devices:
        print(CiscoTelnet(**device).send_config_commands(['interface FastEthernet0/12', 'no showdown'], strict=False))
