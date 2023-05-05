# -*- coding: utf-8 -*-

"""
Задание 24.2d

Скопировать класс MyNetmiko из задания 24.2c или задания 24.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен
работать точно так же как метод send_config_set в netmiko.
Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_24_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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
    def send_command(self, command, **kwargs):
        result = super().send_command(command, **kwargs)
        self._check_error_in_command(command, result)
        return result
    def send_config_set(self, command_list, ignore_errors=True):
        result = ''
        if type(command_list) == type(''):
            command_list = [command_list]
        if not ignore_errors:
            for command in command_list:
                response = super().send_config_set([command])
                self._check_error_in_command(command, response)
                result += response
        else:
            result = super().send_config_set(command_list)
        return result

if __name__ == '__main__':
    print(MyNetmiko(**device_params).send_config_set("logging 0255.255.1"))
