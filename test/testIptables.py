"""
Created on Jun 19, 2012

@author: maz

Unit test for fwviz.iptables"""

from fwviz.iptables.firewall import IptablesNetwork
from network.network import NIC

#import IPy
#import pprint


class testIptablesNetwork:
    """test IptablesNetwork class"""

    def testSetup(self):
        """setting up a network"""
        N = IptablesNetwork()
        lo = NIC("lo")
        N.addNIC(lo)

