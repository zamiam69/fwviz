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
    if isinstance(addr, str):
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
        self.__routingtable = None
        self.__nics = None
        self.__plumbing = None

    def addNIC(self, name):
        """add a network interface"""
        raise NotImplementedError("Should have implemented this")

    def update(self, subject):
        """Called by observer subjects"""
        raise NotImplementedError("Should have implemented this")

class NIC(FwColleague):
    """Implements a network interface"""
    def __init__(self, name, **kwargs):
        """Constructor"""
        super(NIC, self).__init__(kwargs)
        self.name = name
        self.__state = "down"
        self.__address = NICAddressList()

    @property
    def state(self):
        """state getter"""
        return self.__state

    @state.setter
    def state(self, value):
        """state setter"""
        if value not in ["up", "down"]:
            raise ValueError("""state is either "up" or "down"!""")
        self.__state = value
        self.report("ifState")

    @property
    def address(self):
        """address getter"""
        return self.__address

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

    def onEvent(self, event, *args, **kwargs):
        """I only report"""
        pass

class NICAddress(object):
    """IP address object"""
    def __init__(self, address):
        # super(NICAddress, self).__init__(address, network)
        self.__address, self.__netmask = setAddr(address)

    def __str__(self):
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
        print event
        # pass
