'''
Created on 26/09/2009

@author: LGustavo
'''

from priorityQueue import PriorityQueue


class Sim:
    def __init__(self):
        self.q = PriorityQueue()
        self.time = 100
        self.nodes = {}
        self.actors = []
        self.done = False

    def add_actor(self, actor):
        actor.sim = self
        self.actors.append(actor)

    def at(self, event):
        if event.time < self.time:
            print "ERROR, time warp"
        else:
            self.q.put(event, event.time)

    def process(self):
        while not self.q.empty():
            event = self.q.get()
            self.time = event.time
            try:
                (result, actor) = event.process(self)
                actor.send(result)
            except StopIteration:
                pass
        print "Sim done"

    def prime(self):
        for a in self.actors:
            a.prime()

    def go(self):
        self.prime()
        self.process()

class Actor:
    def ping(self, who):
        self.sim.at(Ping(self.sim.time + 5, self.this_pointer, who))

    def kill(self, who):
        self.sim.at(Kill(self.sim.time + 5, self.this_pointer, who))

    def wait(self, how_long):
        self.sim.at(Wait(self.sim.time + how_long, self.this_pointer))

    def __init__(self):
        """Somehow get everyone ready"""
        self.sim = None
        self.this_pointer = None

    def prime(self):
        g = self.go()
        g.next()
        g.send(g)

class Node:
    def __init__(self):
        self.status = "OK"

class Pinger(Actor):
    def go(self):
        self.this_pointer = (yield None)
        yield self.wait(100)
        success = True
        while success:
            result = (yield self.ping(ip))
            if result != "success":
                success = False
        print "Pinger done"

class Killer(Actor):
    def go(self):
        self.this_pointer = (yield None)
        yield self.wait(25)
        yield self.kill(ip)
        print "Killer done"

class Event:
    def __init__(self, time, actor):
        self.time = time
        self.actor = actor

    def process(self, sim):
        pass

class Wait(Event):
    def process(self, sim):
        return ("success", self.actor)

class Kill(Event):
    def __init__(self, time, actor, target):
        Event.__init__(self, time, actor)
        self.target = target

    def process(self, sim):
        if sim.nodes[self.target].status == "OK":
            sim.nodes[self.target].status = "DOWN"
            print "  kill SUCCESS"
        return ("success", self.actor)

class Ping(Event):
    def __init__(self, time, actor, target):
        Event.__init__(self, time, actor)
        self.target = target

    def process(self, sim):
        if sim.nodes[self.target].status == "OK":
            print "  ping"
            return ("success", self.actor)
        else:
            print "  ping FAIL"
            return ("failure", self.actor)


ip="200.222.17.90"


if __name__ == "__main__":
    s = Sim()
    n = Node()
    s.nodes[ip] = n
    s.add_actor(Killer())
    s.add_actor(Pinger())
    s.go()
