#!/usr/bin/env python

import threading
import time
import logging

#multithreading
class ThreadPool(threading.Thread):
#accepts threading.Thread for normal threads or thread_window()
	def __init__(self):
		super(Threadpool, self).__init__()
		self.threadID = threadID
		self.name = name
		self.counter = counter
		threads.append(self)
		self.run()
	def run(self):
		logging.info("Starting " + self.name)
		logging.info(print_time(self.name, self.counter, 5))
		logging.info("Exiting " + self.name)


def log_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

def worker():
	while not arg['stop']:
		try:
			logger.debug(arg)
			time.sleep(0.5)
		except Exception:
			logger.exception("[-]logging failed on debug of arbitrary test argument")
			raise

def clean_all():
	#close all windows
	
	#del threading & semaphore objects
	pool_sema.release
	for t in threads:
		t.join()
	del pool
	#force join any outstanding process threads
	exit()

def main(args):
	threads = []
	global pool_sema = BoundedSemaphore(23)

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG, format=(%(threadName-19s) %(message)
	args = sys.argv[1:]
	main(args)
