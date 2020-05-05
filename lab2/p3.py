
import threading 
import time
import queue
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
P = 5003
addr = (IP, PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

helper = []
blockchain = []
event = []
balance = 10
clk = 0
count = 0
broad = False
q = queue.Queue(10)
tmp = queue.Queue(10)
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

		while True:
			# socket set up
			
			# clk set up
			if q.empty():	
				pass
				# threadLock.acquire()
				# print("q is empty, block")
			if not q.empty():
				# print("q is not empty, unblock")
				# threadLock.release()
				e = q.get()

				# lambort logic
				if e[0]=="reply":
					# print("in reply")
					clk = clk+1
					
					# print('sender:',sender)
					# print('receiver:',receiver)
					
					
					# val = (("receive event: "+e[1],clk))
					# send release message
					c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					c.connect(addr)
					data = str(e[1])+"/"+str(e[2])+"/"+str(e[3])+"/"+str(e[4])+"/"+str(clk)
					c.sendall(data.encode('utf-8'))
					c.close()
				elif e[0]=="send":
					c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					c.connect(addr)

					clk = clk+1
					# event(type=send, msg type=request, amt=amt, id = id, sendID = 1, clk=clk)
		
					# val = (("send event: "+e[1], clk))
					# data = e[1]+"/"+str(clk)+"/"+str(e[3])
					# data message = (msg type, amt, receive id, send id, clk)
					# msg type = 0 is request
					data = str(e[1])+"/"+str(e[2])+"/"+str(e[3])+"/"+str(e[4])+"/"+str(clk)
					c.sendall(data.encode('utf-8'))
					c.close()
				# combine both release and broadcast
				elif e[0]=="release" and broad:
					tmp.put(e)
					clk = clk+1
					for i in range (0,2):
						element = tmp.get()
						c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						c.connect(addr)
						
						data = str(e[1])+"/"+str(element[2])+"/"+str(element[3])+"/"+str(element[4])+"/"+str(clk)
						c.sendall(data.encode('utf-8'))
						c.close()
						count = count - 1
					if count == 0:
						broad = False
					# count = count - 1
					# if count == 0:
					# 	broad = False
					# # print("in release")
					# c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					# c.connect(addr)
					# clk = clk+1
					# data = str(e[1])+"/"+str(e[2])+"/"+str(e[3])+"/"+str(e[4])+"/"+str(clk)
					# c.sendall(data.encode('utf-8'))
					# c.close()
				else:
					if e[0]=="release":
						tmp.put(e)

				# events.append(val)
				# threadLock.acquire()
				# print("add: ", e, "unblock the q")


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
		s.bind((IP, P))
		s.listen(1)
		while True:

			# print("wait for message")
			stream, addr = s.accept()
			# print("socket created, wait for incoming message")
			message = stream.recv(1024).decode('utf-8')
			# print(message)

			# print("receive message push to queue")
			# recv message (event, msg, clk, id)
			# threadLock.release()

			# decode msg
			msg = message.split("/")
			# data = (("receive","'"+msg[0]+"'",0,int(msg[1])))
			# when receive request
			if msg[0]=='0':
				# print("receive request")
				sender = 'P'+msg[3]
				receiver = 'p'+msg[2]
				amount = '$'+msg[1]
				if msg[2] == '3':
					balance = balance+int(msg[1])
				blockchain.append((sender,receiver,amount))
				helper.append((1, int(msg[1]), int(msg[2]), int(msg[3]), int(msg[4])))

				clk = max(int(msg[4]), clk) + 1
				event = ["reply", 1, int(msg[1]), int(msg[2]), int(msg[3]), int(msg[4])]
			# when receive reply
			# when should the balanced be changed
			elif msg[0] == '1':
				# print("receive reply")
				sender = msg[3]
				receiver = msg[2]
				amount = int(msg[1])
				count = count + 1
				# c = int(msg[4])
				# clk = max(clk,c)+1
				if count == 2:
					broad = True
				if broad == True:
					# print(amount)
					if sender == '3':
						balance = balance-amount
				
				# print('sender:',sender)
				# print('receiver:',receiver)
				clk = max(int(msg[4]), clk) + 1
				event = ["release", 2, int(msg[1]), int(msg[2]), int(msg[3]), int(msg[4])]
			elif msg[0] == '2':
				# print("receive release")
				clk = max(int(msg[4]), clk) + 1
				event = ["finish", 2, int(msg[1]), int(msg[2]), int(msg[3]), int(msg[4])]
			# print(event)
			q.put(event)
			# print("go back to wait")
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
	x = int(input("\nInput 1 to transfer or 2 to print blockchain or 3 to print balance \n"))
	
	# Add local event
	if x == 1:
		# this send the request
		process = input("Add receiver id: ")
		id = int(process)
		amt = int(input("Send amt: "))

		# balance = balance - amt
		# event(type=send, msg type=request, amt=amt, id = id, sendID = 1, clk=clk)
		if amt<= balance:
			blockchain.append(('P3', 'P'+process, '$'+str(amt)))
			
			clk = clk + 1
			helper.append((0, amt, id, 3, clk))
			event = (("send", 0, amt, id, 3, clk))
		# threadLock.release()
			q.put(event)
		else:
			print("Failure")
	elif x == 2:
		print(blockchain)
		print(helper)
		res = []
		helper.sort(key = sortFifth)
		print(helper)
		for e in helper:
			sen = 'P'+str(e[3])
			re = 'P'+str(e[2])
			am = '$'+str(e[1])
			res.append((sen,re,am))
		print(res)  

	elif x == 3:
		print('$', str(balance))
	else:
		print(clk)






	