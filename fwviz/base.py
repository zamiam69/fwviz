"""
Created on May 30, 2012

@author: maz
"""

class ObsSubject(object):
    """Observer subject
    
    http://code.activestate.com/recipes/131499-observer-pattern/
    """

    def __init__(self):
        """Constructor"""
        self.__observers = []

    def attach(self, observer):
        """add an observer"""
        if not observer in self.__observers:
            self.__observers.append(observer)

    def detach(self, observer):
        """remove an observer"""
        try:
            self.__observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        """notify the other observers"""
        for o in self.__observers:
            if o == modifier:
                continue
            o.update(self)


class FwMediator(object):
    """Abstract mediator class"""

    def __init__(self):
        """Constructor"""
        super(FwMediator, self).__init__()
        self.__colleagues = None

    def register(self, colleague, event):
        """register a reporter/colleague"""
        self.__colleagues[event].append(colleague)

    def unregister(self, colleague, event):
        """unregister a reporter/colleague"""
        self.__colleagues[event].remove(colleague)

    def notify(self, reporter, event, *args, **kwargs):
        """notify reporters/colleagues of a change"""
        for c in self.__colleagues[event]:
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

