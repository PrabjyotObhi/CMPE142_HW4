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
        num = 1
        global queue
        while True:
            condition.acquire()
            if len(queue) == MAX_NUM:
                print("Queue full, producer is waiting")
                condition.wait()
                print("Space in queue, Consumer notified the producer")
            num = (num + 1) % 3
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


class Customer2Thread(Thread): #waiting for burgers[1] and sodas[0]

    food = ['soda', 'burger', 'fries']

    def run(self):
        global queue
        while True:
            condition.acquire()
            if not queue:
                print("Nothing in queue, consumer is waiting")
                condition.wait()
                print("Producer added something to queue and notified the consumer")
            if queue and queue[0] is self.food[2]:
                print("Customer 2 already has unlimited supply of ", self.food[2])
                condition.wait()
            item = queue.pop(0)
            print("Customer 2 consumed", item)
            condition.notify()
            condition.release()
            time.sleep(random.random())

class Customer3Thread(Thread): #waiting for burger[1] and fries[2]

    food = ['soda', 'burger', 'fries']

    def run(self):
        global queue
        while True:
            condition.acquire()
            if not queue:
                print("Nothing in queue, consumer is waiting")
                condition.wait()
                print("Producer added something to queue and notified the consumer")
            if queue and queue[0] is self.food[0]:
                print("Customer 3 already has unlimited supply of ", self.food[0])
                condition.wait()
            item = queue.pop(0)
            print("Customer 3 consumed", item)
            condition.notify()
            condition.release()
            time.sleep(random.random())


customer1eaten = 0
customer2eaten = 0
customer3eaten = 0


for val in range(100):
    #if the queue isnt empty
    ChefThread().start()
    ChefThread().join()
    if queue:
        if queue[val%10] is 1 and queue[val+1%10] is 2:
            Customer2Thread().start()
            customer2eaten = customer2eaten +1

        if queue[val%10] is 1 and queue[val+1%10] is 3:
            CustomerThread().start()
            customer1eaten = customer1eaten + 1

        if queue[val%10] is 2 and queue[val+1%10] is 3:
            Customer3Thread().start()
            customer3eaten = customer3eaten +1
    else:
        print("No one can eat because the queue is empty")
