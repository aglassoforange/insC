import time
import multiprocessing as mp
import progressbar
from threading import Thread
from multiprocessing import Process
import queue
from Filewriting import Filewriting
import threading
import tensorflow as tf

hello = tf.constant('Hello,tensorflow!')

sess = tf.Session()

print(sess.run(hello))

a =tf.constant(10)
b = tf.constant(32)
print(sess.run(a+b))


# queue1=queue.Queue()
# queue2=queue.Queue()
# queue3=queue.Queue()
#
# queue1.put(1)
# class alpha:
#         def apple(self,queue1):
#             while True:
#                 a=queue1.get()
#                 print(a)
#                 b=a+1
#                 queue1.put(b)
#                 queue1.task_done()
#
#         def b(self,queque2):
#             while True:
#                 queue2.put(1)
#                 queque2.task_done()
#         def c(self,queue3):
#             while True:
#                 queue3.put(1)
#                 queue3.task_done()
#
# thread_list =[]
# a=alpha()
# t_apple = threading.Thread(target=a.apple,args=(queue1,))
# thread_list.append(t_apple)
#
#
#
# a = alpha()
# a.apple(queue1)

# t_b=threading.Thread(target=a.b,args=(queue2,))
# thread_list.append(t_b)
# t_c=threading.Thread(target=a.c,args=(queue3,))
# thread_list.append(t_c)
#
# for t in thread_list:
# for q in [queue1,queue2,queue3]:
