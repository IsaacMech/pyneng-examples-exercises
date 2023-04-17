# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

def get_int_vlan_map(config_filename):
    try:
        fhand = open(config_filename, 'r')
    except:
        print(f'Не удалос прочитать файл {config_filename}')
        return None
    trunk = {}
    access = {}
    for line in fhand:
        line = line.split()
        if not len(line) or line[0] != 'interface':
            continue
        intf = line[1]
        for conf in fhand:
            if 'trunk allowed' in conf:
                trunk[intf] = [ int(vlan) for vlan in conf.split()[-1].split(',') ]
                break
            if 'access vlan' in conf:
                access[intf] = int(conf.split()[-1])
                break
            if '!' in conf:
                break
    fhand.close()

    return access, trunk

# print(get_int_vlan_map('config_sw1.txt'))
