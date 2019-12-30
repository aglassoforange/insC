import time
import multiprocessing as mp
import progressbar
from multiprocessing import Process

class good_shit:
        pass



def accumulation(self,x):
        for a in range(1000000):
            print(x)

if __name__=="__main__":
    begin = time.time()
    p = Process(target=accumulation, args=('1200000',))
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



