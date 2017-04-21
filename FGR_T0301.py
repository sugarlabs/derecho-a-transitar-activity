#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   FGR_T0301.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys, random, gtk, pygtk
from pygame.locals import *

import Globals as G
gc.enable()

import BiblioJAM
from BiblioJAM.JAMButton import JAMButton
from BiblioJAM.JAMLabel import JAMLabel
import BiblioJAM.JAMGlobals as JAMG

class FGR_T0301():
	def __init__(self, main):
		# Variables para JAMatrix
		self.ventana= None
		self.name= "Seré Conductor"
		self.estado= False

		self.main= main
		self.ventana= self.main.ventana

		# Variables del Juego
		self.fondo= None
		self.reloj= None
		self.puntos= 0

		# Sprites
		self.textos= None
		self.botonesmenu= None
		self.controles= None
		self.seniales= None
		self.carteles= None
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

	def run(self):
		self.preset()

		from BiblioJAM.JAMatrix import JAMatrix
		matrix= JAMatrix(self, self.ventana_real, self.resolucionreal)
		matrix.set_imagen_matrix(None)
		matrix.carga_game()

		self.estado= "Intro"
		self.switch()

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
			self.controles.update()
			self.handle_event_Game()
			pygame.event.clear()
			self.carteles.draw(self.ventana)
			self.seniales.draw(self.ventana)
			self.controles.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()
			#self.victory()
			#self.game_over(None)

	def switch(self):
		if self.estado== "Intro":
			self.controles.stop()
			self.fondo = self.fondo1
			self.set_event_intro()
			return self.run_menu()
		elif self.estado== "Game":
			self.puntos= 0
			self.fondo = self.fondo2
			self.reset()
			return self.run_juego()

	def reset(self):
		self.puntos= 0
		self.carteles.init()
		self.controles.init()
		self.seniales.init()

	def correct(self):
		self.sonido_exito.play()
		self.puntos+= 10
		self.controles.actualiza_puntos()

	def error(self):
		self.sonido_error.play()
		self.controles.cronometro.cron.segundos_transcurridos+= 5

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

		text1= "Muy bien, ahora saben cuáles son las partes más importantes de una bici y "
		text2= "gracias a eso consiguieron 1 sticker más. Sigan adelante!"

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
		self.fondo1, self.fondo2= G.get_Fondos_FGR_T0301()
		self.textos= Textos_Intro()
		self.botonesmenu= ButtonsMenu(self)
		self.controles= Controles(self)
		self.seniales= SopadeLetras(self)
		self.carteles= Carteles(self)
		self.sonido_error, self.sonido_exito= G.get_Sonidos()
		self.sound_select= JAMG.get_sound_select()
		self.reloj = pygame.time.Clock()
		self.estado= True

	def set_event_intro(self):
		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN, KEYUP, USEREVENT])
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN, VIDEORESIZE, VIDEOEXPOSE, QUIT, ACTIVEEVENT])
		pygame.mouse.set_visible(True)

	# ----------- EVENTOS en MENU ---------------
	def handle_event_Intro(self):
		for event in pygame.event.get(pygame.KEYDOWN):
			tecla= event.key
			if tecla== pygame.K_ESCAPE:
				pygame.event.clear()
				return self.run_dialog_intro(None)

	def run_Instruc(self):
		self.fondo= G.get_instruc("301")
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
		self.estado= "Intro"
	# ----------- EVENTOS en MENU ---------------

	# ----------- EVENTOS en JUEGO ---------------
	def handle_event_Game(self):
		for event in pygame.event.get(pygame.KEYDOWN):
			tecla= event.key
			if tecla== pygame.K_ESCAPE:
				pygame.event.clear()
				return self.run_dialog_game(None)
					
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
			return self.switch()
		else:
			dialog.clear(self.ventana, self.fondo)
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()
			self.controles.play()

	def ok(self, button):
		self.estado= "Intro"
	def cancel(self, button):
		self.estado= "Game"
	# ----------- EVENTOS en JUEGO ---------------

	def salir(self, valor= None):
		if valor: self.estado= True
		if not valor: self.estado= False
		pygame.mixer.music.unpause()
		self.seniales.empty()
		self.carteles.empty()
		self.controles.empty()

# -------- CONTROLES ----------
class Controles(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main= main
		self.flecha= None
		self.titulo= None
		self.puntaje= None
		self.cronometro= None
		self.progress_reloj= None
		self.sonidos_reloj= None

		self.load_sprites()

	def load_sprites(self):
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

		self.titulo= JAMLabel(self.main.name)
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
		self.cronometro.set_alarma(tiempo= (1,40), duracion= 3)
		self.add(self.cronometro)

		self.progress_reloj= ProgressBar(self.main)
		self.add(self.progress_reloj)

	def actualiza_puntos(self):
		puntos= "%s" %(self.main.puntos)
		self.puntaje.set_text(texto= puntos)
		w,h= G.RESOLUCION
		x,y= (w-self.puntaje.rect.w-20, 25)
		self.puntaje.set_posicion(punto= (x,y))

	def switching_game(self, button):
		self.main.estado= "Intro"
		return self.main.switch()

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

# -------- SOPADELETRAS ----------
class SopadeLetras(pygame.sprite.OrderedUpdates):
	''' Grupo de Señales. '''
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main= main
		self.filadebotones= []
		self.palabras= None
		self.posicion= (150,330)
		self.palabra_select= None
		self.imagen= None
		self.imagen_palabra_select= None
		self.Construye()
		
	def Construye(self):
		self.imagen= pygame.sprite.Sprite()
		self.imagen.image= G.get_personajes_FGR_T0301()
		self.imagen.rect= self.imagen.image.get_rect()
		self.add(self.imagen)

		filas= ["ZOMSALEMDA","ELAPEDALES","INFLADORSO", "AECUADROFZ", "BOACECDARV", "POSEDENIEA", "ALISODTANA", "RIASIENTOF", "OCETANOASD", "MAGYOATSGH"]

		self.filadebotones= []
		for fila in filas:
			newfila= []
			for letra in fila:
				boton= Sprite_Button(self, letra)
				newfila.append(boton)
				self.add(boton)
			self.filadebotones.append(newfila)

		w,h = (0,0)
		lado= 0
		for fila in self.filadebotones:
			for boton in fila:
				w1,h1= boton.get_tamanio()
				if w1> w: w= w1
				if h1> h: h= h1
				if lado < w: lado= w	
				if lado < h: lado= h

		for fila in self.filadebotones:
			for boton in fila:
				boton.set_tamanios(tamanio=(lado,lado), grosorbor= 1, detalle= 1, espesor= 1)
				
		self.set_posiciones(punto= self.posicion)

		self.palabras={
			"PEDALES":self.filadebotones[1][3:], 
			"INFLADOR":self.filadebotones[2][0:8],
			"CUADRO":self.filadebotones[3][2:8],
			"LUCES":[self.filadebotones[2][3], self.filadebotones[3][3],self.filadebotones[4][3], self.filadebotones[5][3], self.filadebotones[6][3]],
			"FRENOS":[self.filadebotones[3][8],self.filadebotones[4][8], self.filadebotones[5][8], self.filadebotones[6][8], self.filadebotones[7][8], 				self.filadebotones[8][8]],
			"ASIENTO":self.filadebotones[7][2:9],
			"PLATO":[self.filadebotones[5][0], self.filadebotones[6][1], self.filadebotones[7][2], self.filadebotones[8][3], self.filadebotones[9][4]]}

		for palabra in self.palabras:
		# reconvierte el diccionario a grupos de sprites
			grupopalabra= Palabra(self.main, palabra)
			grupopalabra.add(self.palabras[palabra])
			self.palabras[palabra]= grupopalabra

	def get_posicion(self):
		return self.posicion

	def get_tamanio(self):
		''' Devuelve el tamaño total de la sopa de letras. '''
		w,h= self.filadebotones[0][0].get_tamanio()
		w= w*len(self.filadebotones[0])
		h= h*len(self.filadebotones)
		return w,h

	def set_posiciones(self, punto= (0,0)):
		self.posicion= punto
		x,y= self.posicion
		a,b,c,d= self.imagen.rect
		self.imagen.rect.x= x-50
		self.imagen.rect.y= y-d		
		for fila in self.filadebotones:
			x= self.posicion[0]
			w,h= (0,0)
			for boton in fila:
				boton.set_posicion(punto= (x,y))
				w,h= boton.get_tamanio()
				x+= w
			y+= h

	def verifica(self, boton):
		if boton.ubicada: return
		if self.palabra_select:
		# Si hay una palabra seleccionada
			if boton in self.palabra_select:
			# Si este botón está en la palabra seleccionada
				boton.paint_select()
				return self.verifica_palabra()
			else:
			# Si este botón no está en la palabra seleccionada
				self.deselect_palabras_botones()
				return self.verifica(boton)
		else:
		# Si no hay una palabra seleccionada
			for palabra in self.palabras:
				pal= self.palabras[palabra]
				if not pal.ubicada:
					if boton in pal:
					# seleccionamos la palabra
						self.palabra_select= pal
						return self.verifica(boton) # recursividad
		return self.main.error()
	
	def verifica_palabra(self):
		for letra in self.palabra_select:
			if not letra.ubicada: return
		# Si todos se han ubicado
		self.palabra_select.ubicada= True
		palabra= ""
		for pal in self.palabra_select.sprites():
			palabra+= pal.get_text()

		for plbra in self.main.carteles.sprites():
		# tacha la palabra encontrada
			if palabra== plbra.get_text():
				plbra.set_text(color= JAMG.get_verde1())
				#plbra.tacha()

		if self.imagen_palabra_select: self.imagen_palabra_select.kill()
		self.imagen_palabra_select= Sprite_Imagen_Palabra(self, palabra)
		self.add(self.imagen_palabra_select)
		self.palabra_select= None
		self.main.correct()

		fin= True
		for palabra in self.palabras:
			pal= self.palabras[palabra]
			if not pal.ubicada: return
		if fin == True:
			return self.main.victory()

	def deselect_palabras_botones(self):
		for letra in self.palabra_select:
			letra.init()
			letra.ubicada= False
			self.palabra_select= None

	def init(self):
		for palabra in self.palabras:
			self.palabra_select= None
			if self.imagen_palabra_select: self.imagen_palabra_select.kill()
			self.palabras[palabra].init()

class Sprite_Imagen_Palabra(pygame.sprite.Sprite):
	def __init__(self, main, palabra):
		pygame.sprite.Sprite.__init__(self)
		self.main= main
		self.image= G.get_imagen_FGR_T0301(palabra)
		self.rect= self.image.get_rect()
		self.rect.x= 860
		self.rect.y= 400
		from BiblioJAM.JAMCron import JAMCron
		self.cronometro= JAMCron()
		self.cronometro.set_sound(None)
		self.cronometro.set_alarma(tiempo= (0,6), sound= None, duracion= 1)
		self.cronometro.set_callback(self.killer)
		self.cronometro.play()

	def update(self):
		self.cronometro.update()
	def killer(self, cron):
		cron.pause()
		for sprite in cron.sprites():
			sprite.kill()
		self.kill()

class Palabra(pygame.sprite.OrderedUpdates):
	def __init__(self, main, name):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.ubicada= False

	def init(self):
		self.ubicada= False
		for boton in self.sprites():
			boton.init()

class Sprite_Button(JAMButton):
	def __init__(self, main, texto):
		JAMButton.__init__(self, texto, None)
		self.main= main
		self.ubicada= False

		self.set_font_from_file(JAMG.get_Font_fawn()[0], tamanio= 30)
		self.set_tamanios(tamanio=(0,0), grosorbor= 1, detalle= 1, espesor= 1)
		self.connect(callback= self.main.verifica, sonido_select= None)

	def paint_select(self):
		self.ubicada= True
		a,b,c= JAMG.get_estilo_naranja()
		self.set_colores(colorbas= a, colorbor= b, colorcara= c)

	def init(self):
		self.ubicada= False
		a,b,c,d,e,f= JAMG.get_default_jambutton_values()
		self.set_colores(colorbas= b, colorbor= c, colorcara= a)
# -------- SOPADELETRAS ----------

# --------- PALABRAS A BUSCAR ----------------------------
class Carteles(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main= main
		self.load_sprites()

	def load_sprites(self):
		palabras= ["PEDALES", "INFLADOR", "CUADRO", "LUCES", "FRENOS", "ASIENTO", "PLATO"]
		x,y= self.main.seniales.get_posicion()
		w,h= self.main.seniales.get_tamanio()
		x+= w+5
		for pal in palabras:
			label= JAMLabel(pal)
			label.set_font_from_file(JAMG.get_Font_fawn()[0], tamanio= 50)
			label.set_text(color= JAMG.get_blanco())
			label.set_posicion(punto= (x,y))
			y+= label.get_tamanio()[1]+5		
			self.add(label)

	def init(self):
		for sprite in self.sprites():
			sprite.kill()
			self.empty()
			self.load_sprites()
# --------- PALABRAS A BUSCAR ----------------------------

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
		textos= G.get_Textos_FGR_T0301()
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
		salir.connect (callback= self.main.run_dialog_intro)
		self.add(salir)

		jugar= JAMButton("Jugar",None)
		jugar.set_text(color=JAMG.get_blanco())
		fuente, tamanio= JAMG.get_Font_fawn()
		jugar.set_font_from_file(fuente, tamanio= 50)
		jugar.set_colores(colorbas=JAMG.get_negro(), colorcara=JAMG.get_negro())
		jugar.set_tamanios(tamanio=(200,0), grosorbor=1, detalle=1, espesor=1)
		w,h= G.RESOLUCION
		ww,hh= jugar.get_tamanio()
		jugar.set_posicion(punto= (w-ww-50,h-hh-50))
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
		return self.main.switch()
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
# --------- Mensaje Final ---------

class Main():
	def __init__(self):
		pygame.init()
		pygame.display.set_mode(G.RESOLUCION , 0, 0)
		self.ventana= pygame.display.get_surface()
		FGR_T0301(self)

if __name__ == "__main__":
	Main()

