#!/usr/bin/env python 
import curses
import locale
import time
import struct
import threading
import sys
import yapps.simple_scan
import yapps.raw_scan
import yapps.yapps

def thread_window(fxn):
	def __init__(self, fxn, args):
		columns, rows = _terminal_size()
		window = (columns, rows)
		lock = threading.Lock()
		with thread, window in zip(threading.Thread, window):
			window.border()
			threads = ThreadPool(target=fxn, args=(track, window, lock))
			threads.daemon = True
			ThreadPool.add(thread)

def decurse(window):
	#always call methods to empty all data from buffers before closing a window
	window.touchwin(); window.erase; window.refresh();
	#set ncurses attributes for Window equal to standard terminal behavoir preventing potential errors
	curses.echo(); curses.nocbreak(); window.keypad(0); curses.curs_set(1)
	#curses.endwin() ought to lift curse from window, then refresh() returns terminal to pre-curse state
	curses.endwin()
	#cursed terminals need be test handled for safe exit by checking for success on refresh after endwin
	try:
		if not curses.isendwin():
			curses.endwin()
	except curses.error:
		print "[-]Error closing curses in window:" + str(curses.error)
		print "   curses failed to lift curse behavoir from calling terminal instance twice,"
		print "   if this terminal windows exhibits irregular behavior:"
		print "   restart window then update ncurses to latest release version 5 or greater"
	return

#set value of class attribute
def setval_menu(header, attr):
	win = curses.newwin(1,1,2,30)
	win.setxy(1,1)
	name = eval(header.__name__)
	value = eval(header.attr)
	win.addstr(name + " : " + attr + " : " + value)
	win.setxy(3,1)
	curses.echo()
	value = win.getstr()
	value = value.strip()
	exec(header+"."+attr+"="+value)
	decurse(win)
	return header

class scroll_menu:
	space = 32
	esc = 27

	opts = []
	screen = None

	def __init__(self, obj):
		try:
			self.curses_available = True
			self.win = curses.newwin(*win_size)
		except curses.error:
			self.__del__()
		for e in win_attr: exec e
		self.screen.border(0)
		self.topLineNum = 0
		self.highlightLineNum = 0
		self.obj = obj
		try:
			self.getopts(obj)
		except:
			pass
		self.run()

	def run(self):
		while True:
			self.displayScreen()
			# get user command
			c = self.screen.getch()
			if c == curses.KEY_UP: 
				self.scroll(1)
			elif c == curses.KEY_DOWN:
				self.scroll(-1)
			elif c == self.space:
				self.setval_menu(self.object, x[linenum])
				self.displayScreen()
			elif c == self.esc:
				self.exit()

	#get options from the attributes of an object instatiated by class
	def getopts(self, obj):
		self.opts = [x for x in header.__dict__.keys() if not (x[-1] == '_' | x[-6:] == 'header')]
		self.nopts = len(self.opts)

	def addopts(self, attr):
		opt = str("self."+attr)
		if eval(opt) != None: self.opts += exec(opt)
		else:
			del self.opt
			return 0

	def displayScreen(self):
		#clear screen
        	self.screen.erase()
		#generate rows
		for (n,opt,) in enumerate(self.opts[self.topLineNum:(self.topLineNum+curses.LINES)]):
			line = self.topLineNum + n
			self.screen.addstr(line, 0, opt)
			self.screen.refresh()

	def scroll(self, increment):
		nextLineNum = self.highlightLineNum + increment
		#scroll
		if increment == self.UP and self.highlightLineNum == 0 and self.topLineNum != 0:
			self.topLineNum += self.UP 
			return
		elif increment == self.DOWN and nextLineNum == curses.LINES and (self.topLineNum+curses.LINES) != self.nopts:
			self.topLineNum += self.DOWN
			return
		#highlight
		if increment == self.UP and (self.topLineNum != 0 or self.highlightLineNum != 0):
			self.highlightLineNum = nextLineNum
		elif increment == self.DOWN and (self.topLineNum+self.highlightLineNum+1) != self.nopts and self.highlightLineNum != curses.LINES:
			self.highlightLineNum = nextLineNum

	#return to main menu window
	def exit(self):
		decurse(self)
		curses.wrapper(main())
		
	#catch unexpected terminations
	def __del__(self):
		decurse(self)
		return obj

class text_box():
	def __init__(self):
		try:
			self.curses_available = True
			self.win = curses.newwin(*win_size)
		except curses.error:
			curses.beep()
			print "[-]Error library curses unavailable:" + str(curses.error)
			print "   download libncurses5 or above, else makefile source available:"
			print "   https://ftp.gnu.org/pub/gnu/ncurses/"
			return -1
		self.win = curses.textpad.Textbox(win)
		for e in win_attr: exec e
		return self.win

#class view_header(header, proto):
#	def __init__(self):
#		for

def raw_scan():
	s = yapps.raw_scan.sock_raw()
	screen = scroll_menu())

#exit curses window and run simple scan as script
def simple_scan(screen):
	decurse(screen)
	curses.endwin(screen)
	simple_scan.usage()
	argparse = input()
	argparse = argparse.split(' ')
	simple_scan.main(argparse)
	curses.wrapper(main())

def main_menu():
	main_menu = {}
	main_menu["Packet constructor"] = "packet_constructor()"
	main_menu["Socket constructor"] = "socket_constructor()"
	main_menu["Simple scan"] = "simeple_scan()"
	main_menu["Raw scan"] = "raw_scan()"
	main_menu["Help"] = "usage_main()"
	main_menu["Exit"] = "exit()"

	return main_menu

def main():
	global code, win_attr, win_size
	args = sys.argv[1:]
	#get and set locale-specific character encode name as str, make str code accessable globally
	locale.setlocale(locale.LC_ALL, '')
	code = locale.getpreferredencoding()
	#tuple to intialize most common ncurses attributes in Window; pass items to statement exec
	win_attr = ["curses.noecho()", "curses.cbreak()", "stdscr.keypad(1)", "curses.curs_set(1)"]
	#tuple for default textbox/shell window size; return tuple to params to pass as all args
	win_size = [20,72,2,4]
	#define ncurses window
	window = curses.initscr(*win_size)
	#Frame main interface area at fixed size
	window.box()
	menu = main_menu()
	y=3 for name, function in menu.iteritems():
		window.addstr(y,3,name)
		y += 1;
	window.addstr(y+=1, 2, "input:")
	window.addch(y+2, 2, " ")
	curses.echo()
	c = window.getstr()
	decurse(screen)
	if not c in [k for k,v in menu.iteritems()]:#bad test
		(y+=4, , "input value not found in options, try again:")
		window.getstr()
		curses.wrapper(main())
	else:
		select = menu[c]
	curses.wrapper(exec(select))


if __name__ == '__main__':
	main()
