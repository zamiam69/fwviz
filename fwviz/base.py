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
        self.__args = args
        self.__kwargs = kwargs

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
    def args(self):
        return self.__args

    @property
    def kwargs(self):
        return self.__kwargs

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

    def notify(self, event):
        """notify reporters/colleagues of a change"""
        try:
            for c in self._colleagues[event]:
                if c == event.reporter:
                    continue
                c.onEvent(event)
        except KeyError:
            raise NotImplementedError("Unknown event '{0}'.".format(event))

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

    def report(self, event):
        """Report an event to the mediator"""
        if self.mediator:
            self.__mediator.notify(self, event)

    def onEvent(self, event):
        """Called by the Mediator"""
        if self.__mediator:
            raise NotImplementedError("Should have implemented this")
        else:
            pass

class FwMediatedList(MutableSequence, FwColleague):
    """A list that reports changes to a mediator"""

    def __init__(self, mediator, data=None, eventgroup="list"):
        """Constructor"""
        FwColleague.__init__(self, mediator)
        self._data = []
        self._eventgroup = eventgroup
        if data is not None:
            if type(data) == type(self._data):
                # shallow copy!
                self._data[:] = data
            elif isinstance(data, FwMediatedList):
                self._data[:] = data.data[:]
            else:
                self._data[:] = list(data)
            self.report(self._eventgroup + "Add", data)

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
        self.report(self._eventgroup + "Change", index, value)

    def __delitem__(self, index):
        del(self._data[index])
        self.report(self._eventgroup + "Del", index)

    def __iadd__(self, values):
        self._data.__iadd__(values)
        self.report(self._eventgroup + "Add", values)

    def append(self, value):
        self._data.append(value)
        self.report(self._eventgroup + "Add", value)

    def extend(self, values):
        self._data.extend(values)
        self.report(self._eventgroup + "Add", values)

    def remove(self, value):
        self._data.remove(value)
        self.report(self._eventgroup + "Del", value)

    def insert(self, index, value):
        self._data.insert(index, value)
        self.report(self._eventgroup + "Add", index, value)

    def pop(self, index= -1):
        x = self._data.pop(index)
        self.report(self._eventgroup + "Del", index)
        return x
