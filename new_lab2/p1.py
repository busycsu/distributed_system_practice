
import threading 
import time
import queue
from queue import PriorityQueue
import socket

#  do we care if i before i receive i send a new message to network process
def sortFifth(val):
	return val[4]


class Node: 
   
    # Function to initialize the node object 
    def __init__(self, data): 
        self.data = data  # Assign data 
        self.next = None  # Initialize  
                          # next as null 
   
# Linked List class 
class LinkedList: 
     
    # Function to initialize the Linked  
    # List object 
    def __init__(self):  
        self.head = None





IP = "127.0.0.1"
PORT = 5000
P = 5001
addr = (IP, PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

lock = True
helper = []
clklist = []
blockchain = []
event = []
balance = 10
clk = 0
count = 0
broad = False
q = queue.Queue(10)
tmp = queue.Queue(10)
pq = PriorityQueue()


# This is processing thread or consumer thread, deal with local queue
class cThread (threading.Thread):
	def __init__ (self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		global clk
		global balance
		global count
		global broad
		global q
		global tmp
		global pq 
		global lock

		while True:
			# socket set up
			
			# clk set up
			if pq.empty():	
				pass
			if not pq.empty():
				time.sleep(3)
				print("stop waiting")
				a = pq.get()
				print(a)
				if a[1] == 1:	#change accordingly
					while lock:
						print("in lock")
						time.sleep(3)
						print("qthread",lock)
						# break
					print("end lock")
					balance = balance - a[3]
					lock = True

					msgtype = 2
					amt = a[3]
					dest = a[2]

					# send release
					c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					c.connect(addr)
					clk = clk +1
					clklist.append(("send release", clk))
					data = str(msgtype)+"/"+str(amt)+"/"+str(dest)+"/"+str(1)+"/"+str(clk) #change accordingly
					c.sendall(data.encode('utf-8'))
					c.close()
					print("finsh send release")

				else:
					# send reply
					c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					c.connect(addr)
					clk = clk +1
					clklist.append(("send reply", clk))
					msgtype = 1
					amt = a[3]
					dest = a[2]
					sid = a[1]
					data = str(msgtype)+"/"+str(amt)+"/"+str(dest)+"/"+str(sid)+"/"+str(clk) #change accordingly
					c.sendall(data.encode('utf-8'))
					c.close()
				ele1 = 'P'+str(a[1])
				ele2 = 'P'+str(a[2])
				ele3 = '$'+str(a[3])
				blockchain.append((ele1,ele2,ele3))
				


class pThread (threading.Thread):
	def __init__ (self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		global clk
		global balance
		global count
		global broad
		global q
		global lock
		s.bind((IP, P))
		s.listen(1)
		i = 0
		while True:

			# print("wait for message")
			stream, addr = s.accept()
			# print("socket created, wait for incoming message")
			message = stream.recv(1024).decode('utf-8')
			

			# decode msg
			msg = message.split("/")
			print("msg:",msg)
			# data = (("receive","'"+msg[0]+"'",0,int(msg[1])))
			# when receive request
			if msg[0]=='0':

				clk = max(int(msg[4]), clk) + 1
				clklist.append(("recv request", clk))
				c = int(msg[4])
				pid = int(msg[3])
				dest = int(msg[2])
				mon = int(msg[1])
				# event = ["reply", 1, int(msg[1]), int(msg[2]), int(msg[3]), int(msg[4])]

				pq.put((c,pid, dest, mon, 1))
			# when receive reply
			# when should the balanced be changed
			elif msg[0] == '1':
				i = i + 1
				print("recv reply")
				if i == 2:
					lock = False
					i = 0
				print("normal lock:",lock)
				clk = max(clk,int(msg[4])) + 1
				clklist.append(("recv reply", clk))
			elif msg[0] == '2':
				clk = max(clk,int(msg[4])) + 1
				clklist.append(("recv release", clk))
				print("recv release")
				if msg[2]=='1':
					print("recv money")
					balance = balance+int(msg[1])
			



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
	x = int(input("\nInput 1 to transfer or 2 to print blockchain or 3 to print balance \n"))
	
	# Add local event
	if x == 1:
		# this send the request
		process = input("Add receiver id: ")
		id = int(process)
		amt = int(input("Send amt: "))

		# balance = balance - amt

		if amt<= balance:

			clk = clk + 1
			clklist.append(("trans",clk))
			e = (("send", 0, amt, id, 1, clk))
			
			c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			c.connect(addr)
			clk = clk +1
			clklist.append(("send",clk))
			data = str(e[1])+"/"+str(e[2])+"/"+str(e[3])+"/"+str(e[4])+"/"+str(clk)
			c.sendall(data.encode('utf-8'))
			c.close()
			
			pq.put((clk,1,id,amt,0))
		else:
			clk = clk + 1
			print("Failure")
	elif x == 2:
		print(blockchain)
		


	elif x == 3:
		print('$', str(balance))

	else:
		print(clklist)




