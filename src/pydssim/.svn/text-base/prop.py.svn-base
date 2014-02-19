'''
Created on 19/10/2009

@author: LGustavo
'''

class PropertiesExample(object):
    def __init__(self):
        self.value = 0
 
    def setx(self, value):
        x = value * 2
 
    def getx(self):
        return self.value
 
    x = property(getx, setx)
 
    def geta(self):
        x +=1 
 
if __name__ == "__main__":
    p = PropertiesExample()
    print p.x   # mostra "0"
    p.x = 3     # "x"  uma propriedade, e  um atributo
    p.geta()
    print p.x   # mostra "6"