# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

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
    "host": "10.0.100.101",
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
    def send_config_set(self, command_list):
        result = ''
        if type(command_list) == type(''):
            command_list = [command_list]
        for command in command_list:
            response = super().send_config_set([command])
            print(response)
            self._check_error_in_command(command, response)
            result += response
        return result

if __name__ == '__main__':
    print(MyNetmiko(**device_params).send_config_set(["logging 0255.255.1"]))
