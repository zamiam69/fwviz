"""
Created on Jun 19, 2012

@author: maz

Unit test for fwviz.base"""

from fwviz.base import FwColleague, FwMediator, FwMediatedList, FwEventFactory

class TColleague(FwColleague):

    def __init__(self, mediator=None):
        super(TColleague, self).__init__(mediator)
        self.myevent = 0

    def onEvent(self, event, *args, **kwargs):
        self.myevent = self.myevent + 1
        print "I received event #{0}: {1}.".format(self.myevent, event)



class TestMediator:
    """test the mediator class"""

    def testMediator(self):
        M = FwMediator()
        C1 = TColleague(M, "my")
        C2 = TColleague(M, "my")

        M.register(C1, "my", "Event")
        M.register(C2, "my", "Event")

        E = FwEventFactory(C1, )
        C1.report("my", "Event")
        assert C2.myevent == 1
        assert C1.myevent == 0

        # C1.report("unregisteredEvent")
        C2.report("my", "Event")
        assert C2.myevent == 1
        assert C1.myevent == 1

        M.unregister(C2, "my", "Event")
        C1.report("my", "Event")
        assert C2.myevent == 1
        assert C1.myevent == 1

class TestMediatedList:

    def testMediatedList(self):
        M = FwMediator()
        C = TColleague(M)
        M.register(C, "tlist", "Change", "Add", "Del")

        initlist = ["foo", "bar"]

        # initialisation
        ops = 1
        L = FwMediatedList(M, initlist, "tlist")
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
