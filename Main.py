#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Main.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame
import gc
import sys
import gtk
import gobject
from pygame.locals import *
import Globals as G
gc.enable()
import BiblioJAM
from BiblioJAM.JAMButton import JAMButton
import BiblioJAM.JAMGlobals as JAMG

class Main(gtk.Widget):
	__gsignals__ = {"run":(gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, [])}
	def __init__(self):
		gtk.Widget.__init__(self)
		self.ventana = None
		self.estado = False
		self.fondo = None
		self.reloj = None
		self.botonesmenu = None
		self.ventana_real = None
		self.resolucionreal = None
		self.VA = None
		self.VH = None
		self.load()
		self.estado = "Intro"

	def run(self):
		self.ventana.blit(self.fondo, (0,0))
		self.botonesmenu.draw(self.ventana)
		pygame.display.update()
		while self.estado == "Intro":
			self.reloj.tick(35)
			while gtk.events_pending():
			    	gtk.main_iteration(False)
			G.Traduce_posiciones(self.VA, self.VH)
			self.botonesmenu.clear(self.ventana, self.fondo)
			self.botonesmenu.update()
			self.handle_event_Intro()
			pygame.event.clear()
			self.botonesmenu.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
			pygame.display.update()

	def run_game(self, button):
		self.estado = None
		self.emit("run")
	
	def handle_event_Intro(self):
		for event in pygame.event.get(pygame.KEYDOWN):
			tecla = event.key
			if tecla == pygame.K_ESCAPE:
				return self.run_dialog_intro(None)

	def load(self):
		pygame.display.set_mode( (0,0), pygame.DOUBLEBUF | pygame.FULLSCREEN, 0)
		A, B = G.RESOLUCION
		self.ventana = pygame.Surface( (A, B), flags=HWSURFACE )
		self.ventana_real = pygame.display.get_surface()
		C = pygame.display.Info().current_w
		D = pygame.display.Info().current_h
		self.resolucionreal = (C,D)
		self.VA = float(C)/float(A)
		self.VH = float(D)/float(B)
		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION,
			JOYBUTTONUP, JOYBUTTONDOWN, KEYUP, USEREVENT])
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN,
			KEYDOWN, VIDEORESIZE, VIDEOEXPOSE, QUIT, ACTIVEEVENT])
		pygame.mouse.set_visible(True)
		self.fondo = G.get_Fondo_Inicial()
		self.botonesmenu = ButtonsMenu(self)
		self.reloj = pygame.time.Clock()

	def run_dialog_intro(self, button):
		from BiblioJAM.JAMDialog import JAMDialog
		dialog = JAMDialog(mensaje = "¿Abandonas el Juego?",
		funcion_ok = self.ok_intro, funcion_cancel = self.cancel_intro)
		fuente, tamanio = JAMG.get_Font_fawn()
		dialog.set_font_from_file(fuente, tamanio = 40)
		dialog.boton_aceptar.set_font_from_file(fuente, tamanio = 25)
		dialog.boton_cancelar.set_font_from_file(fuente, tamanio = 25)
		a,b,c = JAMG.get_estilo_papel_quemado()
		dialog.set_colors_dialog(base = c, bordes = c)
		dialog.set_colors_buttons(colorbas = a, colorbor = b, colorcara = c) 
		self.estado = "Dialog"
		dialog.draw(self.ventana)
		pygame.display.update()
		while self.estado == "Dialog":
			self.reloj.tick(35)
			while gtk.events_pending():
			    	gtk.main_iteration(False)
			G.Traduce_posiciones(self.VA, self.VH)
			dialog.clear(self.ventana, self.fondo)
			dialog.update()
			pygame.event.clear()
			dialog.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
			pygame.display.update()
		dialog.clear(self.ventana, self.fondo)
		self.ventana_real.blit(pygame.transform.scale(self.ventana,
			self.resolucionreal), (0,0))
		pygame.display.update()

	def ok_intro(self, button):
		return self.salir()
	def cancel_intro(self, button):
		self.estado = "Intro"
	def salir(self):
		pygame.quit()
		sys.exit()

class ButtonsMenu(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		imagen = G.get_Flecha()
		salir = JAMButton("",None)
		salir.set_imagen(origen = imagen, tamanio = (100,55))
		salir.set_colores(colorbas = JAMG.get_negro(), colorcara = JAMG.get_negro())
		salir.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
		salir.set_posicion(punto = (10,10))
		salir.connect(callback = main.run_dialog_intro)
		self.add(salir)
		jugar = JAMButton("",None)
		jugar.set_imagen(origen = imagen, tamanio = (100,55))
		jugar.set_colores(colorbas = JAMG.get_negro(), colorcara=JAMG.get_negro())
		jugar.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
		w,h = G.RESOLUCION
		ww, hh = jugar.get_tamanio()
		jugar.set_posicion(punto = (w-ww-10,h-hh-10))
		jugar.connect (callback = main.run_game)
		self.add(jugar)
		jugar.final_select = pygame.transform.flip(jugar.final_select, True, False)
		jugar.final_unselect = pygame.transform.flip(jugar.final_unselect, True, False )
		jugar.image = jugar.final_unselect.copy()

