#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gobject
import sys
import socket
import pygame
import shelve

from pygame.locals import *
from sugar.activity import activity
import Globals as G

class Derecho_a_Transitar(activity.Activity):
	def __init__(self, handle):
		activity.Activity.__init__(self, handle, False)
		self.set_title("Derecho A Transitar")
		self.socket = gtk.Socket()
		self.set_canvas(self.socket)
		self.gtkplug = gtkplug()
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
		nombre = gtk.gdk.keyval_name(event.keyval)
		tipo = pygame.KEYDOWN
		unic = str.lower(nombre)
		valor = nombre
		try:
			valor = getattr(pygame, "K_%s" % (str.upper(nombre)))
		except:
			print "no has programado la traduccion de esta tecla: ", nombre
			return False
		evt = pygame.event.Event(tipo, key = valor, unicode = unic, mod = None)
		try:
			pygame.event.post(evt)
		except:
			pass
		return False

	def mousedown(self, widget, event):
		evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN,
		button = event.button, pos=(int(event.x), int(event.y)))
		try:
			pygame.event.post(evt)
		except:
			pass
		return False

	def mousemotion(self, widget, event):
		x, y, state = event.window.get_pointer()
        	rel = (x - self.mouse_pos[0], y - self.mouse_pos[1])
        	self.mouse_pos = (int(x), int(y))
        	self.button_state = [
            	state & gtk.gdk.BUTTON1_MASK and 1 or 0,
            	state & gtk.gdk.BUTTON2_MASK and 1 or 0,
            	state & gtk.gdk.BUTTON3_MASK and 1 or 0,
        	]
		evt = pygame.event.Event(pygame.MOUSEMOTION, pos = self.mouse_pos,
			rel = rel, buttons = self.button_state)
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
		evt = pygame.event.Event(pygame.VIDEORESIZE,
			size = (event.width,event.height),
			width = event.width, height=event.height)
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

class VentanaGTK(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_title("Derecho A Transitar")
		self.fullscreen()
		self.socket = gtk.Socket()
		self.add(self.socket)
		self.gtkplug = gtkplug()
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
		self.resolucion = (self.get_screen().get_width(),self.get_screen().get_height())
		self.eventbox = PygameCanvas()
		self.add(self.eventbox)
		self.ventana = None
		self.show_all()
		self.usuario = None
		self.connect("embedded", self.embed_event)
		os.putenv('SDL_WINDOWID', str(self.eventbox.socket.get_id()))
		gobject.idle_add(self.run_derecho_a_transitar)

	def embed_event(self, widget):
	    	pass

	def run_derecho_a_transitar(self):
		''' Presentacion inicial.'''
		pygame.init()
		self.eventbox.socket.window.set_cursor(None)
		from Main import Main
		main = Main()
		main.connect("run", self.run_login)
		#main.connect("run", self.run_menu)
		main.run()
		return False

	def run_login(self, widget):
		# Seleccionar un Usuario o llama a crear uno nuevo.
		from Login import Login
		login = Login()
		login.connect("crear_usuario", self.crear_usuario)
		login.connect("load_usuario", self.run_menu)
		login.run()
		return False

	def crear_usuario(self, widget):
		# Crear un Nuevo Usuario y pasa al menú o vuelve al login.
		widget.destroy()
		from Crear_Usuario import Crear_Usuario
		crear_usuario = Crear_Usuario()
		crear_usuario.connect("back", self.run_login)
		crear_usuario.connect("run", self.run_menu)
		crear_usuario.run()
		return False

	def run_menu(self, widget, usuario = None):
		# Menú con grupos de actividades.
		# Se llama desde login y crear usuario.
		if usuario: self.usuario = usuario
		filename = os.path.join(G.USERS, self.usuario['nombre'])
		d = shelve.open(filename)
		d['nombre'] = self.usuario['nombre']
		d['edad'] = self.usuario['edad']
		d['escuela'] = self.usuario['escuela']
		d['clase'] = self.usuario['clase']
		d['departamento'] = self.usuario['departamento']
		d['personaje'] = self.usuario['personaje']
		d.close()
		os.chmod(filename, 0666)
		widget.destroy()
		from Menu import Menu
		menu = Menu(self.usuario)
		menu.connect("run_grupo", self.run_grupo)
		menu.connect("back", self.run_login)
		menu.run()
		return False

	def run_grupo(self, widget, grupo, puntos = None):
		# Menú de actividades para grupos.
		widget.destroy()
		if puntos: print ">>>>", puntos # Guardar por actividad
		from Grupos import Grupos
		grupos = Grupos(grupo, self.usuario)
		grupos.connect("back", self.run_menu)
		grupos.connect("run_game", self.run_game)
		grupos.run()
		return False

	def run_game(self, widget, game):
		# Corre un juego.
		widget.destroy()
		if game == "FGR_T0101":
			from FGR_T0101 import FGR_T0101
			juego = FGR_T0101(self.usuario)
		elif game == "FGR_T0102":
			from FGR_T0102 import FGR_T0102
			juego = FGR_T0102(self.usuario)
		elif game == "FGR_T0103":
			from FGR_T0103 import FGR_T0103
			juego = FGR_T0103(self.usuario)
		elif game == "FGR_T0201":
			from FGR_T0201 import FGR_T0201
			juego = FGR_T0201(self.usuario)
		elif game == "FGR_T0202":
			from FGR_T0202 import FGR_T0202
			juego = FGR_T0202(self.usuario)
		#elif game == "FGR_T0203":
		#	from FGR_T0203 import FGR_T0203
		#	juego = FGR_T0203(self.usuario)
		elif game == "FGR_T0204":
			from FGR_T0204 import FGR_T0204
			juego = FGR_T0204(self.usuario)
		elif game == "FGR_T0301":
			from FGR_T0301 import FGR_T0301
			juego = FGR_T0301(self.usuario)
		elif game == "FGR_T0302":
			from FGR_T0302 import FGR_T0302
			juego = FGR_T0302(self.usuario)
		elif game == "FGR_T0303":
			from FGR_T0303 import FGR_T0303
			juego = FGR_T0303(self.usuario)
		elif game == "FGR_T0401":
			from FGR_T0401 import FGR_T0401
			juego = FGR_T0401(self.usuario)
		elif game == "FGR_T0402":
			from FGR_T0402 import FGR_T0402
			juego = FGR_T0402(self.usuario)
		elif game == "FGR_T0501":
			from FGR_T0501 import FGR_T0501
			juego = FGR_T0501(self.usuario)
		elif game == "FGR_T0502":
			from FGR_T0502 import FGR_T0502
			juego = FGR_T0502(self.usuario)
		#elif game == "FGR_T0503":
		#	from FGR_T0503 import FGR_T0503
		#	juego = FGR_T0503(self.usuario)
		#elif game == "FGR_T0504":
		#	from FGR_T0504 import FGR_T0504
		#	juego = FGR_T0504(self.usuario)
		juego.connect("run_grupo", self.run_grupo)
		juego.run()
		return False

if __name__=="__main__":
	VentanaGTK()
	gtk.main()
