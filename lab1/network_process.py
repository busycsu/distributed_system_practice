import socket
import time
import threading
import queue
import random
IP = "127.0.0.1"
PORT = 5000


q = queue.Queue(10)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# send thread
class cThread (threading.Thread):
	def __init__ (self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		while True:
			if not q.empty():
				delay = random.randint(1,5)
				print("send delay: ", delay)
				time.sleep(delay)
				c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				ele = q.get()
				
				x = ele.split("/")
				print("x: ", x)
				p = int(x[2])
				c.connect((IP, PORT+p))
				c.sendall(ele.encode('utf-8'))
				c.close()


# receive thread
class sThread (threading.Thread):
	def __init__ (self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		s.bind((IP, PORT))
		s.listen(3)
		while True:
			stream, addr = s.accept()
			print("socket created, wait for incoming message")
			message = stream.recv(1024).decode('utf-8')
			print(message)
			
			q.put(message)





thread1 = cThread(1, "Thread-1", 1)
thread2 = sThread(2, "Thread-2", 2)

thread1.start()
thread2.start()






