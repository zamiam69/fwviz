"""
Created on May 30, 2012

@author: maz
"""

from collections import MutableSequence

class FwEvent(object):
    """Event class, passed between colleagues"""
    def __init__(self, reporter, action, **kwargs):
        self.__reporter = reporter
        self.__action = action
        self.__kwargs = kwargs
        
    def __str__(self):
        return self.__reporter.eventgroup + self.__action
        
    @property
    def reporter(self):
        return self.__reporter

    @property
    def eventgroup(self):
        return self.__reporter.eventgroup

    @property
    def action(self):
        return self.__action

    @property
    def kwargs(self):
        return self.__kwargs
    
class FwEventFactory(object):
    """Factory for an FwEvent"""
    def __new__(cls, reporter, action, **kwargs):
        return FwEvent(reporter, action, **kwargs)

class FwMediator(object):
    """Abstract mediator class"""
    def __init__(self):
        """Constructor"""
        super(FwMediator, self).__init__()
        self._colleagues = {}

    def register(self, colleague, eventgroup, *actions):
        """register a reporter/colleague"""
        if eventgroup not in self._colleagues:
            self._colleagues[eventgroup] = {}
            
        for a in actions:
            if a not in self._colleagues[eventgroup]:
                self._colleagues[eventgroup][a] = []
            self._colleagues[eventgroup][a].append(colleague)
        
    def unregister(self, colleague, eventgroup, *actions):
        """unregister a reporter/colleague"""
        if eventgroup not in self._colleagues:
            return
        
        for a in actions:
            self._colleagues[eventgroup][a].remove(colleague)

    def notify(self, event):
        """notify reporters/colleagues of a change"""
        try:
            for c in self._colleagues[event.eventgroup][event.action]:
                if c == event.reporter:
                    continue
                c.onEvent(event)
        except KeyError:
            raise NotImplementedError("Unknown event '{0}'.".format(event))

class FwColleague(object):
    """Abstract reporter class"""
    def __init__(self, mediator=None, eventgroup="colleague"):
        """Constructor"""
        super(FwColleague, self).__init__()
        self.__mediator = mediator
        self.__eventgroup = eventgroup

    @property
    def mediator(self):
        """getter for the mediator"""
        return self.__mediator

    @mediator.setter
    def mediator(self, mediator):
        """setter method"""
        self.__mediator = mediator
        
    @property
    def eventgroup(self):
        """getter"""
        return self.__eventgroup

    def report(self, event):
        """Report an event to the mediator"""
        if self.mediator:
            self.__mediator.notify(event)

    def onEvent(self, event):
        """Called by the Mediator"""
        if self.__mediator:
            raise NotImplementedError("Should have implemented this")
        else:
            pass

class FwMediatedList(MutableSequence, FwColleague):
    """A list that reports changes to a mediator"""

    def __init__(self, mediator, eventgroup="list", data=None):
        """Constructor"""
        FwColleague.__init__(self, mediator, eventgroup)
        self._data = []
        if data is not None:
            if type(data) == type(self._data):
                # shallow copy!
                self._data[:] = data
            elif isinstance(data, FwMediatedList):
                self._data[:] = data.data[:]
            else:
                self._data[:] = list(data)
            event = FwEventFactory(self, "Add", data=self.data)
            self.report(event)

    @property
    def data(self):
        "getter"
        return self._data

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return self._data

    def __eq__(self, other):
        if isinstance(other, FwMediatedList):
            return self._data == other.data
        else:
            return self._data == other

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)

    def __setitem__(self, index, value):
        self._data[index] = value
        event = FwEventFactory(self, "Change", data=self.data)
        self.report(self._eventgroup + "Change", index=index, value=value)
        self.report(event)

    def __delitem__(self, index):
        del(self._data[index])
        event = FwEventFactory(self, "Del", index=index)
        self.report(event)

    def __iadd__(self, values):
        self._data.__iadd__(values)
        event = FwEventFactory(self, "Add", values=values)
        self.report(event)

    def append(self, value):
        self._data.append(value)
        event = FwEventFactory(self, "Add", value=value)
        self.report(event)

    def extend(self, values):
        self._data.extend(values)
        event = FwEventFactory(self, "Add", values=values)
        self.report(event)

    def remove(self, value):
        self._data.remove(value)
        event = FwEventFactory(self, "Del", value=value)
        self.report(event)

    def insert(self, index, value):
        self._data.insert(index, value)
        event = FwEventFactory(self, "Add", index=index, value=value)
        self.report(event)

    def pop(self, index= -1):
        x = self._data.pop(index)
        event = FwEventFactory(self, "Del", index=index)
        self.report(event)
        return x