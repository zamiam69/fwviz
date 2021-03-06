# -*- coding: utf-8 -*-
"""
Created on Apr 11, 2012

@author: maz
"""

import IPy
from fwviz.base import FwColleague, FwMediator, FwMediatedList
from abc import abstractmethod
# import pprint

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
        """getter for the routingtable's routes"""
        return self._routingtable.routes
    
    @property
    def routingtable(self):
        """getter for the routingtable"""
        return self._routingtable

    @abstractmethod
    def addNIC(self, name):
        """add a network interface"""
        raise NotImplementedError("Should have implemented this")

    @abstractmethod
    def getNIC(self, nic):
        """find a nic"""
        pass

    @abstractmethod
    def delNIC(self, nic):
        """delete a nic"""
        pass

class NIC(FwColleague):
    """Implements a network interface"""
    def __init__(self, name, **kwargs):
        """Constructor"""
        super(NIC, self).__init__(kwargs)
        self.name = name
        self._state = "down"
        if "mediator" in kwargs.keys():
            self._addresses = NICAddressList(kwargs["mediator"], nic=self)
        else:
            self._addresses = NICAddressList(nic=self)

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

    def onEvent(self, event, *args, **kwargs):
        print event

class NICFactory(object):
    """NIC factory class"""

    def __new__(cls, name, **kwargs):
        return NIC(name, **kwargs)

class NICAddressList(FwMediatedList):
    """A list of NICAddresses"""

    def __init__(self, mediator=None, eventgroup="address", data=None, \
                 nic=None):
        """Constructor"""
        super(NICAddressList, self).__init__(mediator, eventgroup, data)
        self.__nic=nic
        
    @property
    def nic(self):
        return self.__nic

    def __str__(self):
        return "\n".join(str(na) for na in self._data)

    # override destructive methods
    def __setitem__(self, index, addr):
        na = NICAddress(addr)
        super(NICAddressList, self).__setitem__(index, na)

    def __iadd__(self, addrs):
        nas = []
        for addr in addrs:
            nas.append(NICAddress(addr))
        super(NICAddressList, self).__iadd__(nas)

    def append(self, addr):
        na = NICAddress(addr)
        super(NICAddressList, self).append(na)

    def extend(self, addrs):
        nas = []
        for addr in addrs:
            nas.append(NICAddress(addr))
        super(NICAddressList, self).extend(nas)

    def remove(self, addr):
        na = NICAddress(addr)
        super(NICAddressList, self).remove(na)

    def insert(self, index, addr):
        na = NICAddress(addr)
        super(NICAddressList, self).insert(index, na)

    def onEvent(self, event):
        """I only report"""
        print "Event received."

class NICAddress(object):
    """IP address object"""
    def __init__(self, address):
        # super(NICAddreself.__addressss, self).__init__(address, network)
        if isinstance(address, NICAddress):
            self.__address = address.address
            self.__netmask = address.netmask
        else:
            self.__address, self.__netmask = setAddr(address)

    def __str__(self):
        """String representation"""
        return "{0}/{1}".format(self.__address, self.__netmask)
        
    def __repr__(self):
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
    
    @property
    def network(self):
        return self.__address.make_net(self.__netmask)

class Route(object):
    """Implements an IP routing table entry"""

    def __init__(self, network, nic, gateway, metric=0):
        """Constructor"""
        self.network = IPy.IP(network)
        self.nic = nic
        self.metric = metric
        if gateway:
            self.gateway = IPy.IP(gateway)
        else:
            self.gateway = ""
            
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

class RoutingTable(FwMediatedList):
    """Implements a simple routing table"""

    def __init__(self, *args, **kwargs):
        super(RoutingTable, self).__init__(args, kwargs)
        self.events = 0

    def __setitem__(self, index, value):
        super(RoutingTable, self).__setitem__(index, value)
        self._data.sort()

    def __iadd__(self, values):
        super(RoutingTable, self).__iadd__(values)
        self._data.sort()

    def append(self, value):
        super(RoutingTable, self).append(value)
        self._data.sort()

    def extend(self, values):
        super(RoutingTable, self).extend(values)
        self._data.sort()

    def insert(self, index, value):
        super(RoutingTable, self).insert(index, value)
        self._data.sort()

    @property
    def routes(self):
        """getter"""
        return self._data

    def lookup(self, address):
        """Lookup the route for a given address"""
        for r in self._data:
            if address in r.network:
                return r

    def onEvent(self, event):
        """Receive events"""
        self.events +=1
        reporter = event.reporter
        eventgroup = event.eventgroup
        action = event.action
        kwargs = event.kwargs
        
        if eventgroup == "address":
            nic = reporter.nic
            if kwargs.has_key("value"):
                addrs = [ kwargs["value"] ]
            elif kwargs.has_key("values"):
                addrs = kwargs["values"]
            if action == "Add":
                for a in addrs:
                    r = self.lookup(a)
                    print a, type(a)
                    if r is not None:
                        continue
                    #network = a[0].make_net(a[1])
                    #route = Route(network, nic, "")
                    #print ":", route
                    #if nic.state == "down":
                    #    continue
                    
            elif action == "Change":
                print kwargs
            elif action == "Del":
                print kwargs
        elif event == "nic":
            if action == "Up":
                pass
            elif action == "Down":
                pass
        else:
            print "Unhandled event: {0}".format(event)