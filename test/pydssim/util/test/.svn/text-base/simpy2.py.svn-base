'''
Created on 25/09/2009

@author: LGustavo
'''

#!/usr/bin/env python
"""
  Simulation of a jackson queue network

"""
#from __future__ import generators  # not needed in Python 2.3+
from SimPy.Simulation import *
from random import Random,expovariate,uniform

def sum(P):
    """ Sum of the real vector P """
    sumP = 0.0
    for i in range(len(P)): sumP += P[i]
    return (sumP)



def choose2dA(i,P,g):
    """  return a random choice from a set j = 0..n-1
       with probs held in list of lists P[j] (n by n)
       using row i
       g = random variable
       call:  next = choose2d(i,P,g)
    """
    U = g.random()
    sumP = 0.0
    for j in range(len(P[i])):  # j = 0..n-1
        sumP +=  P[i][j]
        if U < sumP: break
    return(j)

## -----------------------------------------------
class Msg(Process):
    """a message"""
    def __init__(self,i,node):
        Process.__init__(self)
        self.i = i
        self.node = node

    def execute(self):
        """ executing a message """
        global noInSystem
        startTime = now()
        noInSystem += 1
        ##print "DEBUG noInSystm = ",noInSystem
        NoInSystem.accum(noInSystem)
        self.trace("Arrived node  %d"%(self.node,))
        while self.node <> 3:
            yield request,self,processor[self.node]
            self.trace("Got processor %d"%(self.node,))
            st = Mrv.expovariate(1.0/mean[self.node])
            Stime.observe(st)
            yield hold,self,st
            yield release,self,processor[self.node]
            self.trace("Finished with %d"%(self.node,))
            self.node = choose2dA(self.node,P,Mrv)
            self.trace("Transfer to   %d"%(self.node,))
        TimeInSystem.observe(now()-startTime)
        self.trace(    "leaving       %d"%(self.node,),noInSystem)
        noInSystem -= 1
        NoInSystem.accum(noInSystem)

    def trace(self,message,nn=0):
        if MTRACING: print "MSG %7.4f %3d %10s %3d"%(now(),self.i, message,nn)


## -----------------------------------------------
class Generator(Process):
 """ generates a sequence of msgs """
 def __init__(self, rate,maxT,maxN):
     Process.__init__(self)
     self.name = "Generator"
     self.rate = rate
     self.maxN = maxN
     self.maxT = maxT
     self.g = Random(11335577)
     self.i = 0

 def execute(self):
     while (now() < self.maxT)  & (self.i < self.maxN):
         self.i+=1
         p = Msg(self.i,startNode)
         activate(p,p.execute())
         ## self.trace("starting "+p.name)
         yield hold,self,self.g.expovariate(self.rate)
     self.trace("generator finished with "+`self.i`+" ========")
     self.stopSim()

 def trace(self,message):
     if GTRACING: print "Generator %7.4f \t%s"%(now(), message)

## -----------------------------------------------
# generator:
GTRACING = 0
# messages:
rate = 0.5
noInSystem = 0
MTRACING = 1
startNode = 0
maxNumber = 10000
maxTime = 100000.0
Mrv = Random(77777)
TimeInSystem=Monitor()
NoInSystem= Monitor()
Stime = Monitor()

processor = [Resource(1),Resource(1),Resource(1)]
mean=[1.0, 2.0, 1.0]
P = [[0, 0.5, 0.5, 0],[0,0,0.8,0.2], [0.2,0,0,0.8]]

initialize()
g = Generator(rate,maxTime,maxNumber)
activate(g,g.execute())
simulate(until=100.0)

print "Mean numberm= %8.4f"%(NoInSystem.timeAverage(),)
print "Mean delay  = %8.4f"%(TimeInSystem.mean(),)
print "Mean stime  = %8.4f"%(Stime.mean(),)
print "Total jobs  = %8d"%(TimeInSystem.count(),)
print "Total time  = %8.4f"%(now(),)
print "Mean rate   = %8.4f"%(TimeInSystem.count()/now(),)