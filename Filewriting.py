import queue
import sys
import os
class Filewriting:

    def file_saving(self,save_queue):
        while True:
            file = save_queue.get()
            print(file)
            if len(file)==3:
                f = open("basic_info.txt ", 'a')
                f.writelines(["%s\n" % item for item in file])
                f.close()
                save_queue.task_done()
                break


