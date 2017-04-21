#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Main.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys, random, gtk, pygtk
from pygame.locals import *

import Globals as G
gc.enable()

import BiblioJAM
from BiblioJAM.JAMButton import JAMButton
import BiblioJAM.JAMGlobals as JAMG

class Menu():
	def __init__(self):
		self.ventana = None
		self.name= "Derecho a Transitar"
		self.estado= False

		# Variables del Juego
		self.fondo= None
		self.reloj= None

		# Sprites
		self.botonesmenu= None
		self.game= None

		# Escalado
		self.ventana_real= None
		self.resolucionreal= None
		self.VA= None
		self.VH= None

		self.preset()

		from BiblioJAM.JAMatrix import JAMatrix
		matrix= JAMatrix(self, self.ventana_real, self.resolucionreal)
		matrix.set_imagen_matrix(None)
		matrix.carga_game()

		self.estado= "Intro"
		self.switch()

	def run_menu(self):
		''' loop del menú. '''
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

	def presentacion(self, button):
		presentacion= Presentacion(self)
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
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()

		self.fondo= G.get_Fondo()
		self.ventana.blit(self.fondo, (0,0))
		self.botonesmenu.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()

	def update(self):
		self.ventana.blit(self.fondo, (0,0))
		self.botonesmenu.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()

	def run_T0101(self, jambutton):
		self.ventana.blit(self.fondo, (0,0))
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		from FGR_T0101 import FGR_T0101
		juego= FGR_T0101(self)
		juego.run()
		self.update()
		if juego.estado: self.run_T0102(None)

	def run_T0102(self, jambutton):
		self.ventana.blit(self.fondo, (0,0))
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		from FGR_T0102 import FGR_T0102
		juego= FGR_T0102(self)
		juego.run()
		self.update()
		#if juego.estado: self.run_T0103(None)

	'''
	def run_T0103(self, jambutton):
		self.ventana.blit(self.fondo, (0,0))
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		from FGR_T0103 import FGR_T0103
		return FGR_T0103(self)'''

	def run_T0201(self, jambutton):
		self.ventana.blit(self.fondo, (0,0))
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		from FGR_T0201 import FGR_T0201
		juego= FGR_T0201(self)
		juego.run()
		self.update()
		if juego.estado: self.run_T0202(None)

	def run_T0202(self, jambutton):
		self.ventana.blit(self.fondo, (0,0))
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		from FGR_T0202 import FGR_T0202
		juego= FGR_T0202(self)
		juego.run()
		self.update()
		#if juego.estado: self.run_T0102(None)

	def run_T0301(self, jambutton):
		self.ventana.blit(self.fondo, (0,0))
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		from FGR_T0301 import FGR_T0301
		juego= FGR_T0301(self)
		juego.run()
		self.update()
		if juego.estado: self.run_T0302(None)
	
	def run_T0302(self, jambutton):
		self.ventana.blit(self.fondo, (0,0))
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		from FGR_T0302 import FGR_T0302
		juego= FGR_T0302(self)
		juego.run()
		self.update()
		if juego.estado: self.run_T0303(None)

	def run_T0303(self, jambutton):
		self.ventana.blit(self.fondo, (0,0))
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		from FGR_T0303 import FGR_T0303
		juego= FGR_T0303(self)
		juego.run()
		self.update()
		#if juego.estado: self.run_T0102(None)

	def run_T0401(self, jambutton):
		self.ventana.blit(self.fondo, (0,0))
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		from FGR_T0401 import FGR_T0401
		juego= FGR_T0401(self)
		juego.run()
		self.update()
		if juego.estado: self.run_T0402(None)

	def run_T0402(self, jambutton):
		self.ventana.blit(self.fondo, (0,0))
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		from FGR_T0402 import FGR_T0402
		juego= FGR_T0402(self)
		juego.run()
		self.update()
		#if juego.estado: self.run_T0403(None)

	def run_T0501(self, jambutton):
		self.ventana.blit(self.fondo, (0,0))
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		from FGR_T0501 import FGR_T0501
		juego= FGR_T0501(self)
		juego.run()
		self.update()
		#if juego.estado: self.run_T0102(None)

	def switch(self):
		if self.estado== "Intro":
			self.set_event_intro()
			return self.run_menu()
	
	def handle_event_Intro(self):
		for event in pygame.event.get(pygame.KEYDOWN):
			tecla= event.key
			if tecla== pygame.K_ESCAPE:
				pygame.event.clear()
				self.run_dialog_intro(None)

	def preset(self):
		A, B= G.RESOLUCION
		self.ventana = pygame.Surface( (A, B), flags=HWSURFACE )
		self.ventana_real= pygame.display.get_surface()
		C= pygame.display.Info().current_w
		D= pygame.display.Info().current_h
		self.resolucionreal= (C,D)
		self.VA= float(C)/float(A)
		self.VH= float(D)/float(B)

	def load(self):
		self.fondo= G.get_Fondo()
		self.botonesmenu= ButtonsMenu(self)
		self.reloj = pygame.time.Clock()
		self.estado= True
	
	def set_event_intro(self):
		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN,KEYUP, USEREVENT])
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN, VIDEORESIZE, VIDEOEXPOSE, QUIT, ACTIVEEVENT])
		pygame.mouse.set_visible(True)

	def run_dialog_intro(self, button):
		from BiblioJAM.JAMDialog import JAMDialog
		dialog= JAMDialog(mensaje="¿Abandonas el Juego?", funcion_ok=self.ok_intro, funcion_cancel=self.cancel_intro)
		fuente, tamanio= JAMG.get_Font_fawn()
		dialog.set_font_from_file(fuente, tamanio= 40)
		dialog.boton_aceptar.set_font_from_file(fuente, tamanio= 25)
		dialog.boton_cancelar.set_font_from_file(fuente, tamanio= 25)
		a,b,c= JAMG.get_estilo_papel_quemado()
		dialog.set_colors_dialog(base=c, bordes=c)
		dialog.set_colors_buttons(colorbas=a, colorbor=b, colorcara=c) 
		self.estado= "Dialog"
		dialog.draw(self.ventana)
		pygame.display.update()
		while self.estado== "Dialog":
			self.reloj.tick(35)
			while gtk.events_pending():
			    	gtk.main_iteration(False)
			G.Traduce_posiciones(self.VA, self.VH)
			dialog.clear(self.ventana, self.fondo)
			dialog.update()
			pygame.event.clear()
			dialog.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()

		dialog.clear(self.ventana, self.fondo)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()

	def ok_intro(self, button):
		return self.salir()
	def cancel_intro(self, button):
		self.estado= "Intro"

	def salir(self):
		pygame.quit()
		sys.exit()

class ButtonsMenu(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		imagen= G.get_Flecha()

		salir= JAMButton("",None)
		salir.set_imagen(origen= imagen, tamanio=(100,55))
		salir.set_colores(colorbas=JAMG.get_negro(), colorcara=JAMG.get_negro())
		salir.set_tamanios(tamanio=(0,0), grosorbor=1, detalle=1, espesor=1)
		salir.set_posicion(punto= (10,10))
		salir.connect (callback= main.run_dialog_intro)
		self.add(salir)

		imagen_cartel_unselect, imagen_cartel_select= G.get_Imagen_CartelMenu()

		uno= Cartel(imagen_cartel_unselect.copy(), imagen_cartel_select.copy(), "Señales de Tránsito")
		uno.connect(callback= main.run_T0101)
		uno.rect.x, uno.rect.y= (50, 100)
		self.add(uno)

		dos= Cartel(imagen_cartel_unselect.copy(), imagen_cartel_select.copy(), "Caminando a la Escuela")
		dos.connect(callback= main.run_T0201)
		dos.rect.x, dos.rect.y= (200, 270)
		self.add(dos)

		tres= Cartel(imagen_cartel_unselect.copy(), imagen_cartel_select.copy(), "Seré Conductor")
		tres.connect(callback= main.run_T0301)
		tres.rect.x, tres.rect.y= (380, 180)
		self.add(tres)

		cuatro= Cartel(imagen_cartel_unselect.copy(), imagen_cartel_select.copy(), "Niñas y niños pasajeros!")
		cuatro.connect(callback= main.run_T0401)
		cuatro.rect.x, cuatro.rect.y= (900, 200)
		self.add(cuatro)

		cinco= Cartel(imagen_cartel_unselect.copy(), imagen_cartel_select.copy(), "Paseando en Familia")
		cinco.connect(callback= main.run_T0501)
		cinco.rect.x, cinco.rect.y= (650, 120)
		self.add(cinco)

		presenta1, presenta2= G.get_cartel_presenta()
		w,h= G.RESOLUCION
		presenta= Cartel(presenta1, presenta2, "")
		presenta.connect(callback= main.presentacion)
		ww,hh= (presenta.rect.w, presenta.rect.h)
		presenta.rect.x, presenta.rect.y= (w-ww, h-hh)
		self.add(presenta)

class Cartel(pygame.sprite.Sprite):
	def __init__(self, imagen_cartel_unselect, imagen_cartel_select, texto):
		pygame.sprite.Sprite.__init__(self)
		labels= self.get_labels(texto)
		self.final_unselect, self.final_select= (imagen_cartel_unselect, imagen_cartel_select)
		self.bliting_labels(self.final_unselect, labels)
		self.bliting_labels(self.final_select, labels)
		self.image= self.final_unselect
		self.rect= self.image.get_rect()
		self.select= False
		self.callback= False

	def get_labels(self, texto):
		from BiblioJAM.JAMLabel import JAMLabel
		labels= []
		for text in texto.split("\n"):
			label= JAMLabel(text)
			label.set_text(color=JAMG.get_azul1())
			fuente, tamanio= JAMG.get_Font_fawn()
			label.set_font_from_file(fuente, tamanio= 30)
			labels.append(label)
		return labels

	def bliting_labels(self, imagen, labels):
		x,y,w,h= imagen.get_rect()
		y+= 10
		for label in labels:
			w1,h1= label.get_tamanio()
			imagen.blit(label.image, (w/2-w1/2, y))
			y+= h1

	def connect(self, callback=None):
		self.callback= callback

	def update(self):	
		eventos_republicar= []
		eventos= pygame.event.get(pygame.MOUSEBUTTONDOWN)
		for event in eventos:
			posicion = event.pos
			if self.rect.collidepoint(posicion):
				punto= (int(posicion[0]-self.rect.x), int(posicion[1]-self.rect.y))
				color= self.image.get_at( punto )
				if color[3] != 0:
					if self.callback:
						pygame.event.clear()
						return self.callback(self)
			else:
				if not event in eventos_republicar: eventos_republicar.append(event)

		eventos= pygame.event.get(pygame.MOUSEMOTION)
		for event in eventos:
			posicion = event.pos
			if self.rect.collidepoint(posicion):
				punto= (int(posicion[0]-self.rect.x), int(posicion[1]-self.rect.y))
				color= self.image.get_at( punto )
				if color[3] != 0:
					if self.select == False:
						self.image = self.final_select
						self.select = True
			else:
				if self.select == True:
					self.image = self.final_unselect
					self.select = False
			if not event in eventos_republicar: eventos_republicar.append(event)
		for event in eventos_republicar:
			pygame.event.post(event)

class Presentacion(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main= main
		self.imagenes= G.get_Presentacion()
		siguiente= None
		anterior= None
		salir= None
		self.imagen_actual= None
		self.estado= True

		fuente, tamanio= JAMG.get_Font_fawn()
		w,h= G.RESOLUCION

		siguiente= JAMButton("Siguiente", None)
		siguiente.set_text(color=JAMG.get_blanco())
		siguiente.set_font_from_file(fuente, tamanio= 40)
		siguiente.set_colores(colorbas=JAMG.get_negro(), colorcara=JAMG.get_negro())
		siguiente.set_tamanios(tamanio=(150,0), grosorbor=1, detalle=1, espesor=1)
		ww,hh= siguiente.get_tamanio()
		siguiente.set_posicion(punto= (w-ww-20,h-hh-20))
		siguiente.connect (callback= self.next)
		self.add(siguiente)

		anterior= JAMButton("Anterior", None)
		anterior.set_text(color=JAMG.get_blanco())
		anterior.set_font_from_file(fuente, tamanio= 40)
		anterior.set_colores(colorbas=JAMG.get_negro(), colorcara=JAMG.get_negro())
		anterior.set_tamanios(tamanio=(150,0), grosorbor=1, detalle=1, espesor=1)
		ww,hh= anterior.get_tamanio()
		anterior.set_posicion(punto= (20,h-hh-20))
		anterior.connect (callback= self.previous)
		self.add(anterior)

		salir= JAMButton("Salir", None)
		salir.set_text(color=JAMG.get_blanco())
		salir.set_font_from_file(fuente, tamanio= 40)
		salir.set_colores(colorbas=JAMG.get_negro(), colorcara=JAMG.get_negro())
		salir.set_tamanios(tamanio=(150,0), grosorbor=1, detalle=1, espesor=1)
		ww,hh= salir.get_tamanio()
		salir.set_posicion(punto= (w/2-ww/2,20))
		salir.connect (callback= self.volver)
		self.add(salir)

		self.imagen_actual= self.imagenes[0]
		self.main.fondo= self.imagen_actual

	def volver(self, button):
		for sprite in self.sprites():
			sprite.kill()
		self.empty()
		self.estado= False

	def next(self, button):
		try:
			indice= self.imagenes.index(self.imagen_actual)
			if indice < len(self.imagenes)-1:
				self.imagen_actual= self.imagenes[indice+1]
				self.main.fondo= self.imagen_actual
			else:
				self.imagen_actual= self.imagenes[0]
			self.main.ventana.blit(self.main.fondo, (0,0))
			pygame.display.update()
		except:
			pass

	def previous(self, button):
		try:
			indice= self.imagenes.index(self.imagen_actual)
			if indice > 1:
				self.imagen_actual= self.imagenes[indice-1]
				self.main.fondo= self.imagen_actual
			else:
				self.imagen_actual= self.imagenes[-1]
			self.main.ventana.blit(self.main.fondo, (0,0))
			pygame.display.update()
		except:
			pass
	
