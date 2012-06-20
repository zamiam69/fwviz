'''
Created on May 22, 2012

@author: maz
'''

class FwCommand(object):
    """Abstract Command class"""

    def __init__(self):
        """Constructor, override this"""
        pass

    def execute(self):
        """override this"""
        pass


class IptablesCmd(FwCommand):
    """iptables command pattern"""

    def __init__(self, firewall):
        FwCommand.__init__(self)
        self.__firewall = firewall

    def execute(self, args):
        pass
