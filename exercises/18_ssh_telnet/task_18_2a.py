# -*- coding: utf-8 -*-
"""
Задание 18.2a

Скопировать функцию send_config_commands из задания 18.2 и добавить параметр log,
который контролирует будет ли выводится на стандартный поток вывода информация о том
к какому устройству выполняется подключение.
По умолчанию, результат должен выводиться.

Пример работы функции:

In [13]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...

In [14]: result = send_config_commands(r1, commands, log=False)

In [15]:

Скрипт должен отправлять список команд commands на все устройства
из файла devices.yaml с помощью функции send_config_commands.
"""

import netmiko
import yaml

commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]

def send_config_commands(device, commands, log=True):
    if log:
        print(f'''Подключаюсь к {device['host']}...''')
    with netmiko.ConnectHandler(**device) as devcon:
        devcon.enable()
        return devcon.send_config_set(commands)

if __name__ == '__main__':
    with open('devices.yaml', 'r') as fileh:
        devices = yaml.safe_load(fileh)

    for device in devices:
        print(send_config_commands(device, commands))
