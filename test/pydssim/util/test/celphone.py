'''
Created on 28/09/2009

@author: LGustavo
'''
from SimPy.Simulation import *
from random import Random,expovariate

class Generator(Process):
 """ generates a sequence of calls """
 def __init__(self, maxN, lam):
     global busyEndTime
     Process.__init__(self)
     self.name = "generator"
     self.maxN = maxN
     self.lam = lam
     self.iatime = 1.0/lam
     self.rv = Random(gSeed)
     busyEndTime = now() # simulation start time

 def execute(self):
     for i in range(self.maxN):
         j = Job(i)
         activate(j,j.execute())
         yield hold,self,self.rv.expovariate(lam)
     self.trace("WARNING generator finished -- ran out of jobs")

 def trace(self,message):
     if GTRACING: print "%7.4f \t%s"%(self.time(), message)


class Job(Process):
    """ instances of the Job class represent calls arriving at
    random at the chnnels.
    """
    def __init__(self,i):
        Process.__init__(self)
        self.i = i
        self.name = "Job"+`i`

    def execute(self):
        global busyStartTime,totalBusyVisits,totalBusyTime
        global Nfree,busyEndTime,Jrv
        self.trace("arrived ")
        if Nfree == 0: self.trace("blocked and left")
        else:
             self.trace("got a channel")
             Nfree -=  1
             if Nfree == 0:
                 self.trace("start busy period======")
                 busyStartTime = now()
                 totalBusyVisits += 1
                 interIdleTime = now() - busyEndTime
             yield hold,self,Jrv.expovariate(mu)
             self.trace("finished")
             if Nfree == 0:
                 self.trace("end   busy period++++++")
                 busyEndTime = now()
                 busy = now() - busyStartTime
                 self.trace("         busy  = %9.4f"%(busy,))
                 totalBusyTime +=busy
             Nfree += 1

    def trace(self,message):
         if TRACING: print "%7.4f \t%s %s "%(now(), message , self.name)


class Statistician(Process):
     """ observes the system at intervals """
     def __init__(self,Nhours,interv,gap):
         Process.__init__(self)
         self.Nhours = Nhours
         self.interv = interv
         self.gap = gap
         self.name="Statistician"

     def execute(self):
         global busyStartTime,totalBusyTime,totalBusyVisits
         global hourBusyTime,hourBusyVisits
         for i in range(self.Nhours):
             yield hold,self,self.gap
             totalBusyTime = 0.0
             totalBusyVisits = 0
             if Nfree == 0: busyStartTime = now()
             yield hold,self,self.interv
             if Nfree == 0: totalBusyTime += now()-busyStartTime
             if STRACING:  print "%7.3f %5d"%(totalBusyTime,totalBusyVisits)
             m.tally(totalBusyTime)
             bn.tally(totalBusyVisits)
         print("Busy Time:   mean = %10.5f var= %10.5f"%(m.mean(),m.var()))
         print("Busy Number: mean = %10.5f var= %10.5f"%(bn.mean(),bn.var()))


     def trace(self,message):
         if STRACING: print "%7.4f \t%s"%(self.time(), message)

totalBusyVisits = 0
totalBusyTime   = 0.0
NChannels =  4  # number of channels in the cell
Nfree   = NChannels
maxN    = 1000
gSeed   = 11111111
JrvSeed = 3333333
lam = 1.0
mu = 0.6667
meanLifeTime = 1.0/mu
TRACING  = 0
GTRACING = 0
STRACING = 1
Nhours  =  10
interv = 60.0    # monitor
gap    = 15.0    # monitor
print "lambda    mu      s  Nhours interv  gap"
print "%7.4f %6.4f %4d %4d    %6.2f %6.2f"%(lam,mu,NChannels,Nhours,interv,gap)

m = Monitor()
bn=Monitor()
Jrv = Random(JrvSeed)
s = Statistician(Nhours,interv,gap)
initialize()
g = Generator(maxN, lam)
activate(g,g.execute())
activate(s,s.execute())
simulate(until=10000.0)