 #!/usr/bin/env python3

import curses, string, traceback, time
import GameWorld as gw
import tiles
import Player_Class as pc
from Screen import Screen
from MenuHandler import MenuHandler
import Client
import threading

gw.spawnIsland.tiles,gw.mainShop.tiles = tiles.allTiles, tiles.allTiles
gw.spawnIsland.doors,gw.mainShop.doors = tiles.spawnIslandDoors, tiles.mainShopDoors

def keyloop(scr,scr2):
	#INTERACT, MOVE, INVENTORY, DRAW = 0,1,2,3
	initWorld = gw.spawnIsland
	screen = Screen(scr,pc.mainPlayer, initWorld)
	menu = MenuHandler(scr2,pc.mainPlayer)
	curses.start_color()
	scr.nodelay(True)
	screen.draw()

	while 1:
		menu.Update()
		try:
			c = chr(scr.getch())
		except:
			c = 'q;'
		if pc.mainPlayer.mode == 1:
			if c == 'w':
				pc.mainPlayer.movePos(0,-1)
				screen.draw()
			elif c == 'a':
				pc.mainPlayer.movePos(-1,0)
				screen.draw()
			elif c == 's':
				pc.mainPlayer.movePos(0,1)
				screen.draw()
			elif c == 'd':
				pc.mainPlayer.movePos(1,0)
				screen.draw()
			elif c == "q":
				client.Send("Quit")
				break
			elif c == "e":
				if not pc.mainPlayer.Interact():
					pc.mainPlayer.cursorShowing = True
					pc.mainPlayer.mode = 0
				screen.draw()
			elif c == "m":
				pc.mainPlayer.cursorShowing = True
				pc.mainPlayer.mode = 2
		elif pc.mainPlayer.mode == 0:
			if c == 'w':
				pc.mainPlayer.moveCursor(0,-1,True)
				screen.draw()
			elif c == 'a':
				pc.mainPlayer.moveCursor(-1,0,True)
				screen.draw()
			elif c == 's':
				pc.mainPlayer.moveCursor(0,1,True)
				screen.draw()
			elif c == 'd':
				pc.mainPlayer.moveCursor(1,0,True)
				screen.draw()
			elif c == "q":
				break
			elif c == "e":
				pc.mainPlayer.cursorShowing = False
				pc.mainPlayer.Interact()
				screen.draw()
		elif pc.mainPlayer.mode == 2:
			if c in '1234567890':
				pc.mainPlayer.setSelectedTile(int(c))
				screen.draw()
			elif c in 'fghjkl':
				pc.mainPlayer.setSelectedTile(str(['f','g','h','j','k','l'].index(c)))
			elif c == 'w':
				pc.mainPlayer.moveCursor(0,-1,False)
				screen.draw()
			elif c == 'a':
				pc.mainPlayer.moveCursor(-1,0,False)
				screen.draw()
			elif c == 's':
				pc.mainPlayer.moveCursor(0,1,False)
				screen.draw()
			elif c == 'd':
				pc.mainPlayer.moveCursor(1,0,False)
				screen.draw()
			elif c == ' ':
				pc.mainPlayer.setTile()
				screen.draw()
			elif c == "q":
				break
			elif c == "m":
				pc.mainPlayer.cursorShowing = False
				pc.mainPlayer.mode = 1
				screen.draw()
			elif c == "p":
				pc.mainPlayer.world.saveArray(screen.world.name)
		scr.refresh()



def main(stdscr):
	scr = stdscr.subwin(46,160,0,0)
	scr2 = stdscr.subwin(45,21,0,160)
	curses.curs_set(0)
	keyloop(scr,scr2)


if __name__=='__main__':
	try:
		# Initialize curses
		stdscr=curses.initscr()
		# Turn off echoing of keys, and enter cbreak mode,
		# where no buffering is performed on keyboard input
		curses.noecho()
		curses.cbreak()

		# In keypad mode, escape sequences for special keys
		# (like the cursor keys) will be interpreted and
		# a special value like curses.KEY_LEFT will be returned
		stdscr.keypad(1)
		main(stdscr)                    # Enter the main loop
		# Set everything back to normal
		stdscr.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin()                # Terminate curses
	except:
		# In event of error, restore terminal to sane state.
		stdscr.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin()
		traceback.print_exc()
