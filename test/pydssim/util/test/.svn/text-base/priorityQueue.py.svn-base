'''
Created on 26/09/2009

@author: LGustavo
'''
from Queue import Queue
from heapq import heappush, heappop

class PriorityQueue(Queue):
    # Initialize the queue representation
    def _init(self, maxsize):
        self.maxsize = maxsize
        self.queue = []

    # Put a new item in the queue
    def _put(self, item):
        return heappush(self.queue, item)

    # Get an item from the queue
    def _get(self):
        return heappop(self.queue)

if __name__ == "__main__":
    q = PriorityQueue()
    q.put((2,"a"))
    q.put((0,"b"))
   
    q.put((1,"c"))
    q.put((2,"d"))
    q.put((1,"e"))
    q.put((0,"x"))
    while not q.empty():
        print q.get()
