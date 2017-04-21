#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Main.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame
import os
import gc
import sys
import random
import gtk
import gobject
from pygame.locals import *
import Globals as G
gc.enable()
import BiblioJAM
from BiblioJAM.JAMButton import JAMButton
import BiblioJAM.JAMGlobals as JAMG

class Grupos(gtk.Widget):
	__gsignals__ = {"run_game":(gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
	"back":(gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, [])}
	def __init__(self, grupo, usuario):
		gtk.Widget.__init__(self)
		self.usuario = usuario
		self.grupo = grupo
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
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()

	def update(self):
		self.ventana.blit(self.fondo, (0,0))
		self.botonesmenu.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()

	def emit_volver(self, button=None):
		self.estado = None
		self.emit("back")

	# Juegos Grupo 1
	def run_game11(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0101")
	def run_game12(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0102")
	def run_game13(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0103")
	# Juegos Grupo 2
	def run_game21(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0201")
	def run_game22(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0202")
	def run_game24(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0204")
	# Juegos Grupo 3
	def run_game31(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0301")
	def run_game32(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0302")
	def run_game33(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0303")
	# Juegos Grupo 4
	def run_game41(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0401")
	def run_game42(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0402")
	# Juegos Grupo 5
	def run_game51(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0501")
	def run_game52(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0502")
	def run_game53(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0503")
	def run_game54(self, jambutton):
		self.estado = None
		self.emit("run_game", "FGR_T0504")

	def handle_event_Intro(self):
		for event in pygame.event.get(pygame.KEYDOWN):
			tecla = event.key
			if tecla == pygame.K_ESCAPE:
				pygame.event.clear()
				#self.run_dialog_intro(None)
				self.emit_volver(None)

	def load(self):
		A, B = G.RESOLUCION
		self.ventana = pygame.Surface( (A, B), flags=HWSURFACE )
		self.ventana_real = pygame.display.get_surface()
		C = pygame.display.Info().current_w
		D = pygame.display.Info().current_h
		self.resolucionreal = (C,D)
		self.VA = float(C)/float(A)
		self.VH = float(D)/float(B)
		imagen = os.path.join(G.IMAGENES, "Login", "fondo.jpg")
		self.fondo = pygame.transform.scale(pygame.image.load(imagen), G.RESOLUCION)
		self.botonesmenu = ButtonsMenu(self)
		self.reloj = pygame.time.Clock()
		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION,
			JOYBUTTONUP, JOYBUTTONDOWN,KEYUP, USEREVENT])
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN,
			KEYDOWN, VIDEORESIZE, VIDEOEXPOSE, QUIT, ACTIVEEVENT])
		pygame.mouse.set_visible(True)

class ButtonsMenu(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		imagen = G.get_Flecha()
		salir = JAMButton("",None)
		salir.set_imagen(origen = imagen, tamanio = (100,55))
		salir.set_colores(colorbas = JAMG.get_negro(), colorcara = JAMG.get_negro())
		salir.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
		salir.set_posicion(punto = (10,10))
		salir.connect(callback = main.emit_volver, sonido_select = None)
		self.add(salir)

		imagen = main.usuario['personaje']
		user = JAMButton(main.usuario['nombre'],None)
		user.set_imagen(origen = imagen, tamanio = (60,60))
		user.set_colores(colorbas = (0,153,255,255),
			colorbor = (0,153,255,255), colorcara = (0,153,255,255))
		user.set_tamanios(tamanio = (80,80), grosorbor = 1, detalle = 1, espesor = 1)
		ww, hh = user.get_tamanio()
		w,h = G.RESOLUCION
		user.set_posicion(punto = (w - ww - 10,10))
		user.connect(callback = None, sonido_select = None)
		self.add(user)

		if main.grupo == "grupo1":
			grupo = BotonJuego()
			grupo.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "Menu", "img1.png")
			grupo.set_imagen(origen = imagen)
			grupo.final_select = grupo.final_unselect
			grupo.connect(callback = None, sonido_select = None)
			self.add(grupo)

			uno = BotonJuego()
			uno.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "capturas", "101.jpg")
			uno.set_imagen(origen = imagen)
			uno.connect(callback = main.run_game11, sonido_select = None)
			self.add(uno)

			dos = BotonJuego()
			dos.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "capturas", "102.jpg")
			dos.set_imagen(origen = imagen)
			dos.connect(callback = main.run_game12, sonido_select = None)
			self.add(dos)

			tres = BotonJuego()
			tres.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "capturas", "103.jpg")
			tres.set_imagen(origen = imagen)
			tres.connect(callback = main.run_game13, sonido_select = None)
			self.add(tres)

			cuatro = BotonJuego()
			cuatro.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			#imagen = os.path.join(G.IMAGENES, "capturas", "104.jpg")
			#cuatro.set_imagen(origen = imagen)
			cuatro.connect(callback = None, sonido_select = None)
			#self.add(cuatro)

		if main.grupo == "grupo2":
			grupo = BotonJuego()
			grupo.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "Menu", "img2.png")
			grupo.set_imagen(origen = imagen)
			grupo.final_select = grupo.final_unselect
			grupo.connect(callback = None, sonido_select = None)
			self.add(grupo)

			uno = BotonJuego()
			uno.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "capturas", "201.jpg")
			uno.set_imagen(origen = imagen)
			uno.connect(callback = main.run_game21, sonido_select = None)
			self.add(uno)

			dos = BotonJuego()
			dos.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "capturas", "202.jpg")
			dos.set_imagen(origen = imagen)
			dos.connect(callback = main.run_game22, sonido_select = None)
			self.add(dos)

			tres = BotonJuego()
			tres.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			#imagen = os.path.join(G.IMAGENES, "capturas", "203.jpg")
			#tres.set_imagen(origen = imagen)
			#tres.connect(callback = None, sonido_select = None)
			#self.add(tres)

			cuatro = BotonJuego()
			cuatro.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "capturas", "204.jpg")
			cuatro.set_imagen(origen = imagen)
			cuatro.connect(callback = main.run_game24, sonido_select = None)
			self.add(cuatro)

		if main.grupo == "grupo3":
			grupo = BotonJuego()
			grupo.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "Menu", "img3.png")
			grupo.set_imagen(origen = imagen)
			grupo.final_select = grupo.final_unselect
			grupo.connect(callback = None, sonido_select = None)
			self.add(grupo)

			uno = BotonJuego()
			uno.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "capturas", "301.jpg")
			uno.set_imagen(origen = imagen)
			uno.connect(callback = main.run_game31, sonido_select = None)
			self.add(uno)

			dos = BotonJuego()
			dos.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "capturas", "302.jpg")
			dos.set_imagen(origen = imagen)
			dos.connect(callback = main.run_game32, sonido_select = None)
			self.add(dos)

			tres = BotonJuego()
			tres.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "capturas", "303.jpg")
			tres.set_imagen(origen = imagen)
			tres.connect(callback = main.run_game33, sonido_select = None)
			self.add(tres)

			cuatro = BotonJuego()
			cuatro.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			#imagen = os.path.join(G.IMAGENES, "capturas", "304.jpg")
			#cuatro.set_imagen(origen = imagen)
			#cuatro.connect(callback = None, sonido_select = None)
			#self.add(cuatro)

		if main.grupo == "grupo4":
			grupo = BotonJuego()
			grupo.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "Menu", "img4.png")
			grupo.set_imagen(origen = imagen)
			grupo.final_select = grupo.final_unselect
			grupo.connect(callback = None, sonido_select = None)
			self.add(grupo)

			uno = BotonJuego()
			uno.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "capturas", "401.jpg")
			uno.set_imagen(origen = imagen)
			uno.connect(callback = main.run_game41, sonido_select = None)
			self.add(uno)

			dos = BotonJuego()
			dos.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "capturas", "402.jpg")
			dos.set_imagen(origen = imagen)
			dos.connect(callback = main.run_game42, sonido_select = None)
			self.add(dos)

			tres = BotonJuego()
			tres.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			#imagen = os.path.join(G.IMAGENES, "capturas", "403.jpg")
			#tres.set_imagen(origen = imagen)
			#tres.connect(callback = None, sonido_select = None)
			#self.add(tres)

			cuatro = BotonJuego()
			cuatro.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			#imagen = os.path.join(G.IMAGENES, "capturas", "404.jpg")
			#cuatro.set_imagen(origen = imagen)
			#cuatro.connect(callback = None, sonido_select = None)
			#self.add(cuatro)

		if main.grupo == "grupo5":
			grupo = BotonJuego()
			grupo.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "Menu", "img5.png")
			grupo.set_imagen(origen = imagen)

			grupo.connect(callback = None, sonido_select = None)
			self.add(grupo)

			uno = BotonJuego()
			uno.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "capturas", "501.jpg")
			uno.set_imagen(origen = imagen)
			uno.connect(callback = main.run_game51, sonido_select = None)
			self.add(uno)

			dos = BotonJuego()
			dos.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			imagen = os.path.join(G.IMAGENES, "capturas", "502.jpg")
			dos.set_imagen(origen = imagen)
			dos.connect(callback = main.run_game52, sonido_select = None)
			self.add(dos)

			tres = BotonJuego()
			tres.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			#imagen = os.path.join(G.IMAGENES, "capturas", "503.jpg")
			#tres.set_imagen(origen = imagen)
			#tres.connect(callback = main.run_game53, sonido_select = None)
			#self.add(tres)

			cuatro = BotonJuego()
			cuatro.set_tamanios(tamanio = (264,264), grosorbor = 1, detalle = 1, espesor = 1)
			#imagen = os.path.join(G.IMAGENES, "capturas", "504.jpg")
			#cuatro.set_imagen(origen = imagen)
			#cuatro.connect(callback = main.run_game54, sonido_select = None)
			#self.add(cuatro)

		sep = 50
		w,h = G.RESOLUCION
		centrox = w/2
		centroy = h/2
		uno.set_posicion( (centrox - sep*3, centroy - uno.get_tamanio()[1]) )
		dos.set_posicion( (uno.get_posicion()[0] + uno.get_tamanio()[0] + sep,
			centroy - uno.get_tamanio()[1]) )
		tres.set_posicion( (uno.get_posicion()[0], centroy + sep) )
		cuatro.set_posicion( (tres.get_posicion()[0] + tres.get_tamanio()[0] + sep,
			centroy + sep) )
		grupo.set_posicion( (uno.get_posicion()[0] - uno.get_tamanio()[0] - sep,
			uno.get_posicion()[1] + uno.get_tamanio()[1]/2) )

class BotonJuego(JAMButton):
	def __init__(self):
		JAMButton.__init__(self, '', None)
	def set_imagen(self, origen):
		imagen = pygame.transform.scale(pygame.image.load(origen), (264,264))
		self.final_unselect = imagen
		self.final_select = JAMG.get_my_surface_whit_border(imagen.copy(), (255,255,255,255), 10)
		self.image = self.final_unselect
		self.rect = self.image.get_rect()

