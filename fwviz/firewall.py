"""
Created on May 23, 2012

@author: maz
"""


class Firewall(object):
    """Firewall"""

    def __init__(self):
        """Constructor"""
        super(Firewall, self).__init__()
        self.__nics = None
        self.__type = None
        self.__log = []
        self.__plumbing = None
        self.__network = None

    def confRules(self, rules):
        """configure firewall rules"""
        raise NotImplementedError("Should have implemented this")

    def recv(self, packet):
        """receive a network packet"""
        raise NotImplementedError("Should have implemented this")

    def send(self, packet):
        """send a network packet"""
        raise NotImplementedError("Should have implemented this")

    def log(self, message):
        """log a message"""
        self.__log.append(message)

    def getLog(self):
        """retrieve the firewall's log"""
        return self.__log

    @property
    def fwtype(self):
        """returns the firewall type"""
        return self.__type


class FwPlumbing(object):
    """Abstract firewall framework"""

    def __init__(self):
        """Constructor"""
        self.__rules = None
        self.__plumbing = None

    def getRules(self):
        """Get the rules"""
        return self.__rules

    def addRule(self):
        """add a rule"""
        raise NotImplementedError("Should have implemented this")

    def process(self, packet):
        """Process a packet"""
        raise NotImplementedError("Should have implemented this")
