# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

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
        if 'Fa' not in intf:
            continue
        for conf in fhand:
            if 'trunk allowed' in conf:
                trunk[intf] = [ int(vlan) for vlan in conf.split()[-1].split(',') ]
                break
            if 'access vlan' in conf:
                access[intf] = int(conf.split()[-1])
                break
            if '!' in conf:
                access[intf] = 1
                break
    fhand.close()

    return access, trunk

# print(get_int_vlan_map('config_sw1.txt'))
