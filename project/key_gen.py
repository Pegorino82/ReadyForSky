import time
import rsa
from threading import Thread
from queue import Queue

key_queue = Queue()


class KeyGenThread:

    def __init__(self, key_queue, *args, **kwargs):
        self.queue = key_queue
        self.thread = Thread(target=self.key_gen, args=args, kwargs=kwargs, daemon=True)
        self.thread.start()

    def key_gen(self, *args, **kwargs):
        print(f'start to generate key')
        length = kwargs['length']
        start_time = time.time()
        pubkey = str(rsa.newkeys(length)[0])
        end_time = time.time()
        print(f'key is ready ({end_time-start_time})')
        key_queue.put_nowait(pubkey)
