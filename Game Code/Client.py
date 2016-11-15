import GameWorld as gw
import tiles
from Player_Class import Player
from Screen import Screen
from MenuHandler import MenuHandler
import socket
import threading
import json
#server = ('127.0.0.1',5000)
#data format: {"function" : <index of function>, "args": (args tuple)}

class Client():
	def __init__(self,player,screen,menu):
		self.shutdown = True
		self.ip = self.getIP()
		self.port = 0
		self.player = player
		self.screen = screen
		self.world = None
		self.menu = menu
		self.server = None
		self.mainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.mainSocket.bind((self.ip, self.port))
		self.mainSocket.setblocking(True)
		self.players = {}
		self.functions = [Player.setChar,Player.setPos,Player.movePos,Player.setTile,Player.Interact]

	def getIP(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("gmail.com",80))
		ip = (s.getsockname()[0])
		s.close()
		return ip

	def addPlayer(self,player):
		self.players[str(player)] = Player(0,0,["@"],self.world)

	def login(self,server):
		self.server = server
		self.Send("Hello!")
		self.shutdown = False
		clients, serverA = self.mainSocket.recvfrom(1024)
		#clients = json.dumps(clients)
		#for client in clients:
			#self.addPlayer(client)
		self.world = gw.spawnIsland

	def Logout(self):
		self.Send("Quit")
		self.shutdown = True

	def receving(self, name, sock):
		while True:
			while not self.shutdown:
				#try:
				data = sock.recv(1024)
				print(data)
				self.handleInput(data)
				#except:
					#pass

	def handleInput(self,data):
		try:
			decodedData = json.loads(data)
			data = decodedData["data"]
			addr = tuple(decodedData["addr"]) #decode list into a tuple
			if data == "Hello!":
				self.addPlayer(addr)
			self.screen.draw()
			print(data)
		except:
			raise
			#print(data)

	def Send(self,message):
		self.mainSocket.sendto(message, self.server)

	def startListening(self):
		self.rT = threading.Thread(target=self.receving, args=("RecvThread",self.mainSocket))
		self.rT.setDaemon(True)
		self.rT.start()

	def Close(self):
		self.shudown = True
		self.mainSocket.close()

'''import socket
import threading
import time

tLock = threading.Lock()
shutdown = False

def receving(name, sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print str(data)
        except:
            pass
        finally:
            tLock.release()

host = '127.0.0.1'
port = 0

server = ('127.0.0.1',5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receving, args=("RecvThread",s))
rT.start()

alias = raw_input("Name: ")
message = raw_input(alias + "-> ")
while message != 'q':
    if message != '':
        s.sendto(alias + ": " + message, server)
    tLock.acquire()
    message = raw_input(alias + "-> ")
    tLock.release()
    time.sleep(0.2)

shudown = True
rT.join()
s.close()
'''
