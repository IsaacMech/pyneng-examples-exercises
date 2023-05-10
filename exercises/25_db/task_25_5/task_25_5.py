# -*- coding: utf-8 -*-
"""
Задание 25.5

Для заданий 25 раздела нет тестов!

После выполнения заданий 25.1 - 25.5 в БД остается информация о неактивных записях.
И, если какой-то MAC-адрес не появлялся в новых записях, запись с ним,
может остаться в БД навсегда.

И, хотя это может быть полезно, чтобы посмотреть, где MAC-адрес находился
в последний раз, постоянно хранить эту информацию не очень полезно.

Например, если запись в БД уже больше месяца, то её можно удалить.

Для того, чтобы сделать такой критерий, нужно ввести новое поле,
в которое будет записываться последнее время добавления записи.

Новое поле называется last_active и в нем должна находиться строка,
в формате: YYYY-MM-DD HH:MM:SS.

В этом задании необходимо:
* изменить, соответственно, таблицу dhcp и добавить новое поле.
 * таблицу можно поменять из cli sqlite, но файл dhcp_snooping_schema.sql тоже необходимо изменить
* изменить скрипт add_data.py, чтобы он добавлял к каждой записи время

Получить строку со временем и датой, в указанном формате,
можно с помощью функции datetime в запросе SQL.
Синтаксис использования такой:
sqlite> insert into dhcp (mac, ip, vlan, interface, switch, active, last_active)
   ...> values ('00:09:BC:3F:A6:50', '192.168.100.100', '1', 'FastEthernet0/7', 'sw1', '0', datetime('now'));

То есть вместо значения, которое записывается в базу данных,
надо указать datetime('now').

После этой команды в базе данных появится такая запись:
mac                ip               vlan  interface        switch  active  last_active
-----------------  ---------------  ----  ---------------  ------  ------  -------------------
00:09:BC:3F:A6:50  192.168.100.100  1     FastEthernet0/7  sw1     0       2019-03-08 11:26:56
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
