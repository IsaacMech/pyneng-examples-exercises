# -*- coding: utf-8 -*-

"""
Задание 22.1c

Изменить класс Topology из задания 22.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

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
