# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""
from concurrent.futures import ThreadPoolExecutor
import subprocess
import yaml

def ping_ip_address(ip):
    return subprocess.run(['ping', ip], stdout=subprocess.DEVNULL).returncode, ip

def ping_ip_addresses(ip_list, limit=3):
    ok_ip = []
    bad_ip = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(ping_ip_address, ip_list)
    for ip in result:
        if ip[0]:
            bad_ip.append(ip[1])
            continue
        ok_ip.append(ip[1])
    return ok_ip, bad_ip

if __name__ == '__main__':
    with open('devices.yaml', 'r') as fileh:
        devices = yaml.safe_load(fileh)
    ip_list = []
    for device in devices:
        ip_list.append(device['host'])
    print(ping_ip_addresses(ip_list + ['256.256.256.256', '10.148.31.2']))
