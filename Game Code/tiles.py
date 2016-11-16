import GameWorld as gw

class envTile:
	def __init__(self,name, char, col, collide):
		self.char = char
		self.col = col
		self.isCollidable = False or collide
		self.canInteract = False
		self.name = name

	def getCol(self):
		return self.col

	def getChar(self):
		return self.char

	def getName(self):
		return self.name

class doorTile():
	def __init__(self,name, char, col, collide,range, room1,room1_y, room1_x, room2, room2_y, room2_x):
		self.char = char
		self.col = col
		self.isCollidable = False or collide
		self.room1,self.room2,self.x1,self.x2,self.y1,self.y2 = room1, room2, room1_x, room2_x, room1_y, room2_y
		self.canInteract = True
		self.range = range
		self.name = name

	def onInteract(self,room,player,dist):
		if dist <= self.range:
			if room == self.room1:
				player.changeWorld(self.room2.name)
				player.x = self.x2
				player.y = self.y2
			elif room == self.room2:
				player.changeWorld(self.room1.name)
				player.x = self.x1
				player.y = self.y1
		return 1

	def getCol(self):
		return self.col

	def getChar(self):
		return self.char

	def getName(self):
		return self.name

Sand = envTile("sand"," ", 3,False)
Grass = envTile("Grass","\"",2,False)
Water = envTile("Water","~", 4,True)
Tree = envTile("Wood Wall","|", 136,True)
Boulder = envTile("Stone Wall"," ", 245, True)
WoodFloor = envTile("Wood Floor",'.',94,False)
Void = envTile("Void"," ",232,True)

DoorToShop = doorTile("Shop/Spawn Door"," ",232,False, 4,gw.spawnIsland,27,88, gw.mainShop,22,20)

spawnIslandDoors = [DoorToShop]
mainShopDoors = [DoorToShop]
allTiles = [Sand,Grass,Water,Tree,Boulder,WoodFloor,Void]
