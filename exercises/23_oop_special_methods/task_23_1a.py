# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""
class IPAddress():
    def __init__(self, string_ip):
        ip = string_ip.split('/')
        if len(ip) != 2:
            raise ValueError('Incorrect format!')
        ip_octets = ip[0].split('.')
        if len(ip_octets) != 4:
            raise ValueError('Incorrect IPv4 address')
        for octet in ip_octets:
            if int(octet) > 255 or int(octet) < 0:
                raise ValueError('Incorrect IPv4 address')
        if int(ip[1]) > 32 or int(ip[1]) < 8:
            raise ValueError('Incorrect mask')
        self.mask = int(ip[1])
        self.ip = ip[0]
    def __str__(self):
        return f'IP address {self.ip}/{self.mask}'
    def __repr__(self):
        return f'IPAddress(\'{self.ip}/{self.mask}\')'
