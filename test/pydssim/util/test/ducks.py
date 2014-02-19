'''
Created on Jul 2, 2009

@author: Robert Dickenson
'''

from SimPy.Simulation import *
from random import random

class Quack( Process ):
    def __init__( self, owner, simInstance ):
        Process.__init__( self, simInstance )
        self.owner = owner
        self.sim = simInstance
    def quack( self ):
        while True:
#            print "%s %s quacks" % ( self.sim.now(), self.owner.name )
            yield hold, self, random()*10

class Fly( Process ):
    def __init__( self, owner, simInstance ):
        Process.__init__( self, simInstance )
        self.owner = owner
        self.sim = simInstance
    def fly( self ):
        while True:
#            print "%s %s flies" % ( self.sim.now(), self.owner.name )
            yield hold, self, random()*10

class Duck:
    def __init__( self, name , simInstance ):
        self.name = name
        self.quack = Quack( self, simInstance )
        simInstance.activate( self.quack, self.quack.quack() )
        self.fly = Fly( self , simInstance )
        self.sim = simInstance
        simInstance.activate( self.fly, self.fly.fly() )
    def aim_at( self, accuracy_decile ):
        rand_decile = int( random()*10 )
        if accuracy_decile > rand_decile:
            print "%10.2f" % ( self.sim.now() ), self.name, "says'.................Oh NOES !........I am a shot duck'"
            Process().cancel( self.quack )
            print "%10.2f" % ( self.sim.now() ), self.name, "says'............................I cannot quack anymore'"
            Process().cancel( self.fly )
            print "%10.2f" % ( self.sim.now() ), self.name, "says'..............................I cannot fly anymore'"
            return True
        else:
            print "%10.2f" % ( self.sim.now() ), self.name, "says'          ....Whew !  he missed me that time......'"
            return False
    def escape( self ):
        # called when hunter gives up on this duck
        print "%10.2f" % ( self.sim.now() ), self.name, "says'':-) :-) ....I totally escaped the hunter......:-) :-)'"
        Process().cancel( self.quack )
        Process().cancel( self.fly )

class Hunter( Process ):
    def __init__( self, name , ammo, accuracy, switch_target, duckflock, simInstance ):
        Process.__init__( self, name, simInstance )
        self.name = name
        self.sim = simInstance
        self.ammo = ammo
        self.duckflock = duckflock
        #accuracy is number of times out of 10 tries that hunter hits target on average
        self.accuracy = accuracy
        #switch_target is number of shots a hunter will/gets to take at a particular target duck
        self.switch_target = switch_target
        print "hunter is ", self.name
        print self.name, "has ", self.ammo, "shells"

    def shoot( self ):
        self.ducks_bagged = 0
        self.shots_taken = 0
        while self.ammo > 0:
            if self.duckflock.nrBuffered > 0 :
                yield get, self, self.duckflock, 1
                target = self.got
                print "%10.2f" % ( self.sim.now() ), self.name, " has targeted:", target[0].name
                shots_at_target = 0
                while ( self.ammo > 0 and ( shots_at_target <= self.switch_target ) ):
                    yield hold, self, random()*500
                    print "%10.2f %s the hunter is shooting at %s" % ( self.sim.now(), self.name , target[0].name )
                    self.ammo = self.ammo - 1
                    self.shots_taken = self.shots_taken + 1
                    shots_at_target = shots_at_target + 1
                    print "%10.2f" % ( self.sim.now() ), self.name , " has ", self.ammo, "ammo rounds left ",
                    print " after taking: ", shots_at_target, "shots at target:", target[0].name
                    if target[0].aim_at( self.accuracy ):
                        print "%10.2f %s the hunter has killed %s" % ( self.sim.now(), self.name , target[0].name )
                        self.ducks_bagged = self.ducks_bagged + 1
                        break
                    else:
                        print "%10.2f" % ( self.sim.now() ), self.name, "says'  Darn !   missed him'"
                        if shots_at_target > self.switch_target:
                            print "%10.2f" % ( self.sim.now() ), self.name, "says'  Giving up on that one.......'"
                            target[0].escape()
                    print "%10.2f" % ( self.sim.now() ), self.name, "has taken ", self.shots_taken, " shots and gotten ", self.ducks_bagged, "ducks.  Percent: ", ( 100.0 * self.ducks_bagged / self.shots_taken )
            else:
                print "%10.2f" % ( self.sim.now() ), self.name, "says' I don't see any ducks......waiting for more'"
                yield hold, self, random()*1000
        print "%10.2f" % ( self.sim.now() ), self.name, "says'  and I'm out of ammo..........'"
        print "%10.2f" % ( self.sim.now() ), self.name, " ................I think I'll go home now...."
        print "%10.2f" % ( self.sim.now() ), self.name, "took ", self.shots_taken, " shots and got ", self.ducks_bagged, "ducks.  Percent: ", ( 100.0 * self.ducks_bagged / self.shots_taken )
        exit()

class DuckFlock( Store ):
    def __init__( self, name, cap, unitname, initial, simInstance ):
        Store.__init__( self,
                           name = name,
                           capacity = cap,
                           unitName = unitname,
                           initialBuffered = initial,
                           monitored = True,
                           monitorType = Monitor,
                           sim = simInstance )

class DuckFactory( Process ):
    def __init__( self, name , finish, maxducks, duckflock, simInstance ):
        Process.__init__( self, name, simInstance )
        self.sim = simInstance
        self.maxducks = maxducks
        self.duck_number = 0
        self.duckflock = duckflock
        self.finish = finish

    def execute( self ):

        while ( ( self.sim.now() < self.finish ) and ( self.duck_number < self.maxducks ) ):
            self.duck_number = self.duck_number + 1
            duck_name = "Duck_" + str( self.duck_number )
            print "%10.2f" % ( self.sim.now() ), "making Duck:", duck_name
            self.name = duck_name
            d = Duck( duck_name, self.sim )
            yield hold, self, random()*2000
       
            
              #colocar na redde
          
            yield put, self, self.duckflock, [d]



if __name__ == '__main__':

    simUntil = 50000
    hunter_ammo = 180
    hunter_accuracy_decile = 5 # municao
    hunter_switch_target = 2
    mySim = Simulation()
    myDuckFlock = DuckFlock( "Duck Flock", "unbounded", "ducks", None, mySim )
    myDuckFactory = DuckFactory( "My Duck Factory", simUntil, 200, myDuckFlock, mySim )
    mySim.activate( myDuckFactory, myDuckFactory.execute() )
    h = Hunter( "Fred", hunter_ammo, hunter_accuracy_decile, hunter_switch_target, myDuckFlock, mySim )
    k = Hunter( "Dave", 180, 4, 4, myDuckFlock, mySim )
    mySim.activate( h, h.shoot() )
    mySim.activate( k, k.shoot() )
    mySim.simulate( until = simUntil )
 

