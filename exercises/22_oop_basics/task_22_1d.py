# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Соединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Соединение с одним из портов существует


"""

topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}
class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
    def _normalize(self, topo_dict):
        filtered = {}
        for local, remote in topo_dict.items():
            if remote[0] in dict(filtered.keys()):
                continue
            filtered[local] = remote
        return filtered
    def delete_link(self, local, remote):
        if (local, remote) in self.topology.items():
            del self.topology[local]
        elif (remote, local) in self.topology.items():
            del self.topology[remote]
        else:
            print('Такого соединения нет')
    def delete_node(self, node):
        copy = {}
        for local, remote in self.topology.items():
            if local[0] == node or remote[0] == node:
                continue
            copy[local] = remote
        if copy == self.topology:
            print('Такого устройства нет')
        else:
            self.topology = copy
    def add_link(self, local, remote):
        if not (local and remote):
            print('Недостаточно аргументов')
            return None
        if (local, remote) in self.topology.items():
            print('Такое соединение существует')
        elif local in tuple(self.topology.keys()) + tuple(self.topology.values())      \
            or remote in tuple(self.topology.keys()) + tuple(self.topology.values()):
            print('Соединение с одним из портов существует')
        else:
            self.topology[local] = remote

from pprint import pprint

if __name__ == '__main__':
    x = Topology(topology_example)
    pprint(x.topology)
    x.delete_node('R5')
    pprint(x.topology)
    x.delete_node('R3')
    pprint(x.topology)
    x.delete_node('R5')
    pprint(x.topology)
    x.add_link(("R1", "Eth0/0"), ("SW1", "Eth0/1"))
    pprint(x.topology)
    x.add_link(("R3", "Eth0/0"), ("SW1", "Eth0/3"))
    pprint(x.topology)
