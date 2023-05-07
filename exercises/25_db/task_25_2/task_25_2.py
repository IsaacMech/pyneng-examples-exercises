# -*- coding: utf-8 -*-
"""
Задание 25.2

Для заданий 25 раздела нет тестов!

В этом задании необходимо создать скрипт get_data.py.

Код в скрипте должен быть разбит на функции.
Какие именно функции и как разделить код, надо решить самостоятельно.
Часть кода может быть глобальной.

Скрипту могут передаваться аргументы и, в зависимости от аргументов,
надо выводить разную информацию.
Если скрипт вызван:
* без аргументов, вывести всё содержимое таблицы dhcp
* с двумя аргументами, вывести информацию из таблицы dhcp,
  которая соответствует полю и значению
* с любым другим количеством аргументов, вывести сообщение,
  что скрипт поддерживает только два или ноль аргументов

Файл БД можно скопировать из задания 25.1.

Примеры вывода для разного количества и значений аргументов:

$ python get_data.py
В таблице dhcp такие записи:
-----------------  ---------------  --  ----------------  ---
00:09:BB:3D:D6:58  10.1.10.2        10  FastEthernet0/1   sw1
00:04:A3:3E:5B:69  10.1.5.2          5  FastEthernet0/10  sw1
00:05:B3:7E:9B:60  10.1.5.4          5  FastEthernet0/9   sw1
00:07:BC:3F:A6:50  10.1.10.6        10  FastEthernet0/3   sw1
00:09:BC:3F:A6:50  192.168.100.100   1  FastEthernet0/7   sw1
00:E9:BC:3F:A6:50  100.1.1.6         3  FastEthernet0/20  sw3
00:E9:22:11:A6:50  100.1.1.7         3  FastEthernet0/21  sw3
00:A9:BB:3D:D6:58  10.1.10.20       10  FastEthernet0/7   sw2
00:B4:A3:3E:5B:69  10.1.5.20         5  FastEthernet0/5   sw2
00:C5:B3:7E:9B:60  10.1.5.40         5  FastEthernet0/9   sw2
00:A9:BC:3F:A6:50  10.1.10.60       20  FastEthernet0/2   sw2
-----------------  ---------------  --  ----------------  ---

$ python get_data.py vlan 10

Информация об устройствах с такими параметрами: vlan 10
-----------------  ----------  --  ---------------  ---
00:09:BB:3D:D6:58  10.1.10.2   10  FastEthernet0/1  sw1
00:07:BC:3F:A6:50  10.1.10.6   10  FastEthernet0/3  sw1
00:A9:BB:3D:D6:58  10.1.10.20  10  FastEthernet0/7  sw2
-----------------  ----------  --  ---------------  ---

$ python get_data.py ip 10.1.10.2

Информация об устройствах с такими параметрами: ip 10.1.10.2
-----------------  ---------  --  ---------------  ---
00:09:BB:3D:D6:58  10.1.10.2  10  FastEthernet0/1  sw1
-----------------  ---------  --  ---------------  ---

$ python get_data.py vln 10
Данный параметр не поддерживается.
Допустимые значения параметров: mac, ip, vlan, interface, switch

$ python get_data.py ip vlan 10
Пожалуйста, введите два или ноль аргументов

"""

import sqlite3

class DBHandler():
    def __init__(self, filename, create=False):
        '''
        Выполняет открытие базы даннных. Если файла не существует и create не передан как True, поднимает исключение ValueError
        '''
        try:
            open(filename, 'r')
            if create:
                print('База данных существует.')
        except:
            if create:
                print('Создаю базу данных...')
            else:
                raise ValueError
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
    def create_schema(self, *, from_str=None, from_file=None):
        if from_str and from_file or (not from_str and not from_file):
            raise ValueError
        if from_str:
            schema = from_str
        elif from_file:
            with open(from_file, 'r') as fileh:
                schema = fileh.read()
        with self.connection as con:
            con.executescript(schema)
    def save(self):
        self.connection.commit()
    def add_data(self, table, rows, data_tuple):
        assert type(table) == str,'table должен быть строкой!'
        assert type(rows) == int and rows > 0,'rows должен быть больше 0!'
        assert type(data_tuple) == tuple,'data_tuple должен быть кортежем!'
        try:
            self.connection.execute(f'INSERT INTO {table} VALUES (' + '?, '*(rows-1) + '?)', data_tuple)
        except sqlite3.IntegrityError as e:
            print(f'При добавлении данных: {data_tuple} Возникла ошибка: {e}')
    def add_data_dict(self, data_dict):
        for table in data_dict:
            print(f'Добавляю данные в таблицу {table}...')
            self.cursor.execute(f'SELECT COUNT(*) FROM pragma_table_info(\'{table}\')')
            rows = self.cursor.fetchone()[0]
            for data in data_dict[table]:
                self.add_data(table, rows, data)
            self.save()
    def get_data(self, table, col=None, val=None):
        if col and val:
            self.cursor.execute(f'SELECT * FROM {table} WHERE {col} = "{val}"')
        else:
            self.cursor.execute(f'SELECT * FROM {table}')
        return self.cursor.fetchall()
