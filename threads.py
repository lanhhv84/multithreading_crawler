from __future__ import print_function
import threading
import time


class Threads:
    """
    How to use:
        Create Threads object
            th = Threads(num_threads, data_pool)

        Create a function f that take two argument
            The first one is data in pool
            The second one is a tuple of additional arguments
            Ex:
            def func(data, extra):
                # extra = (a1, a2)
                a1, a2 = extra
                print(data + a1 + a2)

        Run
            th.run(func, (10, 20))

    """

    def __init__(self, num_threads, data_pool):
        self.num_threads = num_threads
        self.data_pool = data_pool
        self.lock = threading.Lock()
        self.threads = []
    

    def run(self, func, extra_args):
        # Task receive a tuple
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.task, args=(func, extra_args))
            self.threads.append(thread)
            thread.start()
        
    def join(self):
        for t in self.threads:
            t.join()
        
    def task(self, func, extra_args):
        while len(self.data_pool) > 0:
            data = None
            with self.lock:
                if len(self.data_pool) == 0:
                    return
                else:
                    data = self.data_pool[0]
                    self.data_pool = self.data_pool[1: ]
            func(data, extra_args)
        

