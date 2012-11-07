'''
Created on May 23, 2012

@author: maz
'''

import IPy
# import pprint
from fwviz.base import FwColleague

class Network(object):
    """Network"""
    def __init__(self):
        """Constructor"""
        pass

    def update(self):
        """Called by observer subjects."""
        raise NotImplementedError("You must define an update method.")

class NIC(FwColleague):
    """Implements a network interface"""

    def __init__(self, name, address=None, state="down"):
        super(NIC, self).__init__()
        self.name = name
        self.state = state
        self._address = []
        self.address = []

        if address:
            self._address.append(IPy.IP(address))
            self.address.append(address)

    def _state(self, state):
        """State of this interface"""
        self.state = state
        return state == self.state

    def up(self):
        """Take this interface up"""
        return self._state("up")

    def down(self):
        """Take this interface down"""
        return self._state("down")

    def addAddress(self, *addresses):
        """Add an address to this interface"""
        self._address.extend(IPy.IP(addr) for addr in addresses)
        self.address.extend(addresses)

    def delAddress(self, *addresses):
        """Delete an address from this interface"""
        for addr in addresses:
            self._address.remove(IPy.IP(addr))
            self.address.remove(addr)


class Route(object):
    """Implements an IP route"""

    def __init__(self, network, nic, gateway, metric=0):
        '''
        Constructor
        '''
        self.network = IPy.IP(network)
        self.nic = nic
        self.gateway = IPy.IP(gateway)
        self.metric = metric

    def __eq__(self, other):
        return self.network == other.network and self.metric == other.metric \
            and self.nic == other.nic and self.gateway == other.gateway

    def __le__(self, other):
        return (self.network in other.network) and (self.metric <= other.metric)

    def _ge__(self, other):
        return self <= other

    def __gt__(self, other):
        return self != other and self >= other

    def __lt__(self, other):
        return self != other and self <= other

    def __repr__(self):
        return "{0} {1} {2} {3}".format(self.network, self.gateway, self.nic,
                                        self.metric)


class RoutingTable(object):
    """Implements a simple routing table"""

    def __init__(self):
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
