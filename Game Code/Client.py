import GameWorld as gw
import tiles
from Player_Class import Player
from Screen import Screen
from MenuHandler import MenuHandler
import socket
import threading
import json

''' Language:
<code> <param1> <param2> <param3>
m <x pos> <ypos>						# move to location
p <xpos> <ypos> <block#>				# place block at location
j <xpos> <ypos> <char>					# join game or introduce self to newb
q										# quit game
r <room#>								# change room
s <message>	<to> <from>				    # send message to target
t <item#>								# pick up item
d <xpos> <ypos>	<item#>				    # drop item
u <item#> <target>						# use item
'''


class Client():
	def __init__(self,screen,player):
		self.shutdown = True
		self.UPDATE_FLAG = False
		self.ip = self.getIP()
		self.port = 0
		self.screen = screen
		self.world = gw.spawnIsland
		self.server = None
		self.mainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.mainSocket.bind((self.ip, self.port))
		self.mainSocket.setblocking(True)
		self.players = {}
		self.functions = [Player.setChar,Player.setPos,Player.movePos,Player.setTile,Player.Interact]
		self.player = player
		self.playerChars = ["#","$","%","&","H","P"]

	def getIP(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("gmail.com",80))
		ip = (s.getsockname()[0])
		s.close()
		return ip

	def addPlayer(self,player):
		self.players[str(player)] = Player(50,20,[self.playerChars[len(self.players)-1]],self.world)

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
		self.startListening()
		self.world = gw.spawnIsland

	def Logout(self):
		self.Send("q")
		self.shutdown = True
		self.players = {}

	def receving(self, name, sock):
		while True:
			while not self.shutdown:
				data = sock.recv(1024)
				self.handleInput(data)

	def handleInput(self,data):
		decodedData = json.loads(data)
		data = decodedData["data"].split(" ")
		command = data[0]
		addr = tuple(decodedData["addr"]) #decode list into a tuple
		playerKnown = self.players.has_key(str(addr))
		if playerKnown:
			if command == "q":
				self.removePlayer(addr)
				self.UPDATE_FLAG = True
				return True
			if command in "mrp":
				self.players[str(addr)].cmds[command](*tuple(data[1:]))
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
