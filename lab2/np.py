import socket
import time
import threading
import queue
import random

IP = "127.0.0.1"
PORT = 5000
q1 = queue.Queue(10)
q2 = queue.Queue(10)
q3 = queue.Queue(10)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# send thread
class sThread (threading.Thread):
	def __init__ (self, ID):
		threading.Thread.__init__(self)
		self.ID = ID
		# print("id", ID)

	def run(self):
		while True:
			
			# delay = random.randint(1,5)
			# print("send delay: ", delay)
			# time.sleep(delay)
			
			if self.ID == 1:
				if not q1.empty():
					# msg type = 0 is request
					# msg type = 1 is reply
					# msg type = 2 is release/broadcast
					time.sleep(1)
					ele = q1.get()
					# in request
					# send to its process
					# if ele[0]=='0':
					# 	x = ele.split("/")
					# 	print("x: ", x)
						
					# # send to origin process
					# # in request
					# if ele[0]=='1':
					# 	print("reply to 1")
					# 	x = ele.split("/")
					# 	print("x: ", x)
					# # send to id process
					# # in release
					# if ele[0]=='2':
					# 	x = ele.split("/")
					# 	print("x: ", x)

					
					print("delay complete")
					c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					c.connect((IP, PORT+1))#PORT+self.ID)) #for testing
					c.sendall(ele.encode('utf-8'))
					c.close()

			if self.ID == 2:
				if not q2.empty():
					time.sleep(1)
					ele = q2.get()

					
					print("delay complete")
					c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					c.connect((IP, PORT+2))#PORT+self.ID)) #for testing
					c.sendall(ele.encode('utf-8'))
					c.close()

			if self.ID == 3:
				if not q3.empty():
					
					time.sleep(1)
					# c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					ele = q3.get()
					print("delay complete")
					c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					c.connect((IP, PORT+3))#PORT+self.ID)) #for testing
					c.sendall(ele.encode('utf-8'))
					c.close()

			
			# p = int(x[2])
			# c.connect((IP, PORT+self.ID))
			# c.sendall(ele.encode('utf-8'))
			# c.close()


# receive thread
class rThread (threading.Thread):
	def __init__ (self):
		threading.Thread.__init__(self)

	def run(self):
		s.bind((IP, PORT))
		s.listen(3)
		while True:
			stream, addr = s.accept()
			print("socket created, wait for incoming message")
			message = stream.recv(1024).decode('utf-8')
			print(message)
			msg = message.split("/")
			if msg[0] == '0' or msg[0]== '2':
				if msg[3] == '1':
					q2.put(message)
					q3.put(message)
				if msg[3] == '2':
					q1.put(message)
					q3.put(message)
				if msg[3] == '3':
					q1.put(message)
					q2.put(message)
			elif msg[0] == '1':
				if msg[3] == '1':
					q1.put(message)
				if msg[3] == '2':
					q2.put(message)
				if msg[3] == '3':
					q3.put(message)
			# print('q1 is: ', q2.get())
			# event(msg type=request, amt=amt, id = id, sendID = 1, clk=clk)
			# msg type = 0 is request
			# msg type = 1 is reply
			# msg type = 2 is release/broadcast

			






receive_thread = rThread()
thread2 = sThread(2)
thread1 = sThread(1)
thread3 = sThread(3)
thread1.start()
thread2.start()
thread3.start()
receive_thread.start()







