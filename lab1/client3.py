import threading 
import time
import queue
import socket

IP = "127.0.0.1"
PORT = 5000
P = 5003
addr = (IP, PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

events = []
clk = 0
q = queue.Queue(10)

# This is processing thread or consumer thread
class cThread (threading.Thread):
	def __init__ (self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		global clk

		while True:
			# socket set up
			
			# clk set up
			if q.empty():	
				threadLock.acquire()
				# print("q is empty, block")
			if not q.empty():
				# print("q is not empty, unblock")
				threadLock.release()
				e = q.get()

				# lambort logic
				if e[0]=="receive":
					clk = max(clk,e[3])+1
					val = (("receive event: "+e[1],clk))
				elif e[0]=="send":
					c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					c.connect(addr)

					clk = clk+1
					val = (("send event: "+e[1], clk))
					data = e[1]+"/"+str(clk)+"/"+str(e[3])
					c.sendall(data.encode('utf-8'))
					c.close()

				else:
					clk = clk + 1
					val = (("local event: "+e[0]), clk)

				events.append(val)
				threadLock.acquire()
				# print("add: ", e, "unblock the q")


class pThread (threading.Thread):
	def __init__ (self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		s.bind((IP, P))
		s.listen(1)
		while True:
			# print("wait for message")
			stream, addr = s.accept()
			# print("socket created, wait for incoming message")
			message = stream.recv(1024).decode('utf-8')
			print(message)

			print("receive message push to queue")
			# recv message (event, msg, clk, id)
			threadLock.release()

			# decode msg
			msg = message.split("/")
			# (receive, msg, 0, clk)
			data = (("receive","'"+msg[0]+"'",0,int(msg[1])))


			q.put(data)
			print("go back to wait")
		# for i in range (0,3):
		# 	print("starting" + self.name)
		# 	# threadLock.acquire()
		# 	print_time(self.name, self.counter, 3)
		# 	# threadLock.release()



threadLock = threading.Lock()
threads = []

thread1 = cThread(1, "Thread-1", 1)
thread2 = pThread(2, "Thread-2", 2)

thread1.start()
thread2.start()

threads.append(thread1)
threads.append(thread2)


# for t in threads:
# 	t.join()
while True:
	x = int(input("\nInput 1 to add local event or 2 to send a message or 3 to print clock value \n"))
	
	# Add local event
	if x == 1:
		
		# specify the event (event, msg, send = 1, id)
		y = input("Event: ")
		event = ((y,"", 0,0))
		threadLock.release()
		q.put(event)
	elif x == 2:
		id = int(input("Add receiver id: "))

		msg = input("Send event name: ")
		event = (("send", msg, 1, id))
		threadLock.release()
		q.put(event)

	elif x == 3:
		for i in events:
			# print(events)
			print(i,"\n")
















	# event = int(input("enter: "))
	# if event == 1:
	# 	if q.empty():
	# 		print("empty")

	# 	print(l)
	# else:
	# 	q.put(event)





	