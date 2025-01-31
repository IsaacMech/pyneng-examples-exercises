# -*- coding: utf-8 -*-

"""
Задание 24.2a

Скопировать и дополнить класс MyNetmiko из задания 24.2.

Добавить метод _check_error_in_command, который выполняет проверку на такие ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Метод ожидает как аргумент команду и вывод команды.
Если в выводе не обнаружена ошибка, метод ничего не возвращает.
Если в выводе найдена ошибка, метод должен генерировать исключение ErrorInCommand
с сообщением о том какая ошибка была обнаружена, на каком устройстве и в какой команде.

Исключение ErrorInCommand создано в файле задания.

Переписать метод send_command netmiko, добавив в него проверку на ошибки.

In [2]: from task_24_2a import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br')
Out[4]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip br')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-1c60b31812fd> in <module>()
----> 1 r1.send_command('sh ip br')
...
ErrorInCommand: При выполнении команды "sh ip br" на устройстве 192.168.100.1 возникла ошибка "Invalid input detected at '^' marker."

"""


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """

import re
from netmiko.cisco.cisco_ios import CiscoIosSSH

device_params = {
    "device_type": "cisco_ios",
    "host": "10.0.100.100",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}

class MyNetmiko(CiscoIosSSH):
    _regex = re.compile(r'%\s+(.+)\n')
    def __init__(self, **device_params):
        super().__init__(**device_params)
        self.enable()
        self.ip = device_params['host']
    def _check_error_in_command(self, command, output):
        err = self._regex.search(output)
        if err:
            raise ErrorInCommand(f'При выполнении команды "{command}" на устройстве {self.ip} возникла ошибка "{err[1]}"')
    def send_command(self, command):
        result = super().send_command(command)
        self._check_error_in_command(command, result)
        return result

if __name__ == '__main__':
    print(MyNetmiko(**device_params).send_command('sh run | i hostname'))
