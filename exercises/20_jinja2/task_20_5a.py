# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""

data = {
    "tun_num": None,
    "wan_ip_1": "10.0.100.100",
    "wan_ip_2": "10.0.100.101",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}

import yaml
from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler
from task_20_5 import create_vpn_config

def get_tun_intf_list(device):
    '''
    Берёт на вход словарь параметров подключений, возвращает список названий интерфейсов
    input: словарь с параметра подключения
    output: список названий интерфейсов
    '''
    result = []
    with ConnectHandler(**device) as dev:
        tunnels = dev.send_command('show interfaces summary | include Tunnel')
    for tunnel in tunnels.split('\n'):
        try:
            result.append(tunnel.strip().split()[0])
        except:
            continue
    return result

def send_config_commands(device, commands):
    with ConnectHandler(**device) as devcon:
        devcon.enable()
        return devcon.send_config_set(commands)

def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    if not vpn_data_dict['tun_num']:
        tunnels = []
        with ThreadPoolExecutor(max_workers=2) as executor:
            for result in executor.map(get_tun_intf_list, (src_device_params, dst_device_params)):
                tunnels += result
        num = 1
        while True:
            if 'Tunnel' + str(num) in tunnels:
                num += 1
                continue
            break
        vpn_data_dict['tun_num'] = num
    src_conf, dst_conf = create_vpn_config(src_template, dst_template, vpn_data_dict)
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        futures.append(executor.submit(send_config_commands, src_device_params, src_conf.split('\n')))
        futures.append(executor.submit(send_config_commands, dst_device_params, dst_conf.split('\n')))
        return futures[0].result(), futures[1].result()

if __name__ == "__main__":
    with open('devices.yaml', 'r') as fileh:
        devices = yaml.safe_load(fileh)
    src_device = devices[0]
    dst_device = devices[1]
    template1_file = "templates/gre_ipsec_vpn_1.txt"
    template2_file = "templates/gre_ipsec_vpn_2.txt"
    print(configure_vpn(src_device, dst_device, template1_file, template2_file, data))
