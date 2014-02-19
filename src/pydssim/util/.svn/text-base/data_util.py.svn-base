'''
Created on 10/04/2010

@author: Luiz Gustavo
'''

import random
import time

def strTime(start, format='%d/%m/%Y %H:%M'):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    #stime = time.mktime(time.strptime(start, format))
    
    return time.strftime(format, time.localtime(time.mktime(time.strptime(start, format))))

def strTimeProp(start, end, prop, format='%d/%m/%Y %H:%M'):
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


def randomDate(start, end, prop):
    return strTimeProp(start, end, prop)