import threading
from typing import *


class BmfNet:
    _instance_lock = threading.Lock()
    _net_pool = {}

    def __new__(cls, global_name, voltage=None, *args, **kwargs):
        if global_name not in BmfNet._net_pool:
            with BmfNet._instance_lock:
                _instance = object.__new__(cls)
                _instance.uuid = global_name
                _instance.voltage = voltage
                BmfNet._net_pool[_instance.uuid] = _instance

        return BmfNet._net_pool.get(global_name, None)

    @classmethod
    def get_net_by_uuid(cls, uuid):
        return cls._net_pool.get(uuid, None)


class BmfDevice:
    def __init__(self, name):
        self.name = name
        self.terminal: Dict[str, str] = {}


class Device:
    def __init__(self):
        self._bmf_device: Optional[BmfDevice] = None

    @property
    def terminals(self):
        if not self._bmf_device:
            return []
        terminals = []
        for terminal, net in self._bmf_device.terminal.items():
            term_inst = Terminal(terminal, self)
            bmf_net = BmfNet(global_name=net)
            net = Net(net)
            net.bmf_net = bmf_net
            net.add_terminal(term_inst)
            terminals.append(term_inst)

        return terminals


class Net:
    def __init__(self, name):
        self.name = name
        self.__terminals = set()
        self.bmf_net: BmfNet = None

    def add_terminal(self, terminal):
        self.__terminals.add(terminal)
        if terminal.__net is not self:
            terminal.set_net(self)

    @property
    def terminals(self):
        return self.__terminals


class Terminal:
    def __init__(self, name, device):
        self.name = name
        self.__net: Optional[BmfNet] = None
        self.__device: Device = device

    def set_net(self, net_inst):
        self.__net = net_inst
        if self not in self.__net.__terminals:
            self.__net.add_terminal(self)

    @property
    def net(self):
        return self.__net

    @property
    def device(self):
        return self.__device


class SchematicGraph:
    def __init__(self, devices: List[Device] = None):
        self.__devices: List[Device] = devices

    @property
    def terminals(self):
        pass


if __name__ == '__main__':

    pass