'''
Created on 20/04/2010

@author: Luiz Gustavo
'''
from datetime import datetime

if __name__ == '__main__':
    teste = {}
    teste["001"] = (10,"Danielle")
    teste["002"] = {}
    
    
    
    teste["002"][0] = (0,"leticia")
    teste["002"][1] = (10,"clara")
    teste["003"] = 0
    x,y = teste["002"][0]
    print teste
    print teste["002"].keys(), teste["002"].values()
    teste["002"][0] = (30,"Arhur") 
    print teste["002"].keys(), teste["002"].values()
  
    print ("003" in teste.keys() and (teste["003"] > 0))
    teste["003"] += 12
    print ("003" in teste.keys() and (teste["003"] > 0)), teste["003"]
    

    #print x,y
   
    data = "danielle_gustavo.amor"
    nome,senti = data.split(".")
    
    hoje = datetime.today()
    dia = hoje.strftime('%d%m%Y')
    print "%s-%s.%s"%(nome,dia,senti)
    equi = {}
    tame = 6
    
    
    '''
    
    
    for i in range(1,tame+1):
        equi[i] = {}
        for z in range(i+1,tame+1):
            equi[i][z]= "%s-%s"%(i,z)
        print i, "  --  ",equi[i]
    #print equi
    
    ser = equi.values()
    print equi
   
   '''
    
   
   