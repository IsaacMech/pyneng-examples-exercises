# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через subprocess).
IP-адрес считается доступным, если выполнение команды ping отработало с кодом 0 (returncode).
Нюансы: на Windows returncode может быть равен 0 не только, когда ping был успешен,
но для задания нужно проверять именно код. Это сделано для упрощения тестов.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess as sp
import ipaddress as iplib

def ping_ip_addresses(ip_list):
    '''
    Принимаем на вход список ip адресов в виде списка строк, пингуем
    и возвращаем кортеж из двух списков - доступных и недоступных адресов.
    вход: список строк
    выход: кортеж с двумя списками строк
    '''
    online = []
    offline = []
    for ip in ip_list:
        try:
            valid_ip = str(iplib.IPv4Address(ip))
        except iplib.AddressValueError:
            offline.append(ip)
            continue
        ping_test = sp.run(['ping', '-n', '3', valid_ip], stdout=sp.DEVNULL)
        if ping_test.returncode:
            offline.append(valid_ip)
        else:
            online.append(valid_ip)
    return online, offline
'''
ip_list = [
    '192.168.0.1',
    '8.8.8.8',
    '320.40.50.1',
    '1.1.1.1'
]

print(ping_ip_addresses(ip_list))
'''
