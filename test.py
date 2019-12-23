import time
import multiprocessing as mp
from multiprocessing import Process
def accumulation(x):
    for a in range(x):
        print(a)
if __name__=="__main__":
    begin = time.time()
    p = Process(target=accumulation, args=(1000000,))
    p.start()
    p.join()
    #  accumulation(100https://www.youtube.com/results?search_query=lofi&sp=EgQQAVgD00000)
    # pool =mp.Pool(mp.cpu_count())
    # pool.map(accumulation,[1000000])
    # pool.close()
    # pool.join()
    end =time.time()
    print(begin,end)
    print('the totol time is %f second'%(end-begin))



