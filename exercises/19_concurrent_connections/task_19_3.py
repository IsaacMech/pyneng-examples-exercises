# -*- coding: utf-8 -*-
"""
Задание 19.3

Создать функцию send_command_to_devices, которая отправляет разные
команды show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять
  какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом
команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh int desc
Interface                      Status         Protocol Description
Et0/0                          up             up
Et0/1                          up             up
Et0/2                          admin down     down
Et0/3                          admin down     down
Lo9                            up             up
Lo19                           up             up
R3#sh run | s ^router ospf
router ospf 1
 network 0.0.0.0 255.255.255.255 area 0


Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
"""
import yaml
from concurrent.futures import ThreadPoolExecutor
from task_19_2 import send_show_command

# Этот словарь нужен только для проверки работа кода, в нем можно менять IP-адреса
# тест берет адреса из файла devices.yaml
commands = {
    "10.0.100.100": "sh run | s ^router ospf",
    "10.0.100.101": "sh ip int br",
    "10.0.100.102": "sh int desc",
}

def send_command_to_devices(devices, commands_dict, filename, limit=3):
    results = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = []
        for host, command in commands_dict.items():
            for device in devices:
                if host == device['host']:
                    futures.append(executor.submit(send_show_command, device, command))
        for future in futures:
            result = future.result().split('\n')
            results.append(result[-1] + '\n'.join(result[:-1]) + '\n')
    with open(filename, 'w') as fileh:
        fileh.writelines(results)

if __name__ == '__main__':
    with open('devices.yaml', 'r') as fileh:
        devices = yaml.safe_load(fileh)
    send_command_to_devices(devices, commands, 'test.txt')
