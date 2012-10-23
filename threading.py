#!/usr/bin/env python
import threading
import time

exitFlag = 0

class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        self.threadID = threadID
        self.name = name
        self.counter = counter
        threading.Thread.__init__(self)
    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name

def print_time(thread_name, delay, counter):
    while counter:
        if exitFlag:
            thread.exit()
        thime.sleep(delay)
        print "%s: %s" % (thread_name, time.ctime(time.time()))
        counter -= 1

# Create new threads
thread1 = myThread(1, 'Thread 1', 1)
thread2 = myThread(2, 'Thread 2', 2)

# Start new Threads
thread1.start()
thread2.run()

while thread2.isAlive():
    if not thread1.isAlive():
        exitFlag = 1
    pass
print "Exiting Main Thread"
