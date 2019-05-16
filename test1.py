from threads import Threads
import time
import urllib
import threading





def handler(data, extra):
    ex, lock = extra
    f = urllib.urlopen(data)
    response = f.read()

    with lock:
        with open(ex, "a") as f:
            f.write(response)
    

lock = threading.Lock()
data = ['http://www.google.com/'] * 100
extra = ('./text.txt', lock)

threads = Threads(100, data)

threads.run(handler, extra)
threads.join()
# Done

    
            