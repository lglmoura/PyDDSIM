'''
Created on 25/09/2009

@author: LGustavo
'''

__doc__="""
Scenario/Purpose:
To show use of multiple resource units fom multiple resources.
"""
from SimPy.Simulation import *

###########################################################################
### Model components (classes, functions) 
###########################################################################
class User(Process):
    def __init__(self,name,priority):
        Process.__init__(self,name)
        self.priority=priority
    def use(self):
        needA=2
        needB=4
        processTime=5
        def availableA():
            return resA.n>=needA
        def availableB():
            return resB.n>=needB
        while True:
            if availableA():
                yield request,self,semaphoreA ## begin atomic transaction
                for i in range(needA):
                    assert resA.n>0,"Process %s requesting non-available unit at %s"%(self.name,now())
                    yield request,self,resA,self.priority
                yield release,self,semaphoreA ## end atomic transaction
                break
            else:
                yield waituntil,self,availableA
        while True:
            if availableB():
                yield request,self,semaphoreB ## begin atomic transaction
                for i in range(needB):
                    yield request,self,resB,self.priority
                yield release,self,semaphoreB ## end atomic transaction
                break
            else:
                yield waituntil,self,availableB
        ## user now has resources which he needs 
        yield hold,self,processTime
        for i in range(needB):
            yield release,self,resB
        for i in range(needA):
            yield release,self,resA
        print "%s: User %s finished"%(now(),self.name)

initialize()
resA=Resource(capacity=5,name="Resource A")
semaphoreA=Resource(capacity=1,name="SemaphoreA")
resB=Resource(capacity=10,name="Resource B")
semaphoreB=Resource(capacity=1,name="SemaphoreB")
resB
for i in range(10):
    u=User(name=i,priority=i)
    activate(u,u.use())
simulate(until=1000)