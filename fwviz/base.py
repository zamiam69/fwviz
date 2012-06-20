"""
Created on May 30, 2012

@author: maz
"""

from collections import MutableSequence

class FwMediator(object):
    """Abstract mediator class"""

    def __init__(self):
        """Constructor"""
        super(FwMediator, self).__init__()
        self._colleagues = {}

    def register(self, colleague, event):
        """register a reporter/colleague"""
        if event and event not in self._colleagues.keys():
            self._colleagues[event] = []
        if event:
            self._colleagues[event].append(colleague)

    def unregister(self, colleague, event):
        """unregister a reporter/colleague"""
        self._colleagues[event].remove(colleague)

    def notify(self, reporter, event, *args, **kwargs):
        """notify reporters/colleagues of a change"""
        for c in self._colleagues[event]:
            if c == reporter:
                continue
            c.onEvent(event, args, kwargs)

class FwColleague(object):
    """Abstract reporter class"""
    def __init__(self, mediator=None):
        """Constructor"""
        super(FwColleague, self).__init__()
        self.__mediator = mediator

    @property
    def mediator(self):
        """getter for the mediator"""
        return self.__mediator

    @mediator.setter
    def mediator(self, mediator):
        """setter method"""
        self.__mediator = mediator

    def report(self, event, *args, **kwargs):
        """Report an event to the mediator"""
        if self.mediator:
            self.__mediator.notify(self, event, args, kwargs)

    def onEvent(self, event, *args, **kwargs):
        """Called by the Mediator"""
        if self.__mediator:
            raise NotImplementedError("Should have implemented this")
        else:
            pass

class FwMediatedList(MutableSequence, FwColleague):
    """A list that reports changes to a mediator"""

    def __init__(self, mapping, mediator, eventprefix="list"):
        """Constructor"""
        self._eventprefix = eventprefix
        FwColleague.__init__(self, mediator)
        super(MutableSequence, self).__init__(mapping)

    def __setitem__(self, index, value):
        super(FwMediatedList, self).__setitem__(index, value)
        self.report(self._eventprefix + "Change", index, value)

    def __delitem__(self, index):
        super(FwMediatedList, self).__setitem__(index)
        self.report(self._eventprefix + "Del", index)

    def __iadd__(self, values):
        super(FwMediatedList, self).__iadd__(values)
        self.report(self._eventprefix + "Add", values)

    def append(self, value):
        super(FwMediatedList, self).append(value)
        self.report(self._eventprefix + "Add", value)

    def extend(self, values):
        super(FwMediatedList, self).extend(values)
        self.report(self._eventprefix + "Add", values)

    def remove(self, value):
        super(FwMediatedList, self).remove(value)
        self.report(self._eventprefix + "Del", value)

    def insert(self, index, value):
        super(FwMediatedList, self).insert(index, value)
        self.report(self._eventprefix + "Add", index, value)

    def pop(self, index= -1):
        super(FwMediatedList, self).pop(index)
        self.report(self._eventprefix + "Del", index)
