# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
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
import copy

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
    def __add__(self, another):
        copy_self = copy.deepcopy(self)
        for local, remote in another.topology.items():
            copy_self.add_link(local, remote)
        return copy_self
    def __iter__(self):
        return iter(self.topology.items())
