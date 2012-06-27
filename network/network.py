# -*- coding: utf-8 -*-
"""
Created on Apr 11, 2012

@author: maz
"""

import IPy
from fwviz.base import FwColleague, FwMediator
import pprint

def setAddr(addr):
    """enable setting of an address"""
    if isinstance(addr, NICAddress):
        return addr

    # 
    try:
        addr = IPy.IP(addr)
    except ValueError as ve:
        x = addr.find('/')
        if x > 1:
            try:
                net = IPy.IP(addr, make_net=True)
            except:
                raise ve
            else:
                addr = IPy.IP(addr[0:x] + "/32")
    else:
        net = addr

    return addr, net.netmask()

class Network(FwMediator):
    """Abstract network class"""

    def __init__(self):
        """Constructor"""
        super(Network, self).__init__()
        self._routingtable = None
        self._nics = []
        self._plumbing = None

    @property
    def nics(self):
        """getter"""
        return self._nics

    @property
    def routes(self):
        """getter for the routingtable"""
        return self._routingtable.routes

    def addNIC(self, name):
        """add a network interface"""
        raise NotImplementedError("Should have implemented this")


class NIC(FwColleague):
    """Implements a network interface"""
    def __init__(self, name, **kwargs):
        """Constructor"""
        super(NIC, self).__init__(kwargs)
        self.name = name
        self._state = "down"
        self._addresses = NICAddressList()

    def __repr__(self):
        return """NIC: {self.name} 
    State: {self._state}
    Adresses: {self._addresses}
""".format(self=self)

    @property
    def state(self):
        """state getter"""
        return self._state

    @state.setter
    def state(self, value):
        """state setter"""
        if value not in ["up", "down"]:
            raise ValueError("""state is either "up" or "down"!""")
        self._state = value
        self.report("ifState")

    @property
    def addresses(self):
        """address getter"""
        return self._addresses

class NICFactory(object):
    """NIC factory class"""

    def __new__(cls, name, **kwargs):
        return NIC(name, **kwargs)

class NICAddressList(list, FwColleague):
    """A list of NICAddresses"""

    def __init__(self, mediator=None):
        """Constructor"""
        list.__init__(self, [])
        FwColleague.__init__(self, mediator=mediator)

    def __repr__(self):
        return "\n".join(self)

    # override destructive methods
    def __setitem__(self, index, addr):
        na = setAddr(addr)
        super(NICAddressList, self).__setitem__(index, na)

    def __iadd__(self, addrs):
        nas = []
        for addr in addrs:
            nas.append(setAddr(addr))
        super(NICAddressList, self).__iadd__(nas)

    def append(self, addr):
        na = setAddr(addr)
        super(NICAddressList, self).append(na)

    def extend(self, addrs):
        nas = []
        for addr in addrs:
            nas.append(setAddr(addr))
        super(NICAddressList, self).extend(nas)

    def remove(self, addr):
        na = setAddr(addr)
        super(NICAddressList, self).remove(na)

    def insert(self, index, addr):
        na = setAddr(addr)
        super(NICAddressList, self).insert(index, na)


    def onEvent(self, event, *args, **kwargs):
        """I only report"""
        print "Event received."

class NICAddress(object):
    """IP address object"""
    def __init__(self, address):
        # super(NICAddress, self).__init__(address, network)
        self.__address, self.__netmask = setAddr(address)

    def __repr__(self):
        """String representation"""
        return "{0}/{1}".format(self.__address, self.__netmask)

    @property
    def address(self):
        """address getter"""
        return self.__address

    @address.setter
    def address(self, addr):
        """address setter"""
        self.__address, self.__netmask = setAddr(addr)

    @property
    def netmask(self):
        """network getter"""
        return self.__netmask

class Route(object):
    """Implements an IP routing table entry"""

    def __init__(self, network, nic, gateway, metric=0):
        """Constructor"""
        self.network = IPy.IP(network)
        self.nic = nic
        self.gateway = IPy.IP(gateway)
        self.metric = metric

    def __eq__(self, other):
        return self.network == other.network and self.metric == other.metric \
            and self.nic == other.nic and self.gateway == other.gateway

    def __le__(self, other):
        return (self.network in other.network) and (self.metric <= other.metric)

    def __ge__(self, other):
        return self <= other

    def __gt__(self, other):
        return self != other and self >= other

    def __lt__(self, other):
        return self != other and self <= other

    def __repr__(self):
        return "{0} {1} {2} {3}".format(
            self.network, self.gateway, self.nic, self.metric)

class RoutingTable(FwColleague):
    """Implements a simple routing table"""

    def __init__(self, **kwargs):
        super(RoutingTable, self).__init__(kwargs)
        self._routes = []

    @property
    def routes(self):
        """getter"""
        return self._routes

    def add(self, route):
        """Add a route to the routing table"""
        self._routes.append(route)
        self._routes.sort()

    def delete(self, route):
        """Delete a route from the routing table"""
        self._routes.remove(route)

    def lookup(self, address):
        """Lookup the route for a given address"""
        for r in self._routes:
            if address in r.network:
                return r

    def onEvent(self, event, *args, **kwargs):
        """Receive events"""
        print "..................", event
        # pass
