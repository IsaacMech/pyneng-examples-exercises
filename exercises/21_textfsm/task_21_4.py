# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""

import textfsm
import yaml
from netmiko import ConnectHandler
from pprint import pprint
from task_21_3 import parse_command_dynamic

def send_and_parse_show_command(device_dict, command, templates_path='templates', index='index'):
    with ConnectHandler(**device_dict) as dev:
        dev.enable()
        output = dev.send_command(command)
    attr_dict = { 'Vendor': device_dict['device_type'], 'Command': command }
    return parse_command_dynamic(output, attr_dict, index, templates_path)

# вызов функции должен выглядеть так
if __name__ == "__main__":
    with open('devices.yaml', 'r') as fileh:
        devices = yaml.safe_load(fileh)
    for device in devices:
        pprint(send_and_parse_show_command(device, 'sh ip int br'))
