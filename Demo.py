#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from multiprocessing import Process, Semaphore, Lock, Queue
# import time
#
# buffer = Queue(10)
# empty = Semaphore(2)
# full = Semaphore(0)
# lock = Lock()
#
#
# class Consumer(Process):
#     def run(self):
#         global buffer, empty, full, lock
#         while True:
#             full.acquire()
#             lock.acquire()
#             buffer.get()
#             print('Consumer pop an element')
#             time.sleep(1)
#             lock.release()
#             empty.release()
#
#
# class Producer(Process):
#     def run(self):
#         global buffer, empty, full, lock
#         while True:
#             empty.acquire()
#             lock.acquire()
#             buffer.put(1)
#             print('Producer append an element')
#             time.sleep(1)
#             lock.release()
#             full.release()
#
#
# if __name__ == '__main__':
#     p = Producer()
#     c = Consumer()
#     p.daemon = c.daemon = True
#     p.start()
#     c.start()
#     p.join()
#     c.join()
#     print('Ended!')

from multiprocessing import Process, Pipe


class Consumer(Process):
    def __init__(self, pipe):
        Process.__init__(self)
        self.pipe = pipe

    def run(self):
        print('c')
        self.pipe.send('Consumer words')
        print('Consumer Received:', self.pipe.recv())


class Producer(Process):
    def __init__(self, pipe):
        Process.__init__(self)
        self.pipe = pipe

    def run(self):
        print('p')
        print('Producer Received:', self.pipe.recv())
        self.pipe.send('Producer Words')


if __name__ == '__main__':
    pipe = Pipe(duplex=True)
    p = Producer(pipe[0])
    c = Consumer(pipe[1])
    p.daemon = c.daemon = True
    c.start()
    p.start()
    p.join()
    c.join()
    print('Ended!')
