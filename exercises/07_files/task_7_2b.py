# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]

import sys

if len(sys.argv) < 3:
    print('Недостаточно аргументов!')
    exit()

try:
    fhand = open(sys.argv[1], 'r')
except:
    print(f'Не удалось открыть файл {sys.argv[1]}!')
    exit()

try:
    fout = open(sys.argv[2], 'w')
except:
    print(f'Не удалось открыть файл для записи {sys.argv[2]}!')
    exit()

for line in fhand:
    if not len(line) or line[0] == '!':
        continue
    try:
        for cmd in ignore:
            if cmd in line:
                raise Exception
    except:
        continue
    fout.write(line)

fhand.close()
fout.close()
