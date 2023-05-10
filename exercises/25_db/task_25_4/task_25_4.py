# -*- coding: utf-8 -*-
"""
Задание 25.4

Для заданий 25 раздела нет тестов!

Скопировать файл get_data из задания 25.2.
Добавить в скрипт поддержку столбца active, который мы добавили в задании 25.3.

Теперь, при запросе информации, сначала должны отображаться активные записи,
а затем, неактивные. Если неактивных записей нет, не отображать
заголовок "Неактивные записи".

Примеры выполнения итогового скрипта
$ python get_data.py
В таблице dhcp такие записи:

Активные записи:

-----------------  ----------  --  ----------------  ---  -
00:09:BB:3D:D6:58  10.1.10.2   10  FastEthernet0/1   sw1  1
00:04:A3:3E:5B:69  10.1.15.2   15  FastEthernet0/15  sw1  1
00:05:B3:7E:9B:60  10.1.5.4     5  FastEthernet0/9   sw1  1
00:07:BC:3F:A6:50  10.1.10.6   10  FastEthernet0/5   sw1  1
00:E9:BC:3F:A6:50  100.1.1.6    3  FastEthernet0/20  sw3  1
00:E9:22:11:A6:50  100.1.1.7    3  FastEthernet0/21  sw3  1
00:A9:BB:3D:D6:58  10.1.10.20  10  FastEthernet0/7   sw2  1
00:B4:A3:3E:5B:69  10.1.5.20    5  FastEthernet0/5   sw2  1
00:A9:BC:3F:A6:50  10.1.10.65  20  FastEthernet0/2   sw2  1
00:A9:33:44:A6:50  10.1.10.77  10  FastEthernet0/4   sw2  1
-----------------  ----------  --  ----------------  ---  -

Неактивные записи:

-----------------  ---------------  -  ---------------  ---  -
00:09:BC:3F:A6:50  192.168.100.100  1  FastEthernet0/7  sw1  0
00:C5:B3:7E:9B:60  10.1.5.40        5  FastEthernet0/9  sw2  0
-----------------  ---------------  -  ---------------  ---  -

$ python get_data.py vlan 5

Информация об устройствах с такими параметрами: vlan 5

Активные записи:

-----------------  ---------  -  ---------------  ---  -
00:05:B3:7E:9B:60  10.1.5.4   5  FastEthernet0/9  sw1  1
00:B4:A3:3E:5B:69  10.1.5.20  5  FastEthernet0/5  sw2  1
-----------------  ---------  -  ---------------  ---  -

Неактивные записи:

-----------------  ---------  -  ---------------  ---  -
00:C5:B3:7E:9B:60  10.1.5.40  5  FastEthernet0/9  sw2  0
-----------------  ---------  -  ---------------  ---  -


$ python get_data.py vlan 10

Информация об устройствах с такими параметрами: vlan 10

Активные записи:

-----------------  ----------  --  ---------------  ---  -
00:09:BB:3D:D6:58  10.1.10.2   10  FastEthernet0/1  sw1  1
00:07:BC:3F:A6:50  10.1.10.6   10  FastEthernet0/5  sw1  1
00:A9:BB:3D:D6:58  10.1.10.20  10  FastEthernet0/7  sw2  1
00:A9:33:44:A6:50  10.1.10.77  10  FastEthernet0/4  sw2  1
-----------------  ----------  --  ---------------  ---  -
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
            self.connection.execute(f'INSERT OR REPLACE INTO {table} VALUES (' + '?, '*(rows-1) + '?)', data_tuple)
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
    def get_data(self, table, col=None, val=None, sel_col='*'):
        if col and val:
            self.cursor.execute(f'SELECT {sel_col} FROM {table} WHERE {col} = "{val}"')
        else:
            self.cursor.execute(f'SELECT {sel_col} FROM {table}')
        return self.cursor.fetchall()
    def update_data(self, table, set_list, where_list=None):
        '''
        UPDATE table SET (set[0][0] = set[0][1], set[1][0] = set[1][1]) [ WHERE where[0][0] = where[0][1] AND where[1][0] = where[1][1] ]
        '''
        command = 'UPDATE ' + table + ' SET '
        set_str = []
        for col, val in set_list:
            set_str.append(str(col) + ' = ' + str(val))
        command += ', '.join(set_str)
        if where_list:
            command += ' WHERE '
            where_str = []
            for cond in where_list:
                where_str.append(str(cond[0]) + ' = ' + str(cond[2]))
            command += ' AND '.join(where_str)
        self.cursor.execute(command)
