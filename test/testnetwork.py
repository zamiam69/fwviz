"""Unit test for network.network"""
from network.network import NIC, Route, RoutingTable, NICAddress, NICFactory
import IPy
import pprint

legal_addr_v4 = [
              "127.0.0.1/8",
              "10.11.12.13/23",
              "0.0.0.0",
              "217.10.64.172/25",
              "217.10.64.171",
              "0.0.0.0/0",
              "144.1.1.0/255.255.255.0",
              "10.1.1.1/16"
               ]

illegal_addr_v4 = [
                   "256.0.0.0",
                   "127.0.0.0/33",
                   "1.2.3.4.5",
                   "1.2.3",
                   "a.b.c.d/e",
                   "127.0.0.0/0.256.0.0",
                   "127.0.0.0/1.2.3.4.5",
                   "127.0.0.0/1.2.3"
                   ]

legal_routes_v4 = [
                    ["127.0.0.0/8", "127.0.0.1"],
                    ["0.0.0.0/0", "192.168.10.1"],
                    ["192.168.0.0/16", "192.168.0.1"],
                    ["10.0.192.0/18", "10.0.193.0"]
                   ]

def checkLegalAddr(*args):
    """create an interface with a legal address"""
    return NIC(args)

def failIllegalAddr(*args):
    """create an interface with and illegal address"""
    return not NIC(args)

def checkRouteLookup(routingtable, address, gateway, nic):
    r = routingtable.lookup(IPy.IP(address))
    assert r.gateway == IPy.IP(gateway) and r.nic == nic

def checkNICAddress(addr, checkaddr, checknetmask, checknetwork):
        naddr = NICAddress(addr)
        assert naddr.address == IPy.IP(checkaddr) and \
            naddr.netmask == IPy.IP(checknetmask) and \
            naddr.network == IPy.IP(checknetwork)
            
def checkRoute(network, nic, gateway):
    r = Route(network, nic, gateway)
    assert IPy.IP(network) == r.network and \
                IPy.IP(gateway) == r.gateway
                
def checkContains(alist, obj):
    assert obj in alist

class TestNIC:
    """Unit tests for the NIC class"""

    def testInitString(self):
        """test nic creation"""
        nic = NICFactory("lo")
        assert nic.name == "lo"

    def testNICState(self):
        """test state getter and setter"""

        # state after initialisation must be "down".
        nic = NICFactory("eth0")
        assert nic.state == "down"

        # test the setter
        nic.state = "up"
        assert nic.state == "up"

        # test resetting
        nic.state = "down"
        assert nic.state != "up"

        # try an illegal value, must raise a ValueError
        try:
            nic.state = "off"
        except ValueError:
            assert True
        else:
            assert False

    def testNIC(self):
        """test the NIC setters and getters"""
        nic = NICFactory("eth0:1")

        assert nic.name == "eth0:1"
        assert nic.state == "down"
        # pprint.pprint(nic.addresses)
        assert nic.addresses == []

        nic.state = "up"
        assert nic.state == "up"

        addresses = map(NICAddress, legal_addr_v4)
        nic.addresses.extend(addresses)
        assert len(nic.addresses) == len(legal_addr_v4)
        assert nic.state == "up"

        for naddr in addresses:
            nic.addresses.remove(naddr)

        assert len(nic.addresses) == 0
        assert nic.state == "up"

        nic.state = "down"
        assert nic.state == "down"


    def testNICAddress(self):
        """test the NICAddress class"""
        checkdata = [
                     ["217.10.66.66/32", "217.10.66.66", "255.255.255.255", "217.10.66.66/32"],
                     ["127.0.0.1/8", "127.0.0.1", "255.0.0.0", "127.0.0.0/8"],
                     ["192.168.10.3/23", "192.168.10.3", "255.255.254.0", "192.168.10.0/23"],
                     ["217.10.64.172/20", "217.10.64.172", "255.255.240.0", "217.10.64.0/20"],
                     ]
        
        for addr, checkaddr, checknetmask, checknetwork in checkdata:
            yield(checkNICAddress, addr, checkaddr, checknetmask, checknetwork)

    def testNICAddressList(self):
        """test NICAddressList"""
        nic = NIC("eth0:1")
        # print nic.addresses
        assert nic.addresses == []

        addresses = [ NICAddress(a) for a in legal_addr_v4 ]
        nic.addresses.extend(addresses)
        assert len(nic.addresses) == len(legal_addr_v4)
        
        for naddr in addresses:
            yield(checkContains, nic.addresses, naddr)
            # nic.addresses.remove(naddr)

        #assert len(nic.addresses) == 0 and nic.addresses == []

class TestRoute:
    """Unit tests for the Route class"""

    def testRoute(self):
        "Route: test the constructor"
        for route in legal_routes_v4:
            yield(checkRoute, route[0], "test0", route[1])
  
class TestRoutingTable:
    """Unit tests for the RoutingTable class"""

    def testRoutingTable(self):
        """RoutingTable: test the class"""
        routedata = [
                  ["0.0.0.0/0", "192.168.10.1", "eth0" ],
                  ["192.168.10.0/24", "192.168.10.1", "eth0"],
                  ["192.168.10.0/23", "192.168.11.1", "eth1"],
                  ["10.0.0.0/8", "10.0.0.1", "eth1"],
                  ["127.0.0.0/8", "127.0.0.1", "lo"],
                ]

        rt = RoutingTable()
        for d in routedata:
            r = Route(d[0], d[2], d[1])
            rt.append(r)
            
        checkdata = [
                     ["1.2.3.4", "192.168.10.1", "eth0"],
                     ["192.168.10.13", "192.168.10.1", "eth0"],
                     ["192.168.11.117", "192.168.11.1", "eth1"],
                     ["127.1.1.1", "127.0.0.1", "lo"],
                     ["10.1.2.0", "10.0.0.1", "eth1"]
                     ]
        
        for addr, gw, nic in checkdata:
            yield(checkRouteLookup, rt, addr, gw, nic)