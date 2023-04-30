# -*- coding: utf-8 -*-
"""
Задание 21.5

Создать функцию send_and_parse_command_parallel.

Функция send_and_parse_command_parallel должна запускать в
параллельных потоках функцию send_and_parse_show_command из задания 21.4.

Параметры функции send_and_parse_command_parallel:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* templates_path - путь к каталогу с шаблонами TextFSM
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать словарь:
* ключи - IP-адрес устройства с которого получен вывод
* значения - список словарей (вывод который возвращает функция send_and_parse_show_command)

Пример словаря:
{'192.168.100.1': [{'address': '192.168.100.1',
                    'intf': 'Ethernet0/0',
                    'protocol': 'up',
                    'status': 'up'},
                   {'address': '192.168.200.1',
                    'intf': 'Ethernet0/1',
                    'protocol': 'up',
                    'status': 'up'}],
 '192.168.100.2': [{'address': '192.168.100.2',
                    'intf': 'Ethernet0/0',
                    'protocol': 'up',
                    'status': 'up'},
                   {'address': '10.100.23.2',
                    'intf': 'Ethernet0/1',
                    'protocol': 'up',
                    'status': 'up'}]}

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""
import yaml
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
from task_21_4 import send_and_parse_show_command

def send_and_parse_command_parallel(devices, command, templates_path='templates', index='index'):
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {}
        for device in devices:
            futures[device['host']] = executor.submit(send_and_parse_show_command, device, command, templates_path, index)
        for future in futures:
            futures[future] = futures[future].result()
    return futures

# вызов функции должен выглядеть так
if __name__ == "__main__":
    with open('devices.yaml', 'r') as fileh:
        devices = yaml.safe_load(fileh)
    pprint(send_and_parse_command_parallel(devices, 'sh ip int br'))
