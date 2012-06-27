"""
Created on Jun 19, 2012

@author: maz

Unit test for fwviz.iptables"""

from fwviz.iptables.firewall import IptablesNetwork

#import IPy
# import pprint


testAddresses = [
                 ["127.0.0.1/8", "127.0.0.1", "255.0.0.0"],
                 ["192.168.11.12/23", "192.168.11.12", "255.255.254.0" ],
                 ["10.11.12.13/9", "10.11.12.13", "255.128.0.0"],
                 ["66.66.66.66/32", "66.66.66.66", "255.255.255.255"]
                 ]


class testIptablesNetwork:
    """test IptablesNetwork class"""

    def testSetup(self):
        """setting up a network"""
        N = IptablesNetwork()

        nics = "lo", "eth0", "dummy0"
        for n in nics:
            N.addNIC(n)

        for n in nics:
            assert n == N.getNIC(n).name

        N.getNIC("lo").addresses.append("127.0.0.1/8")
        addresses = "192.168.11.12/23", "10.11.12.13/9", "66.66.66.66/32"
        N.getNIC("dummy0").addresses.extend(addresses)
        al = N.getNIC("dummy0").addresses
