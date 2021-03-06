# -*- coding: utf-8 -*-
"""
@author: maz <witte@netzquadrat.de>
@copyright: 2012 netzquadrat GmbH
"""

# import pprint

from fwviz.firewall import Firewall, FwPlumbing
from network.network import Network, RoutingTable, NICFactory, NIC
# from fwviz.fwcommand import IptablesCmd

class IptablesFw(Firewall):
    """An iptables based firewall"""
    def __init__(self):
        """Constructor"""
        super(IptablesFw, self).__init__()
        self.__type = "iptables"
        self.__network = IptablesNetwork()

    def confRules(self, rules):
        """configure firewall rules"""
        pass

    def recv(self, packet):
        """receive a network packet"""
        pass

    def send(self, packet):
        """send a network packet"""
        pass

#    def fromParser(self, tree):
#        rulecommand = tree[0]
#        rule = tree[1:]
        #if rulecommand[0] != '-A':
        #    print rulecommand[0]

class IptablesNetwork(Network):
    """Network for an iptables firewall"""

    __events = {
               "nic": { 
                        "address": ["Change", "Del", "Add" ] 
                       },
               "routingtable": { 
                        "nic": ["Up", "Down"],
                        "address": [ "Change", "Del", "Add" ]
                },
    }

    def __init__(self):
        super(IptablesNetwork, self).__init__()
        self._plumbing = IptablesPlumbing()
        self._routingtable = RoutingTable(mediator=self)
        
        # register 
        for eventgroup in self.__events['routingtable']:
            actions = self.__events["routingtable"][eventgroup]
            self.register(self._routingtable, eventgroup, *actions)

    def addNIC(self, nicname):
        """add a nic"""
        try:
            nic = NICFactory(nicname, mediator=self)
            self._nics.append(nic)
        except:
            raise

        #for event in self.__events['nic']:
        #    self.register(nic, event)

    def getNIC(self, nic):
        """search for nics"""
        if isinstance(nic, str):
            found, = filter(lambda x: nic == x.name, self._nics)
        elif isinstance(nic, NIC):
            found, = filter(lambda x: nic == x, self._nics)
        else:
            raise NameError
        return found

    def delNIC(self, nic):
        """remove a nic"""
        if isinstance(nic, str):
            delnic = self.getNIC(nic)
            self._nics.remove(delnic)
        elif isinstance(nic, NIC):
            self._nics.remove(nic)
        else:
            raise
        #for event in self.__events['nic']:
        #    self.unregister(nic, event)



class IptablesPlumbing(FwPlumbing):
    """Simple simulation of iptables/netfilter"""

    def __init__(self):
        """Constructor"""
        super(IptablesPlumbing, self).__init__()
        self.__tables = {}
        self.__tables["nat"] = Table("nat")
        self.__tables["mangle"] = Table("mangle")
        self.__tables["filter"] = Table("filter")

    def addRule(self):
        pass

    def process(self, packet):
        pass

#
class Table(object):
    """Implements an netfilter table"""
    def __init__(self, name):
        if name == "filter":
            self.builtins = "INPUT", "OUTPUT", "FORWARD"
        elif name == "nat":
            self.builtins = "PREROUTING", "OUTPUT", "POSTROUTING"
        elif name == "mangle":
            self.builtins = "PREROUTING", "POSTROUTING", "INPUT", \
                "FORWARD", "OUTPUT"
        elif name == "raw":
            self.builtins = "PREROUTING", "OUTPUT"
        elif name == "security":
            self.builtins = "INPUT", "OUTPUT", "FORWARD"

        self.chains = []

    def addChain(self, chain):
        """add a table to a firewall"""
        self.chains.append(chain)

    def delChain(self, chain):
        """delete a table from a firewall"""
        self.chains.remove(chain)


class Chain(object):
    """Implements a netfilter rule chain"""
    def __init__(self, name):
        self.name = name
        self.rules = []

    def append(self, rule):
        """append a rule to a chain"""
        self.rules.append(rule)

    def insert(self, rule, pos=1):
        """insert a rule to a chain"""
        self.rules.insert(pos - 1, rule)

    def delete(self, rule):
        """delete a rule from chain"""
        pass

    def match(self, packet):
        """match a packet against the rules in this chain"""
        pass

class Rule(object):
    """Implements an netfilter rule"""
    def __init__(self, options):
        self._counter = 0
        self._options = options

    def __eq__(self, other):
        pass

    def match(self, packet):
        """match a packet against this rule"""
        pass


class RuleParser(object):
    """abstract class for a rule parser"""

    def parseRules(self):
        """This is an a interface"""
        raise NotImplementedError(
"""Exception raised, ImageFinder is supposed to be an interface/abstract class!
""")


class RuleParserNfDump(RuleParser):
    """parse an iptables-save rule dump"""

    def parseRules(self):
        pass
