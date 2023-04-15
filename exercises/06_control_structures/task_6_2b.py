# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
ip_type = 'Неправильный IP-адрес'
while ip_type == 'Неправильный IP-адрес':
    ip = input('Введите IP: ')

    try:
        octet_list = ip.split('.')
        if len(octet_list) != 4:
            raise Exception
        for octet in octet_list:
            if not (int(octet) >= 0 and int(octet) <= 255):
                raise Exception
    except:
        ip_type = 'Неправильный IP-адрес'
    else:
        ip_type = 'unused'
        octet1 = int(ip.split('.')[0])
        if ip == '0.0.0.0':
            ip_type = 'unassigned'
        elif ip == '255.255.255.255':
            ip_type = 'local broadcast'
        elif octet1 >= 1 and octet1 <= 223:
            ip_type = 'unicast'
        elif octet1 > 223 and octet1 <= 239:
            ip_type = 'multicast'

    print(ip_type)
