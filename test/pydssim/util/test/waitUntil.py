"""
waitUntil.py

Prototype of a general 'waitUntil' interrogative scheduling facility for SimPy.

If introduced into SimPy, could be implemented as 'yield waitUntil,self,cond',
with cond being a predicate function returning True if the condition to be waited
for is satisfied. 'test' would be added to SimPy and would be called in event
loop in 'simulate' in Simulation and SimulationXXXX.

"""
from __future__ import generators
from SimPy.SimulationStep import *

def test():
    """
    Gets called by simulate after every event, as long as there are processes
    waiting in condQ for a condition to be satisfied.
    Tests the conditions for all waiting processes. Where condition satisfied,
    reactivates that process immediately and removes it from queue.
    """    
    global condQ
    rList=[]
    for el in condQ:
        if el.cond():
            rList.append(el)
            reactivate(el)
    for i in rList:
        condQ.remove(i)
    
    if not condQ:
        stopStepping()

def waitUntil(proc,cond):
    global condQ
    """
    Puts a process 'proc' waiting for a condition into a waiting queue.
    'cond' is a predicate function which returns True if the condition is
    satisfied.
    """    
    condQ.append(proc)
    proc.cond=cond
    startStepping()         #signal 'simulate' that a process is waiting

condQ=[]

