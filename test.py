import time
import multiprocessing as mp
import progressbar
from threading import Thread
from multiprocessing import Process
import queue


def stuff(self):
        while True:
            a = q.get()
            for i in range(10):
                print(a+i)
            q.task_done()

q =queue.Queue()
threads=[]
for i in range(2):

    worker=Thread(target=stuff)
    worker.setDaemon(True)
    worker.start()
    threads.append(worker)

for i in range(10):
    q.put(1)

q.join()
for i in range(2):
    q.put(None)
for t in threads:
    t.join

