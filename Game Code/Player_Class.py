import GameWorld as gw
import random
import AI, json

#CHARACTER CLASS
class Player:
	def __init__(self, initx, inity, initchars,world):
		self.client = None
		self.x = initx
		self.y = inity
		self.chars = initchars
		self.charnum = 0
		self.char = initchars[0]
		self.world = world
		self.inventory = []
		self.cursorx = 0
		self.cursory = 0
		self.cursorShowing = False
		self.mode = 1
		self.selectedTile = 0
		self.modeNames = ['INTERACT','PLAY','BUILD','JOIN']
		self.serverList = {
		"Generic Server":('10.7.38.170',5000),
		"Super PvP Arena":('127.0.0.1',1337),
		"<HYPE 420>":('127.0.0.1',4200),
		"harambe":('10.7.38.170',9001)
		}
		self.world.addPlayer(self)
		self.cmds = {"m":self.setPos,"r":self.changeWorld,"p":self.setTile}

	def getLoc(self):
		return str(self.x)+" "+str(self.y)

	def connectToServer(self,selectNum):
		if not self.client.shutdown:
			self.client.Logout()
		self.client.login(self.serverList[self.serverList.keys()[selectNum]])

	def setChar(self, charindex):
		self.charnum = charindex
		self.char = self.initchars[self.charnum]

	def setPos(self, x,y):
		self.x = int(x)
		self.y = int(y)

	def changeWorld(self,world):
		self.world.removePlayer(self)
		gw.allWorlds[world].addPlayer(self)
		self.world = gw.allWorlds[world]
		if self.client:
			if not self.client.shutdown: self.client.Send("r "+self.world.name)

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
		if not self.client.shutdown:
			self.client.Send("m "+str(self.x) + " " +str(self.y))

	def getChar(self):
		return self.char

	def setSelectedTile(self,tile):
		self.selectedTile = tile

	def setTile(self,x=False,y=False,tile=False,world=False):
		if not x:
			x, y, tile, world = self.cursorx,self.cursory,self.selectedTile, self.world.name
			if not self.client.shutdown:
				if type(tile) == int:
					tileStr = str(tile)
				else:
					tileStr = "'"+tile+"'"
				self.client.Send("p "+str(x)+" "+str(y)+" "+tileStr+" "+world)
		else:
			if tile[0] != "'":
				tile = int(tile)
			else:
				tile = tile[1:-1]
		gw.allWorlds[world].setTile(tile,int(x),int(y))

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
