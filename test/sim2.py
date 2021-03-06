'''
Created on 28/08/2010

@author: Luiz Gustavo
'''
""" bank01: The single non-random Customer """           
""" bank03: Many non-random Customers """
from SimPy.Simulation import *

## Model components ------------------------

class Source(Process):                              
    """ Source generates customers regularly """

    def generate(self,number,TBA):                  
        for i in range(number):
            c = Customer(name = "Customer%02d"%(i,))
            activate(c,c.visit(timeInBank=12.0))
            yield hold,self,TBA                     

class Customer(Process):
    """ Customer arrives, looks around and leaves """
        
    def visit(self,timeInBank):       
        print "%7.4f %s: Here I am"%(now(),self.name)
        yield hold,self,timeInBank
        print "%7.4f %s: I must leave"%(now(),self.name)

## Experiment data -------------------------

maxNumber = 128
maxTime = 12800 # minutes                                    
ARRint = 10.0   # time between arrivals, minutes 

## Model/Experiment ------------------------------

initialize()
s = Source()                                             
activate(s,s.generate(number=maxNumber,                   
                      TBA=ARRint),at=0.0)             
simulate(until=maxTime)
