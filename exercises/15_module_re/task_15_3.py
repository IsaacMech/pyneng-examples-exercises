# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""

import re

template = '''
object network LOCAL_{0}
 host {0}
 nat (inside,outside) static interface service {1} {2} {3}'''

def convert_ios_nat_to_asa(iosfile, asafile):
    regex = re.compile(r'ip nat \w+ source \w+ (?P<protocol>\w+) (?P<host_ip>(?:\d+\.){3}\d+) (?P<in_port>\d+) interface \S+ (?P<out_port>\d+)')
    with open(iosfile, 'r') as iosfhand, open(asafile, 'w') as asafhand:
        for rule in regex.finditer(iosfhand.read()):
            data = rule.groupdict()
            asafhand.write(template.format(data['host_ip'], data['protocol'], data['in_port'], data['out_port']))

convert_ios_nat_to_asa('cisco_nat_config.txt', 'test.txt')
