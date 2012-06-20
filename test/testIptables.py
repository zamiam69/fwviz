"""
Created on Jun 19, 2012

@author: maz

Unit test for fwviz.iptables"""

from fwviz.iptables.firewall import IptablesNetwork

#import IPy
import pprint


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
        for a in al:
            #print a.address
            #print a.netmask
            print a



