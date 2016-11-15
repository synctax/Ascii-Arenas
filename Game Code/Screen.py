import curses

class Screen:
	def __init__(self,stdscr,player, world):
		self.scr = stdscr
		self.world = 0
		self.player = player

	def draw(self):
		self.world = self.player.world
		for y in range(0,min(self.world.height-7,46)):
			for x in range(0,min(self.world.width,160)):
				char = self.world.getPosChar(x,y)
				col = self.world.getColor(x,y)
				tile = self.world.getTile(x,y)
				curses.init_pair(col,0,col)
				self.scr.addstr(y,x,char, curses.color_pair(col))

		for player in self.world.players:
			self.scr.addstr(player.y,player.x,player.getChar(),curses.A_BOLD)

		for mob in self.world.mobs:
			curses.init_pair(mob.color,mob.color,0)
			self.scr.addstr(mob.y,mob.x,mob.getChar(),curses.color_pair(mob.color))

		if self.player.cursorShowing:
			self.scr.addstr(self.player.cursory,self.player.cursorx,' ', 226)
		self.scr.refresh()
