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
		self.UPDATE_FLAG = False
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
		self.players[str(player)] = Player(50,20,["@"],self.world)

	def removePlayer(self,player):
		self.players[str(player)].world.removePlayer(self.players[str(player)])
		del self.players[str(player)]

	def movePlayer(self,player,data):
		data = data.split(" ")
		self.players[str(player)].setPos(int(data[0]),int(data[1]))

	def login(self,server):
		self.server = server
		self.Send("Hello!")
		self.shutdown = False
		#clients, serverA = self.mainSocket.recv(1024)
		#clients = json.loads(clients)
		#for client in clients:
			#self.addPlayer(client)
		self.world = gw.spawnIsland

	def Logout(self):
		self.Send("Quit")
		self.shutdown = True

	def receving(self, name, sock):
		while True:
			while not self.shutdown:
				data = sock.recv(1024)
				self.handleInput(data)

	def handleInput(self,data):
		decodedData = json.loads(data)
		data = decodedData["data"]
		addr = tuple(decodedData["addr"]) #decode list into a tuple
		if self.players.has_key(str(addr)):
			if data == "Quit":
				self.removePlayer(addr)
				self.UPDATE_FLAG = True
				return True
			self.movePlayer(addr,data)
		else:
			self.Send(str(self.player.x)+" "+str(self.player.y))
			self.addPlayer(addr)
		self.UPDATE_FLAG = True

	def Send(self,message):
		self.mainSocket.sendto(message, self.server)

	def startListening(self):
		self.rT = threading.Thread(target=self.receving, args=("RecvThread",self.mainSocket))
		self.rT.setDaemon(True)
		self.rT.start()

	def Close(self):
		self.shudown = True
		self.mainSocket.close()
