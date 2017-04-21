#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   FGR_T0102.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame
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
from BiblioJAM.JAMLabel import JAMLabel
import BiblioJAM.JAMGlobals as JAMG

class FGR_T0102(gtk.Widget):
	__gsignals__ = {"run_grupo":(gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING,gobject.TYPE_INT))}
	def __init__(self, usuario):
		gtk.Widget.__init__(self)
		self.usuario = usuario
		self.ventana = None
		self.nombre = "Tipos de señales"
		self.estado = False
		self.fondo = None
		self.reloj = None
		self.puntos = 0
		# Sprites
		self.textos = None
		self.botonesmenu = None
		self.controles = None
		self.seniales = None
		self.carteles = None
		self.senial_select = None
		# sonidos
		self.sonido_error = None
		self.sonido_exito = None
		self.sound_select = None
		# Escalado
		self.ventana_real = None
		self.resolucionreal = None
		self.VA = None
		self.VH = None
		self.estado = "Intro"
		self.load()

	def run(self):
		if self.estado == "Intro":
			self.controles.stop()
			self.fondo = self.fondo1
			return self.run_menu()
		elif self.estado == "Game":
			self.puntos = 0
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
		self.carteles.draw(self.ventana)
		self.seniales.draw(self.ventana)
		self.controles.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		while self.estado == "Game":
			self.reloj.tick(35)
			while gtk.events_pending():
			    	gtk.main_iteration(False)
			G.Traduce_posiciones(self.VA, self.VH)
			self.carteles.clear(self.ventana, self.fondo)
			self.seniales.clear(self.ventana, self.fondo)
			self.controles.clear(self.ventana, self.fondo)
			self.seniales.update()
			self.carteles.update()
			self.controles.update()
			#self.handle_event_Game()
			pygame.event.clear()
			self.carteles.draw(self.ventana)
			self.seniales.draw(self.ventana)
			self.controles.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()

	def reset(self):
		self.puntos= 0
		self.controles.init()
		self.seniales.init()
		self.carteles.init()
	
	def toma(self, senial):
		self.sound_select.play()
		if not self.controles.recuadro_select in self.controles:
			self.controles.add(self.controles.recuadro_select)
		self.senial_select= senial
		self.controles.recuadro_select.rect.center= self.senial_select.rect.center

	def deja_en(self, cartel):
		if self.senial_select:
			if self.senial_select.nombre == cartel.nombre:
				self.sonido_exito.play()
				self.senial_select.ubicada= True
				self.controles.recuadro_select.remove(self.controles)
				random.seed()
				posicion= random.choice(cartel.posiciones)
				cartel.posiciones.remove(posicion)
				self.senial_select.rect.x, self.senial_select.rect.y= posicion
				self.senial_select= None
				self.puntos+= 10
				self.controles.actualiza_puntos()
				fin= True
				for senial in self.seniales:
					if senial.ubicada== False:
						fin= False
						return
				if fin == True:
					return self.victory()
			else:
				self.sonido_error.play()
				self.controles.recuadro_select.remove(self.controles)
				self.senial_select= None
				self.controles.cronometro.cron.segundos_transcurridos+= 5

	def suelta(self):
		if self.senial_select:
			self.controles.recuadro_select.remove(self.controles)
			self.senial_select = None

	def victory(self):
		pygame.mixer.music.unpause()
		self.controles.stop()
		self.puntos+= (10*self.controles.cronometro.get_tiempo_restante())
		self.controles.actualiza_puntos()
		self.ventana.blit(self.fondo, (0,0))
		self.carteles.draw(self.ventana)
		self.seniales.draw(self.ventana)
		self.controles.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
		pygame.display.update()
		pygame.time.wait(1000)
		text1= "Bien, consiguieron su primer sticker!"
		text2= ""
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
		self.carteles.draw(self.ventana)
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
		self.ventana_real = pygame.display.get_surface()
		C = pygame.display.Info().current_w
		D = pygame.display.Info().current_h
		self.resolucionreal= (C,D)
		self.VA = float(C)/float(A)
		self.VH = float(D)/float(B)
		self.fondo1, self.fondo2= G.get_Fondos_FGR_T0102()
		self.textos = Textos_Intro()
		self.botonesmenu = ButtonsMenu(self)
		self.controles = Controles(self)
		self.seniales = Seniales(self)
		self.carteles = Carteles(self)
		self.sonido_error, self.sonido_exito= G.get_Sonidos()
		self.sound_select = JAMG.get_sound_select()
		self.reloj = pygame.time.Clock()

	# ----------- EVENTOS en MENU ---------------
	def handle_event_Intro(self):
		for event in pygame.event.get(pygame.KEYDOWN):
			letra= pygame.key.nombre(event.key)
			if letra== "escape":
				pygame.event.clear()
				#return self.run_dialog_intro(None)
				return self.salir()

	def run_Instruc(self):
		self.fondo= G.get_instruc("102")
		self.ventana.blit(self.fondo, (0,0))
		self.botonesmenu.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
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
			letra= pygame.key.nombre(event.key)
			if letra== "escape":
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
		self.emit("run_grupo", "grupo1", self.puntos)

# -------- CONTROLES ----------
class Controles(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main= main
		self.flecha= None
		self.titulo= None
		self.puntaje= None
		self.cronometro= None
		self.recuadro_select= None
		self.reloj= None
		self.progress_reloj= None
		self.sonidos_reloj= None
		self.user = None
		self.load_sprites()
	
	def get_recuadro_select(self, tamanio):
		''' Un Sprite para seleccionar las señales.'''
		sup= JAMG.get_Rectangulo_Transparente( tamanio )
		sup= JAMG.get_my_surface_whit_border(sup, JAMG.get_amarillo1(), 10)
		self.recuadro_select= pygame.sprite.Sprite()
		self.recuadro_select.image= sup
		self.recuadro_select.rect= self.recuadro_select.image.get_rect()

	def get_labels_carteles(self,texto, centro):
		''' Etiquetas sobre los carteles. '''
		label= JAMLabel(texto)
		label.set_text(color=JAMG.get_blanco())
		fuente, tamanio= JAMG.get_Font_fawn()
		label.set_font_from_file(fuente, tamanio= tamanio)
		x,y= centro
		w,h= label.get_tamanio()
		label.set_posicion(punto=(x-w/2,y-h/2))
		self.add(label)

	def load_sprites(self):
		imagen = self.main.usuario['personaje']
		self.user = JAMButton(self.main.usuario['nombre'],None)
		self.user.set_imagen(origen = imagen, tamanio = (60,60))
		self.user.set_colores(colorbas = (0,153,255,255),
			colorbor = (0,153,255,255), colorcara = (0,153,255,255))
		self.user.set_tamanios(tamanio = (80,80), grosorbor = 1, detalle = 1, espesor = 1)
		ww, hh = self.user.get_tamanio()
		w,h = G.RESOLUCION
		self.user.set_posicion(punto = (w - ww - 10, 25))
		self.user.connect(callback = None, sonido_select = None)
		self.add(self.user)

		imagen= G.get_Flecha()
		self.flecha= JAMButton("",None)
		self.flecha.set_imagen(origen= imagen, tamanio=(100,55))
		self.flecha.set_colores(colorbas=JAMG.get_negro(), colorcara=JAMG.get_negro())
		self.flecha.set_tamanios(tamanio=(0,0), grosorbor=1, detalle=1, espesor=1)
		self.flecha.set_posicion(punto= (10,10))
		self.flecha.connect (callback= self.main.run_dialog_game)
		self.add(self.flecha)

		x,y= self.flecha.posicion
		w,h= self.flecha.get_tamanio()
		x+= w
		ancho= G.RESOLUCION[0]/2 - x
		cartel_titulo= pygame.sprite.Sprite()
		cartel_titulo.image= G.get_Imagen_Cartel1()
		cartel_titulo.image= pygame.transform.scale(cartel_titulo.image.copy(), (ancho,cartel_titulo.image.get_size()[1]))
		cartel_titulo.rect= cartel_titulo.image.get_rect()
		cartel_titulo.rect.x= x
		cartel_titulo.rect.y= -60
		self.add(cartel_titulo)

		self.titulo= JAMLabel(self.main.nombre)
		self.titulo.set_text(color=JAMG.get_blanco())
		fuente, tamanio= JAMG.get_Font_fawn()
		self.titulo.set_font_from_file(fuente, tamanio= 40)
		w,h= G.RESOLUCION
		x,y= (cartel_titulo.rect.x + 50, 10)
		self.titulo.set_posicion(punto= (x,y))
		self.add(self.titulo)

		self.puntaje= JAMLabel("%s" %(self.main.puntos))
		self.puntaje.set_text(color=JAMG.get_blanco())
		fuente, tamanio= JAMG.get_Font_fawn()
		self.puntaje.set_font_from_file(fuente, tamanio= 40)
		w,h= G.RESOLUCION
		self.add(self.puntaje)

		self.sonidos_reloj= G.get_sound_clock()

		from BiblioJAM.JAMCron import JAMCron
		self.cronometro= JAMCron()
		x,y= (0-self.cronometro.cron.rect.w-1, 0-self.cronometro.cron.rect.h-1)
		self.cronometro.cron.set_posicion(punto= (x,y))
		self.cronometro.set_callback(self.main.game_over)
		self.cronometro.set_alarma(tiempo= (1,30), duracion= 1)
		self.add(self.cronometro)
		
		self.progress_reloj= ProgressBar(self.main)
		self.add(self.progress_reloj)

	def actualiza_puntos(self):
		puntos = "%s" %(self.main.puntos)
		self.puntaje.set_text(texto= puntos)
		x,y = self.user.get_posicion()
		w,h = self.puntaje.get_tamanio()
		x -= w+10
		self.puntaje.set_posicion(punto= (x,y))

	def switching_game(self, button):
		self.main.estado= "Intro"
		return self.main.run()

	def init(self):
		sound= self.sonidos_reloj[0]
		self.cronometro.set_sound(sound)
		self.cronometro.reset()
		self.actualiza_puntos()
		self.cronometro.play()
	def stop(self):
		self.cronometro.pause()
	def play(self):
		self.cronometro.play()

class ProgressBar(pygame.sprite.Sprite):
	def __init__(self, main):
		pygame.sprite.Sprite.__init__(self)
		self.main= main
		self.acumula= 0
		
		w,h= G.RESOLUCION
		self.tamanio= (w/2-10,10)
		self.posicion= (w/2,10)

		rect1= JAMG.get_Rectangulo( JAMG.get_verde1(), self.tamanio)
		w,y= rect1.get_size()
		a= w/6*3
		rect2= JAMG.get_Rectangulo( JAMG.get_amarillo1(), (a,self.tamanio[1]))
		imagen= JAMG.pegar_imagenes_alineado_derecha(rect2, rect1)
		a= w/6
		rect3= JAMG.get_Rectangulo( JAMG.get_rojo1(), (a,self.tamanio[1]))
		self.imagen_original= JAMG.pegar_imagenes_alineado_derecha(rect3, imagen)

		self.image= self.imagen_original.copy()
		self.rect= self.image.get_rect()
		self.rect.x, self.rect.y= self.posicion

	def update(self):
		tiempo= self.main.controles.cronometro.cron.segundos_final
		transcurridos= self.main.controles.cronometro.get_tiempo_transcurrido()
		faltan= self.main.controles.cronometro.cron.segundos_faltan
		mitad= tiempo/2
		cuarto= tiempo/4
		if faltan <= mitad:
			if faltan > cuarto:
				if not self.main.controles.cronometro.sonido == self.main.controles.sonidos_reloj[1]:
					self.main.controles.stop()
					self.main.controles.cronometro.set_sound(self.main.controles.sonidos_reloj[1])
					self.main.controles.play()
			elif faltan <= cuarto:
				if not self.main.controles.cronometro.sonido == self.main.controles.sonidos_reloj[2]:
					self.main.controles.stop()
					self.main.controles.cronometro.set_sound(self.main.controles.sonidos_reloj[2])
					self.main.controles.play()

		ancho, alto= self.tamanio
		ind= float(float(ancho)/float(self.main.controles.cronometro.cron.segundos_final))
		ancho= float(float(ancho)- float(self.main.controles.cronometro.get_tiempo_transcurrido())*ind)
		dif= float(float(self.tamanio[0]) - float(ancho))
		try:
			self.image= self.imagen_original.copy().subsurface((dif,0,int(ancho), int(alto)))
		except:
			self.image= self.imagen_original.copy().subsurface((dif,0,0,0))

		self.rect= self.image.get_rect()
		x,y= self.posicion
		x+= dif
		self.rect.x, self.rect.y= (x,y)
# -------- CONTROLES ----------

# -------- SEÑALES ----------
class Seniales(pygame.sprite.OrderedUpdates):
	''' Grupo de Señales.'''
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main= main
		self.load_sprites()

	def load_sprites(self):
		''' Carga las señales. '''
		seniales= G.get_Seniales_FGR_T0102()
		posiciones= G.get_Posicion_Seniales_FGR_T0102()
		w,h= (0,0)
		for senial in seniales.keys():
			imagen= seniales[senial][0]
			ancho, alto= imagen.get_size()
			if ancho > w: w= ancho
			if alto > h: h= alto

			random.seed()
			posicion= random.choice(posiciones)
			posiciones.remove(posicion)
			sprite= Sprite_Seniales(imagen, self.main, posicion)
			sprite.nombre= seniales[senial][1]
			self.add(sprite)
		# el sprite para seleccionar las señales
		self.main.controles.get_recuadro_select((w,h))
		
	def init(self):
		posiciones= G.get_Posicion_Seniales_FGR_T0102()
		for senial in self.sprites():
			random.seed()
			posicion= random.choice(posiciones)
			senial.posicion_inicial= posicion
			posiciones.remove(posicion)
			senial.init()
			senial.ubicada= False

class Sprite_Seniales(pygame.sprite.Sprite):
	''' La Señal. '''
	def __init__(self, imagen, main, posicion_inicial):
		pygame.sprite.Sprite.__init__(self)
		self.main= main
		self.posicion_inicial= posicion_inicial

		self.image= imagen
		self.rect= self.image.get_rect()
		self.ubicada= False
		self.nombre= None
		self.init()
	
	def init(self):
		''' Setea la posición inicial. '''
		self.rect.center= self.posicion_inicial

	def update(self):
		if self == self.main.senial_select or self.ubicada: return
		eventos_republicar= []
		eventos= pygame.event.get(pygame.MOUSEBUTTONDOWN)
		for event in eventos:
			posicion = event.pos
			if self.rect.collidepoint(posicion):
				punto= (int(posicion[0]-self.rect.x), int(posicion[1]-self.rect.y))
				color= self.image.get_at( punto )
				if color[3] != 0:
					pygame.event.clear()
					return self.main.toma(self)
				#else:
				#	eventos_republicar.append(event)
			else:
				if not event in eventos_republicar: eventos_republicar.append(event)
		
		for event in eventos_republicar:
			pygame.event.post(event)
# -------- SEÑALES ----------

# -------- CARTELES ----------
class Carteles(pygame.sprite.OrderedUpdates):
	'''Grupo de Carteles. '''
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main= main
		self.load_sprites()
	
	def load_sprites(self):
		''' Carga los Carteles. '''
		carteles= G.get_Carteles_FGR_T0102()
		posiciones= G.get_Posicion_Carteles_FGR_T0102()
		for cartel in carteles.keys():
			sprite= Sprite_Carteles(carteles[cartel], self.main)
			random.seed()
			posicion= random.choice(posiciones)
			sprite.rect.center= posicion
			posiciones.remove(posicion)
			sprite.nombre= cartel
			x,y,w,h= sprite.rect
			posicion= (x+w/2, y+h+20)
			self.main.controles.get_labels_carteles(cartel, posicion)
			self.add(sprite)

	def init(self):
		''' Vuelve a generar las posiciones para las señales. '''
		for sprite in self.sprites():
			sprite.get_posiciones()

class Sprite_Carteles(pygame.sprite.Sprite):
	''' El cartel. '''
	def __init__(self, imagen, main):
		pygame.sprite.Sprite.__init__(self)
		self.main= main
		self.image= imagen
		self.rect= self.image.get_rect()
		self.nombre= None
		self.posiciones= None

	def get_posiciones(self):
		''' Lista de posiciones para las señales ubicadas. '''
		posiciones= []
		x,y,w,h= self.rect
		posiciones.append((x-100,y))
		posiciones.append((x-100,y+100))
		posiciones.append((x,y+210))
		posiciones.append((x+100,y+210))
		posiciones.append((x+w,y))
		posiciones.append((x+w,y+100))
		self.posiciones= posiciones

	def update(self):
		eventos= pygame.event.get(pygame.MOUSEBUTTONDOWN)
		eventos_republicar= []
		for event in eventos:
			posicion = event.pos
			if self.rect.collidepoint(posicion):
				punto= (int(posicion[0]-self.rect.x), int(posicion[1]-self.rect.y))
				color= self.image.get_at( punto )
				if color[3] != 0:
					pygame.event.clear()
					return self.main.deja_en(self)
				else:
					#eventos_republicar.append(event)
					pass
			else:
				if not event in eventos_republicar: eventos_republicar.append(event)

		for event in eventos_republicar:
			pygame.event.post(event)
# -------- CARTELES ----------

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
		textos= G.get_Textos_FGR_T0102()
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

