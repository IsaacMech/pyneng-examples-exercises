# -*- coding: utf-8 -*-
"""
Задание 25.5a

Для заданий 25 раздела нет тестов!

После выполнения задания 25.5, в таблице dhcp есть новое поле last_active.

Обновите скрипт add_data.py, таким образом, чтобы он удалял все записи,
которые были активными более 7 дней назад.

Для того, чтобы получить такие записи, можно просто вручную обновить поле last_active
в некоторых записях и поставить время 7 или более дней.

В файле задания описан пример работы с объектами модуля datetime.
Показано как получить дату 7 дней назад.
С этой датой надо будет сравнивать время last_active.

Обратите внимание, что строки с датой, которые пишутся в БД, можно сравнивать
между собой.

"""

from datetime import datetime, timedelta

now = datetime.today().replace(microsecond=0)
week_ago = now - timedelta(days=7)

# print(now)
# print(week_ago)
# print(now > week_ago)
# print(str(now) > str(week_ago))
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
            set_str.append(str(col) + ' = "' + str(val) + '"')
        command += ', '.join(set_str)
        if where_list:
            command += ' WHERE '
            where_str = []
            for cond in where_list:
                where_str.append(str(cond[0]) + ' = ' + str(cond[2]))
            command += ' AND '.join(where_str)
        self.cursor.execute(command)
        self.save()
    def remove_data(self, table, param_list):
        command = 'DELETE FROM ' + table + ' WHERE '
        str_param_list = []
        for param, val in param_list:
            str_param_list.append(param + ' = "' + val + '"')
        command += ', '.join(str_param_list)
        print(command)
        self.cursor.execute(command)
        self.save()
