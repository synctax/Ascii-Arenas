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
	def __init__(self,ip,port,player,screen,menu):
		self.shutdown = True
		#self.ip = self.getIP()
		self.ip = ip
		self.port = port
		self.player = player
		self.screen = screen
		self.world = None
		self.menu = menu
		self.server = None
		self.mainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.mainSocket.bind((self.ip, self.port))
		#self.mainSocket.setblocking(0)
		self.players = {}
		self.functions = [Player.setChar,Player.setPos,Player.movePos,Player.setTile,Player.Interact]

	def getIP(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("gmail.com",80))
		ip = (s.getsockname()[0])
		s.close()
		return ip

	def addPlayer(self,player):
		self.players[str(player)] = Player.Player(0,0,["@"],self.world)

	def login(self,server):
		self.server = server
		self.Send("Hello!")
		'''clients, serverA = self.mainSocket.recvfrom(1024)
		clients = json.dumps(clients)
		for client in clients:
			self.addPlayer(client)
		self.world = gw.spawnIsland'''

	def Logout(self):
		self.Send("Quit")
		self.shutdown = True

	def receving(self, name, sock):
		while True:
			while not self.shutdown:
				try:
					while True:
						data, addr = sock.recvfrom(1024).decode()
						print(data)
						message = json.loads(data)
						self.handleInput(massage["data"],message["addr"])
				except:
					pass
			pass

	def handleInput(self,data,addr):
		if data == "Hello!":
			self.addPlayer(addr)
		funcData = json.loads(data)
		self.functions[funcData["functions"]](self.clients[addr],*funcData["args"])
		self.screen.draw()

	def Send(self,message):
		self.mainSocket.sendto(message.encode(), self.server)

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
