#!/usr/bin/env python
# Events.py

from SimPy.Simulation import *

class Event:
    """Class implementing named events==signals for synchronization of processes.
    Not to be confused with events as in discrete _event_ simulation!

    Provides for semaphores and also for mass-reactivation of processes after event.
    """
    def __init__(self,name):
        self.name=name
        self.waits=[]       #set of processes waiting for event
        self.queues=[]      #FIFO queue for processes waiting for semaphore
        self.occurred=False 
    def set(self):
        """Produces a signal;
        Set this event if no process waiting or queuing;
        reactivate all processes waiting for this event;
        reactivate first process in FIFO queue for this event
        """
        if not self.waits and not self.queues:
            self.occurred=True
        else:
            #schedule activation for all waiting processes
            for p in self.waits:
                reactivate(p)
            self.waits=[]
        if self.queues:
            #Activate first process in queue to enter critical section
            p=self.queues.pop(0)
            reactivate(p)

    def wait(self,proc):
        """Consumes a signal if it has been sent,
        else process 'proc' waits for this event.
        Return value indicates whether process has to wait.
        """
        if not self.occurred:
            self.waits.append(proc)
            return True
        else:
            self.occurred=False
            return False

    def queue(self,proc):
        """Consumes a signal if it has been sent;
        else process 'proc' queues for this event
        Return value indicates whether process has to queue.
        """
        if not self.occurred:
            self.queues.append(proc)
            return True
        else:
            self.occurred=False
            return False

if __name__=="__main__":

##Pavlov's dogs
    class BellMan(Process):
        def ring(self):
            while True:
                bell.set()
                print "%s %s rings bell"%(now(),self.name)
                yield hold,self,5

    class PavlovDog(Process):
        def behave(self):
            while True:
                if bell.wait(self):
                    yield passivate,self
                    print "%s %s drools"%(now(),self.name)

    initialize()
    bell=Event("bell")
    for i in range(4):
        p=PavlovDog("Dog %s"%(i+1))
        activate(p,p.behave())
    b=BellMan("Pavlov")
    activate(b,b.ring())
    print "\n Pavlov's dogs"
    simulate(until=10)
    
##PERT simulation
    class Activity(Process):
        def __init__(self,name):
            Process.__init__(self,name)
            self.event=Event("completion of %s"%self.name)
            allEvents.append(self.event)
        def perform(self):
            yield hold,self,random.randint(1,100)
            self.event.set()
            print "%s Event '%s' fired"%(now(),self.event.name)

    class TotalJob(Process):
        def perform(self,allEvents):
            for e in allEvents:
                if e.wait(self):
                    yield passivate,self
            # not waiting for any events anymore -- all events were set
            print now(),"All done"
    import random
    initialize()
    allEvents=[]
    for i in range(10):
        a=Activity("Activity %s"%(i+1))
        activate(a,a.perform())
    t=TotalJob()
    activate(t,t.perform(allEvents))
    print "\n PERT network simulation"
    simulate(until=100)

#Semaphore/critical section
    class Car(Process):
        def drive(self):
            if intersectionFree.queue(self): #does process have to queue for intersection?
                # yes; process has been queued
                print "%s %s waiting to enter intersection"%(now(),self.name)
                yield passivate,self     #Process waiting in queue
                # process out of queue
            # Intersection free, enter  . . 
            ### Begin Critical Section
            yield hold,self,1            #drive across
            print "%s %s crossed intersection"%(now(),self.name)
            ### End Critical Section
            intersectionFree.set()

    initialize()
    intersectionFree=Event("Intersection")
    intersectionFree.set()
    arrtime=0.0
    for i in range(20):
        c=Car("Car %s"%(i+1))
        activate(c,c.drive(),at=arrtime)
        arrtime+=0.2
    print "\n Critical section/semaphore"
    simulate(until=100)
                       