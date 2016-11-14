import curses
import Item

class MenuHandler():
	def __init__(self, scr, player):
		self.scr = scr
		self.player = player
		self.menus = []

	def Update(self):
		curses.init_pair(1,15,236)
		self.scr.erase()
		self.scr.bkgd(' ', curses.color_pair(1))
		self.scr.attron(curses.A_BOLD)
		self.scr.attron(curses.color_pair(1))
		self.scr.addstr(0,0,"    CURRENT MODE    ")
		self.scr.addstr(1,0,"--------------------")
		self.scr.addstr(2,1,self.player.modeNames[self.player.mode])
		self.scr.addstr(3,0,"--------------------")
		if self.player.mode == 0:
			self.scr.addstr(5,1,"Move Cursor-W,A,S,D")
			self.scr.addstr(6,1,"Interact - E")
		elif self.player.mode == 1:
			self.scr.addstr(5,1,"Move - W,A,S,D")
			self.scr.addstr(6,1,"Interact - E")
			self.scr.addstr(7,1,"Build - M")
			self.scr.addstr(8,0,"---------------------")
			self.scr.addstr(9,0,"     Inventory")
			self.scr.addstr(10,0,"---------------------")
			for i,v in enumerate(self.player.inventory.occupiedItems.keys()):
				if v != "NON_STACKABLE":
					count = self.player.inventory.occupiedItems[v]
					self.scr.addstr(10+i,int((21-5)/2),str(i)+"("+str(count) +")")
					col = Item.allItems[v].getCol()
					char = Item.allItems[v].getChar()
					curses.init_pair(col,col,0)
					self.scr.addstr(11+i,0,char,curses.color_pair(col))
					self.scr.addstr(11+i,int((21-len(v))/2)+1,v)
		elif self.player.mode == 2:
			self.scr.addstr(5,1,"Move Cursor-W,A,S,D")
			self.scr.addstr(6,1,"Build - SPACE")
			self.scr.addstr(7,1,"Exit - M")
			self.scr.addstr(7,1,"Save Build - P")
			self.scr.addstr(9,0,"-------Tiles-------")
			for i,v in enumerate(self.player.world.tiles):
				self.scr.addstr(10+i,1,str(i) + " - " +v.getName())
				lastI = i
			self.scr.addstr(11+lastI,0,"-------------------")
			self.scr.addstr(13+lastI,0,"-------Doors-------")
			for j,k in enumerate(self.player.world.doors):
				self.scr.addstr(14+lastI+j,1,["F","G","H","J","K","L"][j] + " - " +k.getName())
				lastJ = j
			self.scr.addstr(15+lastI+lastJ,0,"-------------------")
		self.scr.addstr(44,1,"      Q - Quit")
		self.scr.attroff(curses.A_BOLD)
		self.scr.attroff(curses.color_pair(1))

		self.scr.refresh()
