import random
import time
from datetime import datetime

import locale

import time

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)
   

    return time.strftime(format, time.localtime(ptime))


def strTime(start,format='%d/%m/%Y %I:%M %p'):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    #stime = time.mktime(time.strptime(start, format))
    
    return time.strftime(format, time.localtime(time.mktime(time.strptime(start, format))))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%d/%m/%Y %I:%M %p', prop)


t1 = randomDate("1/1/2010 1:30 PM", "12/12/2010 4:50 AM", random.random())
t2 = strTime("6/1/2010 1:30 PM")
t3 = strTime("12/1/2010 1:30 PM")

def createMessage(level,msg1):
        format='%a, %d-%b-%Y %H:%M:%S %p'
        
        locale.setlocale(locale.LC_ALL, '')


        hoje = datetime.today()
        agora = hoje.strftime(format)
        msg = "%s- %s - %s"%(agora,level,msg1)
        return msg
        
        

locale.setlocale(locale.LC_ALL, '')

print t1
print t2
print t3
print t2 <= t1 <= t3
print datetime.today()

locale.setlocale(locale.LC_ALL, '')
format='%d/%m/%Y %I:%M:%S %p'

hoje = datetime.today()


print  hoje.strftime('%d-%m-%Y-%I:%M:%S %p')
print createMessage("info", "teste")


