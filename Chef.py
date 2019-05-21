from threading import Thread, Condition
import time
import random

# I am getting IndexError, I think I need to add Semaphore into this implementation

queue = []
MAX_NUM = 10
condition = Condition()


class ChefThread(Thread):
    food = ['soda', 'burger', 'fries']

    def run(self):
        nums = range(3)
        global queue
        while True:
            condition.acquire()
            if len(queue) == MAX_NUM:
                print("Queue full, producer is waiting")
                condition.wait()
                print("Space in queue, Consumer notified the producer")
            num = random.choice(nums)
            queue.append(self.food[num])
            print("Produced ", self.food[num])
            condition.notify()
            condition.release()
            time.sleep(random.random())



