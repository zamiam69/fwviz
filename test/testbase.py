"""
Created on Jun 19, 2012

@author: maz

Unit test for fwviz.base"""

from fwviz.base import FwColleague, FwMediator, FwMediatedList, FwEventFactory

class TColleague(FwColleague):

    def __init__(self, mediator=None, eventgroup="TestEvents"):
        super(TColleague, self).__init__(mediator, eventgroup)
        self.myevent = 0

    def onEvent(self, event, *args, **kwargs):
        self.myevent = self.myevent + 1
        print "I received event #{0}: {1}.".format(self.myevent, event)
        
        
class TestMediator:
    """test the mediator class"""
    def testEvent(self):
        reporter = None
        action = "Add"
        kwargs = {'foo': 'bar', 'baz': 'bla'}
        E = FwEventFactory(reporter, action, **kwargs)
        assert E.reporter == reporter
        assert E.action == action
        assert E.kwargs == kwargs

    def testMediator(self):
        M = FwMediator()
        
        eventgroup = "testEvents"
        C1 = TColleague(M, eventgroup)
        C2 = TColleague(M, eventgroup)
        assert C1.mediator == M and C2.mediator == M
        
        M.register(C1, eventgroup, "Add", "Change", "Del")
        M.register(C2, eventgroup, "Add", "Del")
        
        E1 = FwEventFactory(C1, "Add")
        E2 = FwEventFactory(C1, "Change") 
        assert E1.eventgroup == eventgroup and E2.eventgroup == eventgroup

        C1.report(E1)
        assert C2.myevent == 1 and C1.myevent == 0
        
        # C2 isn't registred for "Change" actions
        C1.report(E2)
        assert C2.myevent == 1 and C1.myevent == 0
       
        # register another event 
        M.register(C2, eventgroup, "Change")
        C1.report(E2)
        assert C2.myevent == 2 and C1.myevent == 0
        
        # unregister from all events
        M.unregister(C2, eventgroup, "Add", "Change")
        C1.report(E1)
        C1.report(E2)
        assert C2.myevent == 2 and C1.myevent == 0
        

class TestMediatedList:

    def testMediatedList(self):
        M = FwMediator()
        C = TColleague(M, "tlist")
        
        M.register(C, "tlist", "Change", "Add", "Del")

        initlist = ["foo", "bar"]

        # initialisation
        ops = 1
        L = FwMediatedList(M, "tlist", initlist)
        for x in initlist:
            assert x in L
        assert C.myevent == ops
        assert len(L) == len(initlist)

        # append
        ops = ops + 1
        L.append("baz")
        assert C.myevent == ops
        assert "baz" in L
        assert len(L) == len(initlist) + 1

        # remove
        ops = ops + 1
        L.remove("foo")
        assert "foo" not in L
        assert len(L) == len(initlist)
        assert C.myevent == ops

        # insert
        ops = ops + 1
        L.insert(1, "foo")
        assert L[1] == "foo"
        assert C.myevent == ops
        assert len(L) == len(initlist) + 1

        # pop
        ops = ops + 1
        x = L.pop()
        assert x == "baz"
        assert C.myevent == ops
        assert len(L) == len(initlist)

        # extend
        ops = ops + 1
        add = ["bla", "fasel"]
        L.extend(add)
        assert C.myevent == ops
        for x in add:
            assert x in L
        assert len(L) == len(initlist) + len(add)

        # setitem
        ops = ops + 1
        L[1] = "FOO"
        assert C.myevent == ops
        assert "FOO" in L
        assert "foo" not in L
        assert len(L) == len(initlist) + len(add)
