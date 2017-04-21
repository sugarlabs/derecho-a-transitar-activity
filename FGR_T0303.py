#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   FGR_T0303.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame
import gc
import gobject
import sys
import random
import gtk
from pygame.locals import *
import Globals as G
gc.enable()
import BiblioJAM
from BiblioJAM.JAMButton import JAMButton
from BiblioJAM.JAMLabel import JAMLabel
import BiblioJAM.JAMGlobals as JAMG

class FGR_T0303(gtk.Widget):
	__gsignals__ = {"run_grupo":(gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING,gobject.TYPE_INT))}
	def __init__(self, usuario):
		gtk.Widget.__init__(self)
		self.usuario = usuario
		self.ventana = None
		self.nombre = "¡Ciclistas y peatones precavidos y expertos!"
		self.estado = False
		# Variables del Juego
		self.fondo= None
		self.reloj= None
		self.puntos= 0

		# Sprites
		self.textos= None
		self.botonesmenu= None
		self.controles= None
		self.seniales= None
		self.senial_select= None

		# sonidos
		self.sonido_error= None
		self.sonido_exito= None
		self.sound_select= None

		# Escalado
		self.ventana_real= None
		self.resolucionreal= None
		self.VA= None
		self.VH= None
		self.load()
		self.estado = "Intro"

	def run(self):
		if self.estado== "Intro":
			self.controles.stop()
			self.fondo = self.fondo1
			return self.run_menu()
		elif self.estado== "Game":
			self.puntos= 0
			self.fondo = self.fondo2
			self.reset()
			return self.run_juego()

	def run_menu(self):
		self.ventana.blit(self.fondo, (0,0))
		self.textos.draw(self.ventana)
		self.botonesmenu.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		while self.estado == "Intro":
			self.reloj.tick(35)
			while gtk.events_pending():
			    	gtk.main_iteration(False)
			G.Traduce_posiciones(self.VA, self.VH)
			self.textos.clear(self.ventana, self.fondo)
			self.botonesmenu.clear(self.ventana, self.fondo)
			self.botonesmenu.update()
			self.handle_event_Intro()
			pygame.event.clear()
			self.textos.draw(self.ventana)
			self.botonesmenu.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()

	def run_juego(self):
		pygame.mixer.music.pause()
		self.ventana.blit(self.fondo, (0,0))
		self.seniales.draw(self.ventana)
		self.controles.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		while self.estado == "Game":
			self.reloj.tick(35)
			while gtk.events_pending():
			    	gtk.main_iteration(False)
			G.Traduce_posiciones(self.VA, self.VH)
			self.seniales.clear(self.ventana, self.fondo)
			self.controles.clear(self.ventana, self.fondo)
			self.seniales.update()
			self.controles.update()
			#self.handle_event_Game()
			pygame.event.clear()
			self.seniales.draw(self.ventana)
			self.controles.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()

	def reset(self):
		self.puntos= 0
		self.controles.init()
		self.seniales.init()

	def deja_en(self, boton):
		if boton.valor:
			self.sonido_exito.play()
			self.puntos+= 10
			self.controles.actualiza_puntos()
			self.seniales.next()
		else:
			self.sonido_error.play()
			self.controles.cronometro.cron.segundos_transcurridos+= 5

	def victory(self):
		pygame.mixer.music.unpause()
		self.controles.stop()
		self.puntos+= (10*self.controles.cronometro.get_tiempo_restante())
		self.controles.actualiza_puntos()
		self.ventana.blit(self.fondo, (0,0))
		self.seniales.draw(self.ventana)
		self.controles.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		pygame.time.wait(1000)
		text1= "Muy bien, completaron el nivel “Seré conductor”, ahora sí tienen"
		text2= "todos los conocimientos para circular correctamente en su bici."
		mensaje= Mensaje(self, "Victory", text1, text2)
		self.fondo= self.fondo1
		self.ventana.blit(self.fondo, (0,0))
		mensaje.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		while mensaje.estado == True:
			self.reloj.tick(35)
			mensaje.clear(self.ventana, self.fondo)
			mensaje.update()
			mensaje.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()
		pygame.time.wait(6000)
		return self.salir(True)

	def game_over(self, jamcron):
		pygame.mixer.music.unpause()
		self.controles.update() # para actualizar imagen de progressbar del reloj
		self.controles.stop()
		self.controles.actualiza_puntos()
		self.ventana.blit(self.fondo, (0,0))
		self.seniales.draw(self.ventana)
		self.controles.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		pygame.time.wait(1000)
		text1= "Te han Faltado Unos Segundos Para Completar la Actividad."
		text2= "Prueba Nuevamente."
		mensaje= Mensaje(self, "End", text1, text2)
		self.fondo= self.fondo1
		self.ventana.blit(self.fondo, (0,0))
		mensaje.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		while mensaje.estado == True:
			self.reloj.tick(35)
			mensaje.clear(self.ventana, self.fondo)
			mensaje.update()
			mensaje.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()
		pygame.time.wait(6000)
		return self.salir(False)

	# ----------- SETEOS -------------
	def load(self):
		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION,
			JOYBUTTONUP, JOYBUTTONDOWN, KEYUP, USEREVENT])
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN,
			KEYDOWN, VIDEORESIZE, VIDEOEXPOSE, QUIT, ACTIVEEVENT])
		pygame.mouse.set_visible(True)
		A, B= G.RESOLUCION
		self.ventana = pygame.Surface( (A, B), flags=HWSURFACE )
		self.ventana_real= pygame.display.get_surface()
		C= pygame.display.Info().current_w
		D= pygame.display.Info().current_h
		self.resolucionreal= (C,D)
		self.VA= float(C)/float(A)
		self.VH= float(D)/float(B)
		self.fondo1, self.fondo2= G.get_Fondos_FGR_T0303()
		self.textos= Textos_Intro()
		self.botonesmenu= ButtonsMenu(self)
		from Globals import Controles
		self.controles= Controles(self)
		self.seniales= Seniales(self)
		self.sonido_error, self.sonido_exito= G.get_Sonidos()
		self.sound_select= JAMG.get_sound_select()
		self.reloj = pygame.time.Clock()

	# ----------- EVENTOS en MENU ---------------
	def handle_event_Intro(self):
		for event in pygame.event.get(pygame.KEYDOWN):
			tecla= event.key
			if tecla== pygame.K_ESCAPE:
				pygame.event.clear()
				#return self.run_dialog_intro(None)
				return self.salir()

	def run_Instruc(self):
		self.fondo= G.get_instruc("303")
		self.ventana.blit(self.fondo, (0,0))
		self.botonesmenu.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		while self.estado== "Instruc":
			self.reloj.tick(35)
			while gtk.events_pending():
			    	gtk.main_iteration(False)
			G.Traduce_posiciones(self.VA, self.VH)
			self.botonesmenu.clear(self.ventana, self.fondo)
			self.botonesmenu.update()
			pygame.event.clear()
			self.botonesmenu.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()

	'''
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
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
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
		return self.salir(False)
	def cancel_intro(self, button):
		self.estado= "Intro"'''
	# ----------- EVENTOS en MENU ---------------

	'''
	# ----------- EVENTOS en JUEGO ---------------
	def handle_event_Game(self):
		for event in pygame.event.get(pygame.KEYDOWN):
			tecla= event.key
			if tecla== pygame.K_ESCAPE:
				pygame.event.clear()
				return self.run_dialog_game(None)'''
					
	def run_dialog_game(self, button):
		self.controles.stop()
		from BiblioJAM.JAMDialog import JAMDialog
		dialog= JAMDialog(mensaje="¿Abandonas el Juego?", funcion_ok=self.ok, funcion_cancel=self.cancel)
		fuente, tamanio= JAMG.get_Font_fawn()
		dialog.set_font_from_file(fuente, tamanio= 30)
		dialog.boton_aceptar.set_font_from_file(fuente, tamanio= 30)
		dialog.boton_cancelar.set_font_from_file(fuente, tamanio= 30)
		a,b,c= JAMG.get_estilo_papel_quemado()
		dialog.set_colors_dialog(base=c, bordes=c)
		dialog.set_colors_buttons(colorbas=a, colorbor=b, colorcara=c)
		self.estado= "Dialog"
		dialog.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
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

		if self.estado== "Intro":
			dialog.clear(self.ventana, self.fondo)
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()
			return self.run()
		else:
			dialog.clear(self.ventana, self.fondo)
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()
			self.controles.play()

	def ok(self, button):
		#self.estado = "Intro"
		self.salir()
	def cancel(self, button):
		self.estado= "Game"
	# ----------- EVENTOS en JUEGO ---------------

	def salir(self, valor= None):
		self.estado = False
		self.emit("run_grupo", "grupo3", self.puntos)

# -------- SEÑALES ----------
class Seniales(pygame.sprite.OrderedUpdates):
	''' Grupo de Señales. '''
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main= main
		self.imagenes= []
		self.afirmaciones= []
		self.afirmacion_actual= None
		self.load_sprites()
		
	def load_sprites(self):
		for elemento in G.get_imagenes_FGR_T0303():
			button= Sprite_Boton_Imagen(self, elemento)
			self.imagenes.append(button)
			self.add(button)

		afirmaciones= G.get_afirmaciones_FGR_T0303()
		for afirmacion in afirmaciones:
			self.afirmaciones.append(Afirmacion(self, afirmacion))
	
	def next(self):
		indice= self.afirmaciones.index(self.afirmacion_actual)
		if indice < len(self.afirmaciones)-1:
			for sprite in self.afirmacion_actual.sprites():
				self.remove(sprite)
			self.afirmacion_actual= self.afirmaciones[indice+1]
			for imagen in self.imagenes:
				imagen.valor= False
			self.imagenes[self.afirmacion_actual.indice_imagen].valor= True
			self.add(self.afirmacion_actual)
		else:
			return self.main.victory()

	def barajar(self):
		afirmaciones= list(self.afirmaciones)
		self.afirmaciones= []
		random.seed()
		while afirmaciones:
			afirmacion= random.choice(afirmaciones)
			self.afirmaciones.append(afirmacion)
			afirmaciones.remove(afirmacion)

	def init(self):
		if self.afirmacion_actual:
			for sprite in self.afirmacion_actual.sprites():
				self.remove(sprite)
		self.barajar()
		self.afirmacion_actual= self.afirmaciones[0]
		for imagen in self.imagenes:
			imagen.valor= False
		self.imagenes[self.afirmacion_actual.indice_imagen].valor= True
		self.add(self.afirmacion_actual)

class Afirmacion(pygame.sprite.OrderedUpdates):
	def __init__(self, main, afirmacion):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main= main
		self.frase, self.indice_imagen= afirmacion

		self.labels= self.get_sprite_frase()
		self.set_posicion()
		self.add(self.labels)

	def get_sprite_frase(self):
		labels= []
		for frase in self.frase.split("\n"):
			label= JAMLabel(frase)
			label.set_text(color= JAMG.get_blanco())
			label.set_contenedor(colorbas= JAMG.get_negro(), grosor=1, colorbor=JAMG.get_negro())
			label.set_font_from_file(JAMG.get_Font_fawn()[0], tamanio= 50)
			labels.append(label)
		return labels

	def set_posicion(self):
		w,h= (0,0)
		for label in self.labels:
			w1,h1= label.get_tamanio()
			if w < w1: w= w1
			if h < h1: h= h1

		x,y= (15+w/2,100)
		for label in self.labels:
			w2,h2= label.get_tamanio()
			label.set_posicion(punto= (x-w2/2, y))
			y+= h2

class Sprite_Boton_Imagen(pygame.sprite.Sprite):
	def __init__(self, main, imagenpos):
		pygame.sprite.Sprite.__init__(self)
		self.main= main
		self.valor= False

		self.image, pos= imagenpos
		self.rect= self.image.get_rect()
		self.rect.centerx, self.rect.centery= pos

		self.select = False

		self.final_unselect= self.image
		self.final_select= self.get_select()

	def get_select(self):
		img= self.image.copy()
		img= JAMG.get_my_surface_whit_border(img, JAMG.get_amarillo1(), 10)
		return img

	def update(self):
		eventos_republicar= []
		eventos= pygame.event.get(pygame.MOUSEBUTTONDOWN)
		for event in eventos:
			posicion = event.pos
			if self.rect.collidepoint(posicion):
				pygame.event.clear()
				return self.main.main.deja_en(self)
			else:
				if not event in eventos_republicar: eventos_republicar.append(event)

		eventos= pygame.event.get(pygame.MOUSEMOTION)
		for event in eventos:
			posicion = event.pos
			if self.rect.collidepoint(posicion):
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
# -------- SEÑALES ----------

# --------- TEXTOS ----------------
class Textos_Intro(pygame.sprite.OrderedUpdates):
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.base= None
		self.labels= []
		self.gruber= None
		self.base= None

		self.load_textos()
		self.set_posicion_labels()
		self.base= self.get_base()
		self.gruber= self.get_gruber()

		self.add(self.base)
		self.add(self.labels)
		self.add(self.gruber)

	def get_gruber(self):
		gruber= pygame.sprite.Sprite()
		gruber.image= G.get_Imagen_Gruber1()
		gruber.rect= gruber.image.get_rect()
		w,h= G.RESOLUCION
		gruber.rect.x, gruber.rect.y= (w/2-gruber.rect.w/2, self.base.rect.y-gruber.rect.h)
		return gruber

	def get_base(self):
		w,h= self.get_dimensiones()
		w+= 20
		h+= 20
		base= pygame.sprite.Sprite()
		superficie = pygame.Surface( (w,h), flags=SRCALPHA )
		superficie.fill((0,0,0,150))
		base.image= superficie
		base.rect= base.image.get_rect()
		base.rect.x, base.rect.y= (G.RESOLUCION[0]/2-base.rect.w/2, self.labels[0].rect.y-10)
		return base
		
	def load_textos(self):
		textos= G.get_Textos_FGR_T0303()
		for linea in textos:
			label= Sprite_Texto(linea)
			self.labels.append(label)

	def set_posicion_labels(self):
		w,h= G.RESOLUCION
		x, y= (0,h/2-30)
		for label in self.labels:
			x= w/2-label.rect.w/2
			label.rect.x= x
			label.rect.y= y
			y+= label.rect.h

	def get_dimensiones(self):
		w,h= (0,0)
		for label in self.labels:
			if label.rect.w > w: w= label.rect.w
			h+= label.rect.h
		return (w,h)

class Sprite_Texto(pygame.sprite.Sprite):
	def __init__(self, texto):
		pygame.sprite.Sprite.__init__(self)
		string_to_render= ""
		fuente= self.get_Font()
		string_to_render = unicode( texto.decode("utf-8") )
		self.image = fuente.render(string_to_render, 1, JAMG.get_blanco())
		self.rect= self.image.get_rect()

	def get_Font(self):
		fuente, tamanio= JAMG.get_Font_fawn()
		return pygame.font.Font(fuente, tamanio)
# --------- TEXTOS ----------------

# --------- Botones en Menu (Salir y Jugar) ------------------
class ButtonsMenu(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main= main
		imagen= G.get_Flecha()

		salir= JAMButton("",None)
		salir.set_imagen(origen= imagen, tamanio=(100,55))
		salir.set_colores(colorbas=JAMG.get_negro(), colorcara=JAMG.get_negro())
		salir.set_tamanios(tamanio=(0,0), grosorbor=1, detalle=1, espesor=1)
		salir.set_posicion(punto= (10,10))
		#salir.connect (callback= self.main.run_dialog_intro)
		salir.connect (callback = self.main.salir, sonido_select = None)
		self.add(salir)

		jugar= JAMButton("Jugar",None)
		jugar.set_text(color=JAMG.get_blanco())
		fuente, tamanio= JAMG.get_Font_fawn()
		jugar.set_font_from_file(fuente, tamanio= 50)
		jugar.set_colores(colorbas=JAMG.get_negro(), colorcara=JAMG.get_negro())
		jugar.set_tamanios(tamanio=(200,0), grosorbor=1, detalle=1, espesor=1)
		w,h= G.RESOLUCION
		ww,hh= jugar.get_tamanio()
		jugar.set_posicion(punto= (w-ww-10,h-hh-10))
		jugar.connect (callback= self.run_Instruc)
		self.add(jugar)

	def run_Instruc(self, button):
		button.connect (callback= self.switching)
		self.main.estado= "Instruc"
		pygame.event.clear()
		return self.main.run_Instruc()

	def switching(self, button):
		self.main.estado= "Game"
		pygame.event.clear()
		return self.main.run()
# --------- Botones en Menu (Salir y Jugar) ------------------

# --------- Mensaje Final ---------
class Mensaje(pygame.sprite.OrderedUpdates):
	def __init__(self, main, opcion, text1, text2):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main= main
		self.estado= True

		self.base= None
		self.label1= None
		self.label2= None
		self.labels= []
		self.gruber= None

		self.label1= Sprite_Texto(text1)
		self.label2= Sprite_Texto(text2)
		self.labels= [self.label1, self.label2]

		self.x_final_label1= 0
		self.x_final_label2= 0

		self.init()
		self.base= self.get_base()
		if opcion== "Victory":
			self.gruber= self.get_gruber2()
		elif opcion== "End":
			self.gruber= self.get_gruber3()

		self.add(self.base)
		self.add(self.labels)
		self.add(self.gruber)

	def init(self):
		w,h= G.RESOLUCION
		w1,h1= (self.label1.rect.w, self.label1.rect.h)
		w2,h2= (self.label2.rect.w, self.label2.rect.h)

		x= 0-w
		y= h/2-h2/2
		self.label2.rect.x, self.label2.rect.y= (x,y)
		self.x_final_label2= w/2-w2/2

		x= w
		y= self.label2.rect.y - h2
		self.label1.rect.x, self.label1.rect.y= (x,y)
		self.x_final_label1= w/2-w1/2

	def get_base(self):
		w,h= self.get_dimensiones()
		w+= 20
		h+= 20
		base= pygame.sprite.Sprite()
		superficie = pygame.Surface( (w,h), flags=SRCALPHA )
		superficie.fill((0,0,0,150))
		base.image= superficie
		base.rect= base.image.get_rect()
		base.rect.x, base.rect.y= (G.RESOLUCION[0]/2-base.rect.w/2, self.labels[0].rect.y-10)
		return base

	def get_dimensiones(self):
		w,h= (0,0)
		for label in self.labels:
			if label.rect.w > w: w= label.rect.w
			h+= label.rect.h
		return (w,h)

	def get_gruber2(self):
		gruber= pygame.sprite.Sprite()
		gruber.image= G.get_Imagen_Gruber2()
		gruber.rect= gruber.image.get_rect()
		w,h= G.RESOLUCION
		gruber.rect.x, gruber.rect.y= (w/2-gruber.rect.w/2, self.base.rect.y-gruber.rect.h)
		return gruber

	def get_gruber3(self):
		gruber= pygame.sprite.Sprite()
		gruber.image= G.get_Imagen_Gruber3()
		gruber.rect= gruber.image.get_rect()
		w,h= G.RESOLUCION
		gruber.rect.x, gruber.rect.y= (w/2-gruber.rect.w/2, self.base.rect.y-gruber.rect.h)
		return gruber

	def update(self):
		x,y,w,h= self.label2.rect
		final= True
		if x < self.x_final_label2:	
			x+= 60
			self.label2.rect.x, self.label2.rect.y= (x,y)
			final= False
		else:
			self.label2.rect.x= self.x_final_label2

		x,y,w,h= self.label1.rect
		if x > self.x_final_label1:	
			x-= 60
			self.label1.rect.x, self.label1.rect.y= (x,y)
			final= False
		else:
			self.label1.rect.x= self.x_final_label1

		if final== True:
			self.label2.rect.x= self.x_final_label2
			self.label1.rect.x= self.x_final_label1
			self.estado= False

