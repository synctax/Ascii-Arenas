import GameWorld as gw
import random
import AI
import Item
from Inventory import Inventory

#CHARACTER CLASS
class Player():
	def __init__(self, initx, inity, initchars,world):
		self.stats = {"HEALTH":100}
		self.inventory = Inventory(10)
		self.x = initx
		self.y = inity
		self.chars = initchars
		self.charnum = 0
		self.char = initchars[0]
		self.world = world
		self.cursorx = 0
		self.cursory = 0
		self.cursorShowing = False
		self.mode = 1
		self.selectedTile = 0
		self.modeNames = ['INTERACT','PLAY','BUILD']
		self.world.addPlayer(self)

	def pickUpItem(self,itemName,amount):
		self.Inventory.addItem(itemName,amount)

	def setChar(self, charindex):
		self.charnum = charindex
		self.char = self.initchars[self.charnum]

	def setPos(self, x,y):
		self.x = x
		self.y = y

	def changeWorld(self,world):
		self.world.removePlayer(self)
		world.addPlayer(self)
		self.world = world

	def movePos(self, xDiff, yDiff):
		newX = self.x + xDiff
		newY = self.y + yDiff

		if self.world.getTile(newX,newY).isCollidable:
			return False
		self.x += xDiff
		self.y += yDiff
		if self.mode == 1:
			self.cursorx = self.x
			self.cursory = self.y

	def getChar(self):
		return self.char

	def setSelectedTile(self,tile):
		self.selectedTile = tile

	def setTile(self):
		self.world.setTile(self.selectedTile, self.cursorx, self.cursory)

	def Interact(self):
		x = self.cursorx
		y = self.cursory
		if self.world.getTile(x,y).canInteract:
			self.mode = self.world.getTile(x,y).onInteract(self.world,self,self.maxDistFromPlayer(x,y))
			return True
		else:
			self.mode = 1
			return False

	def maxDistFromPlayer(self,x,y):
		return max(abs(self.x-x),abs(self.y-y))

	def moveCursor(self,x,y,collide):
		newX = self.cursorx  + x
		newY = self.cursory +y

		if (not self.maxDistFromPlayer(newX, newY) < 10 or self.world.getTile(newX,newY).isCollidable) and collide:
			return False
		self.cursorx += x
		self.cursory += y

	def toggleCursor(self):
		if self.cursorShowing:
			self.cursorShowing = False
		else:
			self.cursorShowing = True



class Mob(Player):
	def __init__(self, initx, inity, initchars,color,world, ai):
		self.x = initx
		self.y = inity
		self.chars = initchars
		self.charnum = 0
		self.char = initchars[0]
		self.world = world
		self.ai = ai
		self.color = color
		world.mobs.append(self)

playerChars = ["@"]
crabChars = ['#','*']
mainPlayer = Player(int(80),int(25),playerChars,gw.spawnIsland)
spawnCrabs = []
#make spawn crabs
'''for i in range(0,random.randint(3,10)):
	spawnCrabs.append(Mob(random.randint(25,129),random.randint(9,43),crabChars,160,gw.spawnIsland,AI.mobAi))'''
