#-------------------------------------------------------------------------------
# Name:        aBank_Recipe001.py
# Scenario:    Customers visit a bank and get service one of a number of counters.
#              The load on the counters is to be determined.
# Model:       The counters are modeled as a Resource for which visitors have to queue.
#
# Author:      Klaus Muller
#
# Created:     2009-09-05
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from random import *
## Model components ------------------------------------------------------------
from SimPy.Simulation import *

class Visitor(Process):
    def visit(self,counter,tService):
        yield request,self,counter
        yield hold,self,tService
        yield release,self,counter
        
class VisitorGenerator(Process):
     def generate(self,counter,serveRate,arriveRate):
         while True:
            v = Visitor()
            tServe = expovariate(serveRate)
            activate(v,v.visit(counter=counter,tService=tServe))
            tArrival = expovariate(arriveRate)
            yield hold,self,tArrival 
         
## Model -----------------------------------------------------------------------
def bankModel(nrCounters,serveRate,arriveRate,endTime):
    counter = Resource(capacity=nrCounters,monitored=True)
    initialize()
    vg = VisitorGenerator()
    activate(vg,vg.generate(counter=counter,serveRate=serveRate,arriveRate=arriveRate))
    simulate(until=endTime)
    return counter

def main():
    ## Experiment data ---------------------------------------------------------
    nrCounters = 2
    sRate = 10       # customers per hour get served at acounter
    aRate = 8       # customers per hour arrive at bank
    runTime = 100    # hours simulation time
    seed(1237)
    ## Experiment --------------------------------------------------------------
    moni = bankModel(nrCounters=nrCounters,serveRate=sRate,arriveRate=aRate,endTime=runTime)
    ## Analysis ----------------------------------------------------------------
    data = moni.waitMon
    averageQ = data.timeAverage()
    maxQ = max(data.yseries())
    ## Output ------------------------------------------------------------------
    print """
    The time-averaged counter queue length was %3.1f.
    The maximum counter length was %s.
    """%(averageQ, maxQ)
    
if __name__ == '__main__':
    main()
