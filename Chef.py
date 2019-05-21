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


class CustomerThread(Thread):  # waiting for fries[2] and sodas[0], has unlimited burgers

    food = ['soda', 'burger', 'fries']

    def run(self):
        global queue
        while True:
            condition.acquire()
            if not queue:
                print("Nothing in queue, consumer is waiting")
                condition.wait()
                print("Producer added something to queue and notified the consumer")
            '''if queue and queue[0] is self.food[1]:
                print("Customer 1 already has unlimited supply of ", self.food[1])
                condition.wait()'''
            item = queue.pop(0)
            print("Customer 1 consumed", item)
            condition.notify()
            condition.release()
            time.sleep(random.random())
