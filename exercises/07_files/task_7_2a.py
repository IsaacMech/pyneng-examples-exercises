# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт: Скрипт не должен выводить на стандартрый поток вывода команды,
в которых содержатся слова из списка ignore.

При этом скрипт также не должен выводить строки, которые начинаются на !.

Проверить работу скрипта на конфигурационном файле config_sw1.txt.
Имя файла передается как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]

import sys

if len(sys.argv) < 2:
    print('Недостаточно аргументов!')
    exit()

try:
    fhand = open(sys.argv[1], 'r')
except:
    print(f'Не удалось открыть файл {sys.argv[1]}!')
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
    print(line, end='')

fhand.close()
