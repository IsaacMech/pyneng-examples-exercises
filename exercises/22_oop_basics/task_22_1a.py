# -*- coding: utf-8 -*-

"""
Задание 22.1a

Скопировать класс Topology из задания 22.1 и изменить его.

Перенести функциональность удаления "дублей" в метод _normalize.
При этом метод __init__ должен выглядеть таким образом:
"""

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
from pprint import pprint

if __name__ == '__main__':
    x = Topology(topology_example)
    pprint(x.topology)
