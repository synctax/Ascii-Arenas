import socket
import time
import GameWorld as gw
import tiles
import Player_Class as pc
from Screen import Screen
from MenuHandler import MenuHandler
import json
import threading

class Server():
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.clients = []
		self.mainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.mainSocket.bind((self.ip,self.port))
		self.mainSocket.setblocking(0)
		self.quitting = False
		self.lock = threading.Lock()

	def Start(self):
		self.thread = threading.Thread(target = self.main)
		self.thread.setDaemon(True)
		self.thread.start()

	def main(self):
		while not self.quitting:
			try:
				data, addr = self.mainSocket.recvfrom(1024).decode()
				self.handleData(data,addr)
				jsonMessage = json.dumps({"data":data, "addr" : addr})
				for client in self.clients:
					if client != addr:
						self.mainSocket.sendto(jsonMessage.encode(), client)
			except:
				pass
		self.mainSocket.close()

	def handleData(self,data,addr):
		if addr not in self.clients:
			self.clients.append(addr)

	def sendData(self,data):
		for client in self.clients:
		    self.mainSocket.sendto('data: ' + data + " addr: "+ self.ip, client)

	def Close(self):
		self.quitting = True


