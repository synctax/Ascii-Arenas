#!/usr/bin/python

class node():
	def __init__(self,x,y,parent,endx,endy): 
		self.x, self.y = x, y
		self.parent = parent
		if self.parent:	
			self.g = self.parent.g + self.distance(self.parent.x,self.parent.y)
		else:
			self.g = 0
		self.h = self.distance(endx,endy) 
		self.f = self.g + self.h

	def distance(self,x,y):
		diffx = abs(self.x - x) 
		diffy = abs(self.y - y)
		adjcomp = abs(diffx - diffy)
		diagcomp = max(diffx,diffy) - adjcomp 
		return (adjcomp * 10) + (diagcomp * 14)
def minf(Set):
	Min = None
	for i,v in enumerate(Set):
		if Min:		
			if v.f < Min.f:
				Min = v
		else:
			Min = v
	return Min

def positionClosed(x,y,closednodes):
	for i,v in enumerate(closednodes):
		if v.x == x and v.y == y:
			return True
	return False

def nonNodable(x,y,worlddata,closednodes):
	if worlddata[y][x] == "1" or positionClosed(x,y,closednodes):
		return True
	else:
		return False

def positionOpen(x,y,opennodes):
	for i,v in enumerate(opennodes):
		if v.x == x and v.y == y:
			return True
	return False

def nodeAtPos(x,y,opennodes):
	for i,v in enumerate(opennodes):
		if v.x == x and v.y == y:
			return v

def findPathFromEnd(end):
	curNode = end
	path = []
	while curNode.parent:
		path.append([curNode.x,curNode.y])
		curNode = curNode.parent
	return path

def findPath(startx,starty,endx,endy,worldData):
	opennodes = []
	closednodes = []
	Node1 = node(startx,starty,None,endx,endy)
	opennodes.append(Node1)
	while True:
		current = minf(opennodes)
		del opennodes[opennodes.index(current)]
		closednodes.append(current)

		if current.x == endx and current.y == endy:
			break

		for i,v in enumerate([[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]):
			newX = current.x + v[0]
			newY = current.y + v[1]
			if nonNodable(newX,newY,worldData,closednodes):
				continue
			if not positionOpen(newX,newY,opennodes) or (positionOpen(newX,newY,opennodes) and (current.distance(newX,newY)+current.g)<nodeAtPos(newX,newY,opennodes).g):
				opennodes.append(node(newX,newY,current,endx,endy))
	return findPathFromEnd(current)
