#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, gtk, pygtk, gobject, sys, socket, pygame

from pygame.locals import *
from sugar.activity import activity
from Main import Main
import Globals as G

class Derecho_a_Transitar(activity.Activity):
	def __init__(self, handle):
	        activity.Activity.__init__(self, handle, False)
		self.eventbox= PygameCanvas()
		self.set_canvas(self.eventbox)

		self.add_events(gtk.gdk.ALL_EVENTS_MASK)
		self.connect("destroy", self.salir)

		self.show_all()
		self.realize()

	       	os.putenv('SDL_WINDOWID', str(self.eventbox.socket.get_id()))
		gobject.idle_add(self.get_run_game)

	def get_run_game(self):
		print "Lanzando Derecho a Transitar."
		pygame.init()
		Main()
		return False

	def salir(self, widget):
		lambda w: gtk.main_quit()
		sys.exit()

class PygameCanvas(gtk.EventBox):
	def __init__(self):
		gtk.EventBox.__init__(self)
		self.set_flags(gtk.CAN_FOCUS)
		self.setup_events()
		self.socket = gtk.Socket()
		self.add(self.socket)
		self.button_state = [0,0,0]
        	self.mouse_pos = (0,0)

	def setup_events(self):
		self.set_events(gtk.gdk.KEY_PRESS | gtk.gdk.EXPOSE | gtk.gdk.POINTER_MOTION_MASK | \
		            gtk.gdk.POINTER_MOTION_HINT_MASK | gtk.gdk.BUTTON_MOTION_MASK | \
		            gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK)
	
		self.connect("key-press-event", self.keypress)
		self.connect("button_press_event", self.mousedown)
		self.connect("motion-notify-event", self.mousemotion)
		self.connect('expose-event', self.expose)
		self.connect('configure-event', self.resize)
		self.connect("focus-in-event", self.set_focus)

	def keypress(self, selfmain, event, parametros= None):
		nombre= gtk.gdk.keyval_name(event.keyval)
		tipo= pygame.KEYDOWN
		unic= str.lower(nombre)
		valor= nombre
		try:
			valor= getattr(pygame, "K_%s" % (str.upper(nombre)))
		except:
			print "no has programado la traduccion de esta tecla: ", nombre
			return False
		evt = pygame.event.Event(tipo, key= valor, unicode= unic, mod=None)
		try:
			pygame.event.post(evt)
		except:
			pass
		return False

	def mousedown(self, widget, event):
		evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button= event.button, pos=(int(event.x), int(event.y)))
		try:
			pygame.event.post(evt)
		except:
			pass
		return False

	def mousemotion(self, widget, event):
		x, y, state = event.window.get_pointer()
        	rel = (x - self.mouse_pos[0], y - self.mouse_pos[1])
        	self.mouse_pos= (int(x), int(y))
        	self.button_state = [
            	state & gtk.gdk.BUTTON1_MASK and 1 or 0,
            	state & gtk.gdk.BUTTON2_MASK and 1 or 0,
            	state & gtk.gdk.BUTTON3_MASK and 1 or 0,
        	]
		evt = pygame.event.Event(pygame.MOUSEMOTION, pos= self.mouse_pos, rel=rel, buttons=self.button_state)
		try:
			pygame.event.post(evt)
		except:
			pass
		return False

	def expose(self, event, widget):
		if pygame.display.get_init():
			try:
				pygame.event.post(pygame.event.Event(pygame.VIDEOEXPOSE))
			except:
				pass
		return False # continue processing

	def resize(self, widget, event):
		evt = pygame.event.Event(pygame.VIDEORESIZE, size=(event.width,event.height), width=event.width, height=event.height)
		try:
			pygame.event.post(evt)
		except:
			pass
		return False # continue processing

	def set_focus(self, container, widget):
		try:
			pygame.display.update()
		except:
			pass
		self.queue_draw()
		return False

# -----------------------------------------------
# 	******** El Juego en gtk ********
# -----------------------------------------------
class VentanaGTK(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_title("Derecho A Transitar")
		self.fullscreen()

                self.socket = gtk.Socket()
                self.add(self.socket)

		self.gtkplug= gtkplug()
		self.socket.add_id(self.gtkplug.get_id())	
		
		self.add_events(gtk.gdk.ALL_EVENTS_MASK)
		self.connect("destroy", self.salir)
		self.connect("set-focus-child", self.refresh)
		self.show_all()

	def refresh(self, widget, datos):
		try:
			pygame.display.update()
		except:
			pass
		self.queue_draw()
		return True

	def salir(self, widget):
		pygame.quit()
		sys.exit()

class gtkplug(gtk.Plug):
	def __init__(self):
		gtk.Plug.__init__(self, 0L)
		self.set_title("Ventana de Plug")
		self.resolucion= (self.get_screen().get_width(),self.get_screen().get_height())
		self.eventbox= PygameCanvas()
		self.add(self.eventbox)
		self.ventana= None
		self.show_all()

		self.connect("embedded", self.embed_event)

	       	os.putenv('SDL_WINDOWID', str(self.eventbox.socket.get_id()))
		gobject.idle_add(self.get_run_game)

	def get_run_game(self):
		pygame.init()
        	self.eventbox.socket.window.set_cursor(None)
		Main()
		return False

	def embed_event(self, widget):
	    	print "Juego embebido"

if __name__=="__main__":
	VentanaGTK()
	gtk.main()
