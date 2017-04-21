#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   FGR_T0204.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame
import os
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

class FGR_T0204(gtk.Widget):
	__gsignals__ = {"run_grupo":(gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING,gobject.TYPE_INT))}
	def __init__(self, usuario):
		gtk.Widget.__init__(self)
		self.usuario = usuario
		self.ventana = None
		self.nombre = "Crucigrama."
		self.estado = False
		self.fondo = None
		self.reloj = None
		self.puntos = 0
		# Sprites
		self.textos = None
		self.botonesmenu = None
		self.controles = None
		self.seniales = None
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
		self.load()
		self.estado = "Intro"

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
		self.ventana_real.blit(pygame.transform.scale(self.ventana,
			self.resolucionreal), (0,0))
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
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
			pygame.display.update()

	def run_juego(self):
		pygame.mixer.music.pause()
		self.ventana.blit(self.fondo, (0,0))
		self.seniales.draw(self.ventana)
		self.controles.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana,
			self.resolucionreal), (0,0))
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
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
			pygame.display.update()

	def reset(self):
		self.puntos= 0
		self.controles.init()
		#self.seniales.init()

	def toma(self, boton):
		if boton.ubicado: return
		self.sound_select.play()
		self.senial_select = boton
		self.seniales.seleccionar(self.senial_select)

	def deja(self, flecha):
		if not self.senial_select: return
		if self.senial_select.get_text() == flecha.nombre:
			self.sonido_exito.play()
			self.puntos += 10
			self.controles.actualiza_puntos()
			self.senial_select.marcar()
			self.senial_select = None
			self.seniales.marcar(flecha)
			self.verificar()
		else:
			self.sonido_error.play()
			self.controles.cronometro.cron.segundos_transcurridos += 5

	def verificar(self):
		faltan = False
		for boton in self.seniales.botones:
			if not boton.ubicado:
				faltan = True
				break
		if not faltan:
			self.ventana.blit(self.fondo, (0,0))
			self.seniales.draw(self.ventana)
			self.controles.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
			pygame.display.update()
			pygame.time.wait(1000)
			self.ventana.blit(self.fondo, (0,0))
			return self.victory()

	def victory(self):
		pygame.mixer.music.unpause()
		self.controles.stop()
		self.puntos+= (10*self.controles.cronometro.get_tiempo_restante())
		self.controles.actualiza_puntos()
		self.ventana.blit(self.fondo, (0,0))
		self.seniales.draw(self.ventana)
		self.controles.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana,
			self.resolucionreal), (0,0))
		pygame.display.update()
		pygame.time.wait(1000)
		text1= "Muy bien, ahora saben cuáles son las partes más importantes de una bici y "
		text2= "gracias a eso consiguieron 1 sticker más. Sigan adelante!"
		mensaje= Mensaje(self, "Victory", text1, text2)
		self.fondo= self.fondo1
		self.ventana.blit(self.fondo, (0,0))
		mensaje.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana,
			self.resolucionreal), (0,0))
		pygame.display.update()
		while mensaje.estado == True:
			self.reloj.tick(35)
			mensaje.clear(self.ventana, self.fondo)
			mensaje.update()
			mensaje.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
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
		self.ventana_real.blit(pygame.transform.scale(self.ventana,
			self.resolucionreal), (0,0))
		pygame.display.update()
		pygame.time.wait(1000)
		text1= "Te han Faltado Unos Segundos Para Completar la Actividad."
		text2= "Prueba Nuevamente."
		mensaje= Mensaje(self, "End", text1, text2)
		self.fondo= self.fondo1
		self.ventana.blit(self.fondo, (0,0))
		mensaje.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana,
			self.resolucionreal), (0,0))
		pygame.display.update()
		while mensaje.estado == True:
			self.reloj.tick(35)
			mensaje.clear(self.ventana, self.fondo)
			mensaje.update()
			mensaje.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
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
		self.fondo1, self.fondo2= G.get_Fondos_FGR_T0204()
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
		self.fondo= G.get_instruc("204")
		self.ventana.blit(self.fondo, (0,0))
		self.botonesmenu.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana,
			self.resolucionreal), (0,0))
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
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
			pygame.display.update()

	'''
	def run_dialog_intro(self, button):
		from BiblioJAM.JAMDialog import JAMDialog
		dialog= JAMDialog(mensaje="¿Abandonas el Juego?",
			funcion_ok=self.ok_intro, funcion_cancel=self.cancel_intro)
		fuente, tamanio= JAMG.get_Font_fawn()
		dialog.set_font_from_file(fuente, tamanio= 40)
		dialog.boton_aceptar.set_font_from_file(fuente, tamanio= 25)
		dialog.boton_cancelar.set_font_from_file(fuente, tamanio= 25)
		a,b,c= JAMG.get_estilo_papel_quemado()
		dialog.set_colors_dialog(base=c, bordes=c)
		dialog.set_colors_buttons(colorbas=a, colorbor=b, colorcara=c) 
		self.estado= "Dialog"
		dialog.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana,
			self.resolucionreal), (0,0))
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
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
			pygame.display.update()
		dialog.clear(self.ventana, self.fondo)
		self.ventana_real.blit(pygame.transform.scale(self.ventana,
			self.resolucionreal), (0,0))
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
		dialog= JAMDialog(mensaje="¿Abandonas el Juego?",
			funcion_ok=self.ok, funcion_cancel=self.cancel)
		fuente, tamanio= JAMG.get_Font_fawn()
		dialog.set_font_from_file(fuente, tamanio= 30)
		dialog.boton_aceptar.set_font_from_file(fuente, tamanio= 30)
		dialog.boton_cancelar.set_font_from_file(fuente, tamanio= 30)
		a,b,c= JAMG.get_estilo_papel_quemado()
		dialog.set_colors_dialog(base=c, bordes=c)
		dialog.set_colors_buttons(colorbas=a, colorbor=b, colorcara=c)
		self.estado= "Dialog"
		dialog.draw(self.ventana)
		self.ventana_real.blit(pygame.transform.scale(self.ventana,
			self.resolucionreal), (0,0))
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
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
			pygame.display.update()
		if self.estado== "Intro":
			dialog.clear(self.ventana, self.fondo)
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
			pygame.display.update()
			return self.run()
		else:
			dialog.clear(self.ventana, self.fondo)
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
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
		self.emit("run_grupo", "grupo2", self.puntos)

class Seniales(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main = main
		self.palabras = {}
		self.botones = []
		self.flechas = {}
		self.matriz_letras = []
		self.textos = []
		self.load_sprites()
		self.set_posicion((75, 180))
		
	def load_sprites(self):
		self.empty()
		self.botones = []
		self.palabras = {}
		self.flechas = {}
		self.matriz_letras = []
		self.textos = []
		matriz = G.get_letras_FGR_T0204()
		for linea in matriz:
			fila = []
			for letra in linea:
				l = Letra(letra)
				fila.append(l)
				if bool(letra): self.add(l)
			self.matriz_letras.append(fila)

		# Verticales
		acera = []
		for linea in self.matriz_letras[0:5]:
			acera.append(linea[-1])
		self.palabras['ACERA'] = acera
		banquina = []
		for linea in self.matriz_letras[2:]:
			banquina.append(linea[8])
		self.palabras['BANQUINA'] = banquina
		cruzar = []
		for linea in self.matriz_letras[2:8]:
			cruzar.append(linea[6])
		self.palabras['CRUZAR'] = cruzar
		# Horizontales
		self.palabras['FILA'] = self.matriz_letras[0][9:]
		self.palabras['BORDE'] = self.matriz_letras[2][8:]
		self.palabras['ESQUINA'] = self.matriz_letras[4][3:10]
		self.palabras['OPUESTA'] = self.matriz_letras[6][:7]
		self.palabras['PEATON'] = self.matriz_letras[-1][6:]

		for key in self.palabras.keys():
			boton = Boton(key)
			boton.connect(callback = self.main.toma, sonido_select = None)
			self.botones.append(boton)
			self.add(boton)

		directorio = os.path.join(G.IMAGENES, 'flechas')
		self.flechas['ACERA'] = Flecha('ACERA', os.path.join(directorio, 'v_flecha6.png'))
		self.flechas['BANQUINA'] = Flecha('BANQUINA', os.path.join(directorio, 'v_flecha2.png'))
		self.flechas['CRUZAR'] = Flecha('CRUZAR', os.path.join(directorio, 'v_flecha3.png'))
		self.flechas['FILA'] = Flecha('FILA', os.path.join(directorio, 'flecha7.png'))
		self.flechas['BORDE'] = Flecha('BORDE', os.path.join(directorio, 'flecha5.png'))
		self.flechas['ESQUINA'] = Flecha('ESQUINA', os.path.join(directorio, 'flecha1.png'))
		self.flechas['OPUESTA'] = Flecha('OPUESTA', os.path.join(directorio, 'flecha4.png'))
		self.flechas['PEATON'] = Flecha('PEATON', os.path.join(directorio, 'flecha8.png'))
		for key in self.flechas.keys():
			flecha = self.flechas[key]
			flecha.connect(callback = self.main.deja, sonido_select = None)
			self.add(flecha)

		fuente, tamanio = JAMG.get_Font_fawn()
		for linea in G.get_Texto_FGR_T0204():
			label = JAMLabel(linea)
			label.set_font_from_file(fuente, tamanio = 28)
			label.set_text(color = (255,255,255,255))
			self.textos.append(label)

	def set_posicion(self, punto = (0,0)):
		pos = punto
		x, y = pos
		w, h = (0,0)
		for fila in self.matriz_letras:
			for letra in fila:
				letra.set_posicion( (x,y) )
				w,h = letra.get_tamanio()
				x += w
			y += h
			x = pos[0]

		# Verticales
		flecha = self.flechas['ACERA']
		elemento = self.matriz_letras[0][-1]
		((a,b), (c,d)) = (elemento.get_posicion(), flecha.get_tamanio())
		flecha.set_posicion( (a,b-d) )
		flecha = self.flechas['BANQUINA']
		elemento = self.matriz_letras[2][8]
		((a,b), (c,d)) = (elemento.get_posicion(), flecha.get_tamanio())
		flecha.set_posicion( (a,b-d) )
		flecha = self.flechas['CRUZAR']
		elemento = self.matriz_letras[2][6]
		((a,b), (c,d)) = (elemento.get_posicion(), flecha.get_tamanio())
		flecha.set_posicion( (a,b-d) )

		# Horizontales
		flecha = self.flechas['FILA']
		elemento = self.matriz_letras[0][9]
		((a,b), (c,d)) = (elemento.get_posicion(), flecha.get_tamanio())
		flecha.set_posicion( (a - c, b) )
		flecha = self.flechas['BORDE']
		elemento = self.matriz_letras[2][8]
		((a,b), (c,d)) = (elemento.get_posicion(), flecha.get_tamanio())
		flecha.set_posicion( (a-c,b) )
		flecha = self.flechas['ESQUINA']
		elemento = self.matriz_letras[4][3]
		((a,b), (c,d)) = (elemento.get_posicion(), flecha.get_tamanio())
		flecha.set_posicion( (a-c,b) )
		flecha = self.flechas['OPUESTA']
		elemento = self.matriz_letras[6][0]
		((a,b), (c,d)) = (elemento.get_posicion(), flecha.get_tamanio())
		flecha.set_posicion( (a-c,b) )
		flecha = self.flechas['PEATON']
		elemento = self.matriz_letras[-1][6]
		((a,b), (c,d)) = (elemento.get_posicion(), flecha.get_tamanio())
		flecha.set_posicion( (a-c,b) )

		ultimo = self.matriz_letras[-1][-1]
		x, y = ultimo.get_posicion()
		w, h = ultimo.get_tamanio()
		posbuttons = (x+w,y+h)

		for fila in self.matriz_letras:
			for letra in fila:
				if not letra.letra:
					fila.remove(letra)
					letra.kill()

		y = posbuttons[1] + 60
		for boton in self.botones[6:]:
			w,h = boton.get_tamanio()
			x = posbuttons[0] - w
			boton.set_posicion( (x, y) )
			y += h + 10
		y = posbuttons[1] + 60
		posbuttons = (posbuttons[0] - (w+10), posbuttons[1])
		for boton in self.botones[4:6]:
			w,h = boton.get_tamanio()
			x = posbuttons[0] - w
			boton.set_posicion( (x, y) )
			y += h + 10
		y = posbuttons[1] + 60
		posbuttons = (posbuttons[0] - (w+10), posbuttons[1])
		for boton in self.botones[2:4]:
			w,h = boton.get_tamanio()
			x = posbuttons[0] - w
			boton.set_posicion( (x, y) )
			y += h + 10
		y = posbuttons[1] + 60
		posbuttons = (posbuttons[0] - (w+10), posbuttons[1])
		for boton in self.botones[:2]:
			w,h = boton.get_tamanio()
			x = posbuttons[0] - w
			boton.set_posicion( (x, y) )
			y += h + 10

		x, y = (G.RESOLUCION[0]/2 + 175, 150)
		for label in self.textos:
			label.set_posicion((x,y))
			y += label.get_tamanio()[1]+10

		a,b,c,d = (0,0,0,0)
		a,b = self.textos[0].get_posicion()
		for label in self.textos:
			e,f = label.get_tamanio()
			if e > c: c = e
			if f > d: d = f
		sombra = JAMG.get_Sombra((c+40, self.textos[-1].get_posicion()[1]-b + d + 40),
			(92,193,235,255), 80)
		sombra = sombra.sprites()[0]
		sombra.rect.x, sombra.rect.y = (a-20, b-20)
		self.add(sombra)
		for label in self.textos:
			self.add(label)

	def seleccionar(self, boton):
		for bot in self.botones:
			if not bot.ubicado:
				bot.connect(callback = self.main.toma, sonido_select = None)
				bot.reset()
		boton.connect(callback = None, sonido_select = None)
		boton.seleccionar()

	def marcar(self, flecha):
		for letra in self.palabras[flecha.nombre]:
			letra.set_text(texto = letra.letra)
			flecha.kill()

class Boton(JAMButton):
	def __init__(self, texto):
		JAMButton.__init__(self, texto, None)
		self.ubicado = False
		fuente, tamanio = JAMG.get_Font_fawn()
		self.set_font_from_file(fuente, tamanio = 30)
		self.set_tamanios(tamanio = (150, 25), grosorbor=1, detalle=1, espesor=1)
		self.colorcara, self.colorbase, self.colorborde, g, d, e = JAMG.get_default_jambutton_values()
		self.colormarca = (92,193,235,255)
		self.reset()
	def reset(self):
		self.set_colores(colorbas = self.colorbase,
			colorbor = self.colorborde, colorcara = self.colorcara)
	def seleccionar(self):
		self.set_colores(colorbas = self.colormarca,
			colorbor = self.colormarca, colorcara = self.colormarca)
	def marcar(self):
		self.ubicado = True
		self.connect(callback = None, sonido_select = None)
		self.set_colores(colorbas = self.colorbase,
			colorbor = self.colorbase, colorcara = self.colorbase)

class Flecha(JAMButton):
	def __init__(self, nombre, imagen):
		JAMButton.__init__(self, '',imagen)
		self.nombre = nombre
		self.set_tamanios(tamanio = (50, 50), grosorbor=1, detalle=1, espesor=1)
		imagen = pygame.image.load(imagen)
		self.final_select = JAMG.get_Rectangulo((240,150,0,255), (50,50))
		self.final_select.blit(imagen,(0,0))
		self.final_unselect = imagen
		self.image = self.final_unselect
		self.rect = self.image.get_rect()

class Letra(JAMButton):
	def __init__(self, letra):
		JAMButton.__init__(self, '',None)
		fuente, tamanio = JAMG.get_Font_fawn()
		self.set_font_from_file(fuente, tamanio = 30)
		self.letra = letra
		#if self.letra: self.set_text(texto = self.letra)
		self.set_tamanios(tamanio = (50, 50), grosorbor=1, detalle=1, espesor=1)
	def update(self):
		pass

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
		self.main = main
		imagen = G.get_Flecha()
		salir = JAMButton("",None)
		salir.set_imagen(origen = imagen, tamanio=(100,55))
		salir.set_colores(colorbas=JAMG.get_negro(), colorcara=JAMG.get_negro())
		salir.set_tamanios(tamanio=(0,0), grosorbor=1, detalle=1, espesor=1)
		salir.set_posicion(punto= (10,10))
		#salir.connect (callback = self.main.run_dialog_intro)
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

