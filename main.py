import Crawlcomments
from Crawlposts import Crawlposts
from  Filewriting import Filewriting
import queue
import threading
if __name__ =='__main__':
    save_queue=queue.Queue()
    url_queue=queue.Queue()
    detialpage_queue = queue.Queue()
    list_1=[]
    list_1.append('wang1ec')
    url_queue.put(list_1)
    a=Crawlposts()
    a.requests_frontpage(url_queue,detialpage_queue,save_queue,1)
    #
    print(detialpage_queue.get())
    # b=Filewriting()
    # b.file_saving(save_queue)
    # detialpage_queue.task_done()
    # thread_list=[]
    # t1 =threading.Thread(target=a.requests_frontpage,args=(url_queue,detialpage_queue,save_queue,1))
    # t1.start()
    # thread_list.append(t1)
    # t2= threading.Thread(target=a.b,args=(detialpage_queue,))
    # t2.start()
    # thread_list.append(t2)
    # t3= threading.Thread(target=a.a,args=(save_queue,))
    # t3.start()
    # thread_list.append(t3)
    # for t in thread_list:
    #     t.join()
    for q in [save_queue,detialpage_queue,url_queue]:
        q.join()


    print('process finished')
