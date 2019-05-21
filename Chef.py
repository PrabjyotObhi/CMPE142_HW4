from threading import Thread, Condition
import time
import random
import threading
import random
import time

hasSoda, hasFries, hasBurger = 0, 0, 0


def generateRandomItems():
    item1 = random.randint(1, 100) % 3
    item2 = random.randint(1, 100) % 3
    if (item1 == item2):
        item2 += 1
        item2 %= 3
    return [item1, item2]


class Customer:
    def __init__(self, meals):
        self.condMutex = threading.Condition()
        self.chefSleep = threading.Semaphore(0)
        self.meals = meals
        self.food = ['soda', 'burger', 'fries']
        # ITEMS UNAVAILABLE AT START
        self.availableItems = [False] * 3
        self.consumerThreads = []
        self.terminate = False
        # Create Three Consumer Threads
        self.consumerThreads.append(threading.Thread(target=self.consumerRoutine, name='HasFries', args=(0, 1)))
        self.consumerThreads.append(threading.Thread(target=self.consumerRoutine, name='HasSoda', args=(1, 2)))
        self.consumerThreads.append(threading.Thread(target=self.consumerRoutine, name='HasBurger', args=(0, 2)))
        for consumer in self.consumerThreads:
            consumer.start()
        self.chefThread = threading.Thread(target=self.chefRoutine)
        self.chefThread.start()

    def chefRoutine(self):
        for i in range(self.meals):
            # Generate two random items.
            randomItems = generateRandomItems()
            self.condMutex.acquire()
            print('Chef produced: {0} and {1}'.format(self.food[randomItems[0]], self.food[randomItems[1]]))
            # Make items available on table.
            self.availableItems[randomItems[0]] = True
            self.availableItems[randomItems[1]] = True
            # Announce to all consumers that items are made available on table.
            self.condMutex.notify_all()
            self.condMutex.release()
            # Go to sleep till the selected consumer is done with meal.
            self.chefSleep.acquire()

    def consumerRoutine(self, neededItem1, neededItem2):
        myName = threading.currentThread().getName()
        while 1:
            self.condMutex.acquire()
            # Block till the needed items are on table.
            while (False == self.availableItems[neededItem1] or False == self.availableItems[neededItem2]):
                self.condMutex.wait()
            self.condMutex.release()
            # Check if it was a terminate signal.
            if (True == self.terminate):
                break
            # Pickup the items from the table.
            self.availableItems[neededItem1] = False
            self.availableItems[neededItem2] = False
            # All ingredients are with you start eating.
            print('{0} started meal.'.format(myName))
            # eating
            randomTime = random.randint(1, 100)
            randomTime %= 5
            time.sleep(randomTime + 1)
            if myName == 'HasFries':
                global hasFries
                hasFries += 1
            elif myName == 'HasBurger':
                global hasBurger
                hasBurger += 1
            elif myName == 'HasSoda':
                global hasSoda
                hasSoda += 1
            print('{0} ended meal.'.format(myName))
            # Eating is done, wakeup the sleeping chef.
            self.chefSleep.release()

    def waitForCompletion(self):
        # Wait for chef thread to end.
        self.chefThread.join()
        # Send terminate signal to consumer threads.
        self.condMutex.acquire()
        self.terminate = True
        self.availableItems = [True, True, True]
        self.condMutex.notify_all()
        self.condMutex.release()


if __name__ == "__main__":
    obj = Customer(100)
    obj.waitForCompletion()
    print("\nHasFries: ", hasFries)
    print("HasBurger: ", hasBurger)
    print("HasSoda: ", hasSoda)
