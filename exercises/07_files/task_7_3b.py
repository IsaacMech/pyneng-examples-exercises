# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

filename = 'CAM_table.txt'

try:
    fhand = open(filename, 'r')
except:
    print(f'Не удалось открыть файл {filename}!')
    exit()

while True:
    try:
        vlan = int(input('Enter VLAN number: '))
        break
    except:
        print('VLAN должен быть числом!')

template = '{0:<9}{1:<20}{3}'
buffer = []

for line in fhand:
    line = line.split()
    if not len(line) or not line[0].isdigit():
        continue
    line[0] = int(line[0])
    buffer.append(line)

for record in buffer:
    if record[0] != vlan:
        continue
    print(template.format(*record))

fhand.close()
