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

    def __str__(self):
        return getattr(self, 'uuid')

    def __repr__(self):
        return self.__str__()


class BmfDevice:
    def __init__(self, name, terminal: Dict[str, str] = None):
        self.name = name
        self.terminal: Dict[str, str] = terminal

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Device:
    def __init__(self, bmf_device=None):
        self._bmf_device: Optional[BmfDevice] = bmf_device
        self.terminals = self.get_terminals()

    @property
    def name(self):
        return self._bmf_device.name

    def get_terminals(self):
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

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Net:
    _instance_lock = threading.Lock()
    _net_pool = {}

    def __new__(cls, name, bmf_net=None, *args, **kwargs):
        if name not in cls._net_pool:
            with cls._instance_lock:
                _instance = object.__new__(cls)
                _instance.uuid = name
                _instance.name = name
                _instance.__terminals = set()
                _instance.bmf_net = bmf_net
                cls._net_pool[_instance.uuid] = _instance
        return cls._net_pool.get(name, None)

    def add_terminal(self, terminal):
        self.__terminals.add(terminal)
        if terminal.net is not self:
            terminal.set_net(self)

    @property
    def terminals(self):
        return self.__terminals

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    @classmethod
    def get_net_pool(cls):
        return cls._net_pool


class Terminal:
    def __init__(self, name, device):
        self.name = name
        self.__net: Optional[Net] = None
        self.__device: Device = device

    def set_net(self, net_inst):
        self.__net = net_inst
        if self not in self.__net.terminals:
            self.__net.add_terminal(self)

    @property
    def net(self):
        return self.__net

    @property
    def device(self):
        return self.__device

    def __str__(self):
        return self.device.name + ":" + self.name

    def __repr__(self):
        return self.__str__()


class SchematicGraph:
    def __init__(self, devices: List[Device] = None):
        self.__devices: List[Device] = devices

    @property
    def terminals(self):
        pass


if __name__ == '__main__':
    from dataset import reference_devices, hsy_device

    device_inst_list = []
    bmf_device_inst_list = []

    n_mos_inst_list = []
    p_mos_inst_list = []

    for item in hsy_device:
        device_name = item[0]
        terms = item[1]
        nets = item[2]
        term_net_map = {t: n for t, n in zip(terms, nets)}
        bmf_device_inst = BmfDevice(name=device_name, terminal=term_net_map)
        device_inst = Device(bmf_device=bmf_device_inst)
        bmf_device_inst_list.append(bmf_device_inst)
        device_inst_list.append(device_inst)
        if 'PM' in device_name:
            p_mos_inst_list.append(device_inst)
        elif 'NM' in device_name:
            n_mos_inst_list.append(device_inst)

    nets = Net.get_net_pool()

    n_mos_nets = list(set([term.net for device in n_mos_inst_list for term in device.terminals]))
    p_mos_nets = list(set([term.net for device in p_mos_inst_list for term in device.terminals]))

    public_nets = list(set([net for net in n_mos_nets if net in p_mos_nets]))

    print(n_mos_inst_list)
    print(p_mos_inst_list)
