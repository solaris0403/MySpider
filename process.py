#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from multiprocessing import Process, Lock


class MyProcess(Process):
    def __init__(self, loop, lock):
        Process.__init__(self)
        self.loop = loop
        self.lock = lock

    def run(self):
        for count in range(self.loop):
            time.sleep(1)
            self.lock.acquire()
            print('Pid:' + str(self.pid) + ' LoopCount:' + str(count))
            self.lock.release()


if __name__ == '__main__':
    lock = Lock()
    for i in range(10, 15):
        print(str(i))
        p = MyProcess(i, lock)
        # p.daemon = True
        p.start()
        # p.join()
    print('Main Process End')