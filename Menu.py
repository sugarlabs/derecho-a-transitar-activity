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

class Menu(gtk.Widget):
	__gsignals__ = {"run_grupo":(gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
	"back":(gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, [])}
	def __init__(self, usuario):
		gtk.Widget.__init__(self)
		self.usuario = usuario
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

	def presentacion(self, button):
		presentacion = Presentacion(self)
		self.ventana.blit(self.fondo, (0,0))
		presentacion.draw(self.ventana)
		pygame.display.update()
		while presentacion.estado:
			self.reloj.tick(35)
			while gtk.events_pending():
			    	gtk.main_iteration(False)
			G.Traduce_posiciones(self.VA, self.VH)
			presentacion.clear(self.ventana, self.fondo)
			presentacion.update()
			pygame.event.clear()
			presentacion.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
			pygame.display.update()
		imagen = os.path.join(G.IMAGENES, "Login", "fondo.jpg")
		self.fondo = pygame.transform.scale(pygame.image.load(imagen),
			G.RESOLUCION)
		self.ventana.blit(self.fondo, (0,0))
		self.botonesmenu.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana,
			self.resolucionreal), (0,0))
		pygame.display.update()

	def update(self):
		self.ventana.blit(self.fondo, (0,0))
		self.botonesmenu.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana,
			self.resolucionreal), (0,0))
		pygame.display.update()

	def emit_volver(self, button=None):
		self.estado = None
		self.emit("back")

	def run_grupo1(self, jambutton):
		self.estado = None
		self.emit("run_grupo", "grupo1")
	def run_grupo2(self, jambutton):
		self.estado = None
		self.emit("run_grupo", "grupo2")
	def run_grupo3(self, jambutton):
		self.estado = None
		self.emit("run_grupo", "grupo3")
	def run_grupo4(self, jambutton):
		self.estado = None
		self.emit("run_grupo", "grupo4")
	def run_grupo5(self, jambutton):
		self.estado = None
		self.emit("run_grupo", "grupo5")

	def handle_event_Intro(self):
		for event in pygame.event.get(pygame.KEYDOWN):
			tecla = event.key
			if tecla == pygame.K_ESCAPE:
				pygame.event.clear()
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

	def ok_intro(self, button):
		return self.emit_volver()
	def cancel_intro(self, button):
		self.estado = "Intro"

class ButtonsMenu(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		self.main = main
		pygame.sprite.OrderedUpdates.__init__(self)
		imagen = G.get_Flecha()
		salir = JAMButton("",None)
		salir.set_imagen(origen = imagen, tamanio = (100,55))
		salir.set_colores(colorbas = JAMG.get_negro(), colorcara = JAMG.get_negro())
		salir.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
		salir.set_posicion(punto = (10,10))
		salir.connect(callback = self.main.emit_volver, sonido_select = None)
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

		uno = BotonGrupo()
		uno.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
		imagen = os.path.join(G.IMAGENES, "Menu", "img1.png")
		uno.set_imagen(origen = imagen)
		uno.connect(callback = main.run_grupo1, sonido_select = None)
		self.add(uno)

		dos = BotonGrupo()
		dos.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
		imagen = os.path.join(G.IMAGENES, "Menu", "img2.png")
		dos.set_imagen(origen = imagen)
		dos.connect(callback = main.run_grupo2, sonido_select = None)
		self.add(dos)

		tres = BotonGrupo()
		tres.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
		imagen = os.path.join(G.IMAGENES, "Menu", "img3.png")
		tres.set_imagen(origen = imagen)
		tres.connect(callback = main.run_grupo3, sonido_select = None)
		self.add(tres)

		cuatro = BotonGrupo()
		cuatro.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
		imagen = os.path.join(G.IMAGENES, "Menu", "img4.png")
		cuatro.set_imagen(origen = imagen)
		cuatro.connect(callback = main.run_grupo4, sonido_select = None)
		self.add(cuatro)

		cinco = BotonGrupo()
		cinco.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
		imagen = os.path.join(G.IMAGENES, "Menu", "img5.png")
		cinco.set_imagen(origen = imagen)
		cinco.connect(callback = main.run_grupo5, sonido_select = None)
		self.add(cinco)

		presenta = BotonPresentacion()
		presenta.connect(callback = main.presentacion, sonido_select = None)
		self.add(presenta)

		sep = 50
		w,h = G.RESOLUCION
		ww, hh = dos.get_tamanio()
		dos.set_posicion( (w/2-ww/2, h/2 - hh) )
		x, y = dos.get_posicion()
		tres.set_posicion( (x + ww + sep, y) )
		uno.set_posicion( (x - ww - sep, y) )

		cuatro.set_posicion( ((w/2 - ww) - sep, y + hh + sep) )
		cinco.set_posicion( (w/2 + sep, y + hh + sep) )

		ww,hh = presenta.get_tamanio()
		presenta.set_posicion( (w-ww-10, h-hh-10) )

class BotonGrupo(JAMButton):
	def __init__(self):
		JAMButton.__init__(self, '', None)
	def set_imagen(self, origen):
		imagen = pygame.image.load(origen)
		self.final_unselect = imagen
		self.final_select = JAMG.get_my_surface_whit_border(imagen.copy(),
			(255,255,255,255), 10)
		self.image = self.final_unselect
		self.rect = self.image.get_rect()

class BotonPresentacion(JAMButton):
	def __init__(self):
		JAMButton.__init__(self, '', None)
		self.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
		imagen1 = os.path.join(G.IMAGENES, "pandilla1.png")
		self.set_imagen(origen = imagen1)
		imagen2 = os.path.join(G.IMAGENES, "pandilla2.png")
		self.final_unselect = pygame.image.load(imagen1)
		self.final_select = pygame.image.load(imagen2)
		self.image = self.final_unselect
		self.rect = self.image.get_rect()

class Presentacion(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main = main
		self.imagenes = G.get_Presentacion()
		self.siguiente = None
		self.anterior = None
		salir = None
		self.imagen_actual = None
		self.estado = True
		fuente, tamanio = JAMG.get_Font_fawn()
		w,h = G.RESOLUCION
		self.siguiente = JAMButton("Siguiente", None)
		self.siguiente.set_text(color = JAMG.get_blanco())
		self.siguiente.set_font_from_file(fuente, tamanio = 40)
		self.siguiente.set_colores(colorbas = JAMG.get_negro(), colorcara = JAMG.get_negro())
		self.siguiente.set_tamanios(tamanio = (150,0), grosorbor = 1, detalle = 1, espesor = 1)
		ww,hh = self.siguiente.get_tamanio()
		self.siguiente.set_posicion(punto = (w-ww-20,h-hh-20))
		self.siguiente.connect(callback = self.next, sonido_select = None)
		self.add(self.siguiente)
		self.anterior = JAMButton("Anterior", None)
		self.anterior.set_text(color = JAMG.get_blanco())
		self.anterior.set_font_from_file(fuente, tamanio = 40)
		self.anterior.set_colores(colorbas = JAMG.get_negro(), colorcara = JAMG.get_negro())
		self.anterior.set_tamanios(tamanio = (150,0), grosorbor = 1, detalle = 1, espesor = 1)
		ww,hh = self.anterior.get_tamanio()
		self.anterior.set_posicion(punto = (20,h-hh-20))
		self.anterior.connect (callback = self.previous, sonido_select = None)
		self.add(self.anterior)
		salir = JAMButton("Salir", None)
		salir.set_text(color = JAMG.get_blanco())
		salir.set_font_from_file(fuente, tamanio = 40)
		salir.set_colores(colorbas = JAMG.get_negro(), colorcara = JAMG.get_negro())
		salir.set_tamanios(tamanio = (150,0), grosorbor = 1, detalle = 1, espesor = 1)
		ww,hh = salir.get_tamanio()
		salir.set_posicion(punto = (w/2-ww/2,20))
		salir.connect(callback = self.volver, sonido_select = None)
		self.add(salir)
		self.imagen_actual = self.imagenes[0]
		self.main.fondo = self.imagen_actual

	def volver(self, button):
		for sprite in self.sprites():
			sprite.kill()
		self.empty()
		self.estado = False

	def next(self, button):
		indice = self.imagenes.index(self.imagen_actual)
		if indice < len(self.imagenes)-1:
			indice += 1
			self.imagen_actual = self.imagenes[indice]
			self.main.fondo = self.imagen_actual
		self.main.ventana.blit(self.main.fondo, (0,0))
		pygame.display.update()
		self.view_buttons(indice)

	def previous(self, button):
		indice = self.imagenes.index(self.imagen_actual)
		if indice > 0:
			indice -= 1
			self.imagen_actual = self.imagenes[indice]
			self.main.fondo = self.imagen_actual
		self.main.ventana.blit(self.main.fondo, (0,0))
		pygame.display.update()
		self.view_buttons(indice)

	def view_buttons(self, indice):
		if indice == len(self.imagenes)-1:
			self.remove(self.siguiente)
		elif indice == 0:
			self.remove(self.anterior)
		else:
			if not self.anterior in self.sprites():
				self.add(self.anterior)
			if not self.siguiente in self.sprites():
				self.add(self.siguiente)

