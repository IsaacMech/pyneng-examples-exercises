# -*- coding: utf-8 -*-

"""
Задание 23.2

Скопировать класс CiscoTelnet из задания 22.2 и добавить классу поддержку
работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_23_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка

Тест проверяет подключение с параметрами из файла devices.yaml. Там должны быть
указаны доступные устройства.
"""
from telnetlib import Telnet
from time import sleep

class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.connection = Telnet(ip)
        self._logpass(username, password)
        self._enable(secret)
    def __enter__(self):
        return self
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
    def send_show_command(self, line):
        self._write_line(line)
        return self.connection.read_until(b'#').decode()
    def __del__(self):
        self.connection.close()
    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()
