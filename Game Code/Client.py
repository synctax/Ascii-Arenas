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
		self.shutdown = False
		self.ip = ip
		self.port = port
		self.player = player
		self.screen = screen
		self.menu = menu
		self.server = None
		self.mainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.mainSocket.bind((self.ip, self.port))
		self.mainSocket.setblocking(0)
		self.players = {}
		self.functions = [Player.setChar,Player.setPos,Player.movePos,Player.setTile,Player.Interact]

	def login(self,server):
		self.server = server
		self.Send("{'function':1,'args':(1,2)")

	def receving(self, name, sock):
		while not self.shutdown:
			try:
				while True:
					data, addr = sock.recvfrom(1024)
					print(data)
					message = json.loads(data)
					self.handleInput(massage["data"],message["addr"])
			except:
				pass

	def handleInput(self,data,addr):
		if addr not in self.clients:
			self.clients[addr] = pc.Player(int(80),int(25),["@"],self.screen.world)
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
