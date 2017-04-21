#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import os
import gc
import sys
import gtk
import gobject
from pygame.locals import *
import Globals as G
gc.enable()
import BiblioJAM
from BiblioJAM.JAMButton import JAMButton
from BiblioJAM.JAMLabel import JAMLabel
from BiblioJAM.JAMEntryText import JAMEntryText
from BiblioJAM.JAMBoardEntryText import JAMBoardEntryText
import BiblioJAM.JAMGlobals as JAMG

class Crear_Usuario(gtk.Widget):
	__gsignals__ = {"run":(gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
	"back":(gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, [])}
	def __init__(self):
		gtk.Widget.__init__(self)
		self.ventana = None
		self.estado = False
		self.fondo = None
		self.reloj = None
		self.frame = None
		self.ventana_real = None
		self.resolucionreal = None
		self.VA = None
		self.VH = None
		self.load()
		self.estado = "Intro"

	def run(self):
		self.ventana.blit(self.fondo, (0,0))
		self.frame.draw(self.ventana)
		pygame.display.update()
		while self.estado == "Intro":
			self.reloj.tick(35)
			while gtk.events_pending():
			    	gtk.main_iteration(False)
			G.Traduce_posiciones(self.VA, self.VH)
			self.frame.clear(self.ventana, self.fondo)
			self.frame.update()
			self.handle_event_Intro()
			pygame.event.clear()
			self.frame.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()

	def emit_volver(self, button=None):
		self.estado = None
		self.emit("back")
	
	def handle_event_Intro(self):
		for event in pygame.event.get(pygame.KEYDOWN):
			tecla = event.key
			if tecla == pygame.K_ESCAPE:
				return self.emit_volver()

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
		imagen = os.path.join(G.IMAGENES, "Login", "fondo.jpg")
		self.fondo = pygame.transform.scale(pygame.image.load(imagen), G.RESOLUCION)
		self.reloj = pygame.time.Clock()
		self.frame = Frame(self)
		self.frame.center(self.fondo.get_size())

	def crear_usuario(self, usuario):
		self.estado = None
		self.emit("run", usuario)

class Frame(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		imagen = os.path.join(G.IMAGENES, "Login", "fondo_selecciona.png")
		imagen = pygame.transform.scale(pygame.image.load(imagen), (800, 570))
		fuente, tamanio = JAMG.get_Font_fawn()
		imagen_teclado = os.path.join(G.IMAGENES, "icono_teclado.jpg")

		self.main = main
		self.estado = None

		self.usuario = {
		'nombre':'',
		'edad':'',
		'escuela':'',
		'clase':'',
		'departamento':'',
		'personaje':'' }

		self.jacinto = BotonUsuario()
		imagenusuario = os.path.join(G.IMAGENES, "Login", "jacinto.png")
		self.jacinto.set_imagen(origen = imagenusuario)
		self.jacinto.connect(callback = self.select_personaje, sonido_select = None)

		self.jose = BotonUsuario()
		imagenusuario = os.path.join(G.IMAGENES, "Login", "jose.png")
		self.jose.set_imagen(origen = imagenusuario)
		self.jose.connect(callback = self.select_personaje, sonido_select = None)

		self.natalia = BotonUsuario()
		imagenusuario = os.path.join(G.IMAGENES, "Login", "natalia.png")
		self.natalia.set_imagen(origen = imagenusuario)
		self.natalia.connect(callback = self.select_personaje, sonido_select = None)

		self.personajes = [self.jacinto, self.jose, self.natalia]

		self.entrys = []
		self.board = Board()

		self.fondo = pygame.sprite.Sprite()
		self.fondo.image = (imagen)
		self.fondo.rect = self.fondo.image.get_rect()
		self.add(self.fondo)
		imagen = G.get_Flecha()
		salir = JAMButton("",None)
		salir.set_imagen(origen = imagen, tamanio = (100,55))
		salir.set_colores(colorbas = JAMG.get_negro(), colorcara = JAMG.get_negro())
		salir.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
		salir.set_posicion(punto = (10,10))
		salir.connect(callback = main.emit_volver, sonido_select = None)
		self.add(salir)

		# Ingresar nombre
		self.label_nombre = JAMLabel("Nombre:")
		self.label_nombre.set_text(color = (255,255,255,255))
		self.label_nombre.set_font_from_file(fuente, tamanio = 30)
		self.add(self.label_nombre)
		self.entry_nombre = JAMButton("",None)
		self.entrys.append(self.entry_nombre)
		self.add(self.entry_nombre)

		# Ingresar Edad
		self.label_edad = JAMLabel("Edad:")
		self.label_edad.set_text(color = (255,255,255,255))
		self.label_edad.set_font_from_file(fuente, tamanio = 30)
		self.add(self.label_edad)
		self.entry_edad = JAMButton("",None)
		self.entrys.append(self.entry_edad)
		self.add(self.entry_edad)

		# Ingresar escuela
		self.label_escuela = JAMLabel("Escuela:")
		self.label_escuela.set_text(color = (255,255,255,255))
		self.label_escuela.set_font_from_file(fuente, tamanio = 30)
		self.add(self.label_escuela)
		self.entry_escuela = JAMButton("",None)
		self.entrys.append(self.entry_escuela)
		self.add(self.entry_escuela)

		# Ingresar Clase
		self.label_clase = JAMLabel("Clase:")
		self.label_clase.set_text(color = (255,255,255,255))
		self.label_clase.set_font_from_file(fuente, tamanio = 30)
		self.add(self.label_clase)
		self.entry_clase = JAMButton("",None)
		self.entrys.append(self.entry_clase)
		self.add(self.entry_clase)

		# Ingresar departamento
		self.label_departamento = JAMLabel("Departamento:")
		self.label_departamento.set_text(color = (255,255,255,255))
		self.label_departamento.set_font_from_file(fuente, tamanio = 30)
		self.add(self.label_departamento)
		self.entry_departamento = JAMButton("",None)
		self.entrys.append(self.entry_departamento)
		self.add(self.entry_departamento)

		for boton in self.entrys:
			boton.set_alineacion_label("izquierda")
			boton.set_imagen(origen = imagen_teclado)
			boton.set_font_from_file(fuente, tamanio = 25)
			boton.set_tamanios(tamanio = (300, 35), grosorbor = 1, detalle = 1, espesor = 1)
			boton.connect(callback = None, sonido_select = None)

		self.label_derecho = JAMLabel("Selecciona un Personaje:")
		self.label_derecho.set_text(color = (255,255,255,255))
		self.label_derecho.set_font_from_file(fuente, tamanio = 30)
		self.add(self.label_derecho)

		self.boton_crear = JAMButton("Crear",None)
		self.boton_crear.set_font_from_file(fuente, tamanio = 30)
		self.boton_crear.set_tamanios(tamanio = (200,40), grosorbor = 1, detalle = 1, espesor = 1)
		self.boton_crear.set_colores(colorbas = (0,157,224,255),
			colorbor = (0,157,224,255), colorcara = (92,193,235,255))
		#self.boton_crear.set_colores(colorbas = (92,193,235,255),
		#	colorbor = (255,255,255,255), colorcara = (92,193,235,255))
		self.boton_crear.set_text(color=(255,255,255,255))
		self.boton_crear.connect(callback = self.crear_usuario, sonido_select = None)

		self.add(self.boton_crear)

		self.add(self.jacinto)
		self.add(self.jose)
		self.add(self.natalia)

		self.entry_nombre.connect(callback = self.enter_nombre)
		self.entry_edad.connect(callback = self.enter_edad)
		self.entry_escuela.connect(callback = self.enter_escuela)
		self.entry_clase.connect(callback = self.enter_clase)
		self.entry_departamento.connect(callback = self.enter_departamento)

	def center(self, fondo_size):
		sep = 10
		w,h = fondo_size
		x, y = (w/2 - self.fondo.rect.w/2, h/2 - self.fondo.rect.h/2)
		self.fondo.rect.x, self.fondo.rect.y = (x, y)

		x += sep*2
		y += sep*2

		self.label_nombre.set_posicion( (x,y) )
		y += self.label_nombre.get_tamanio()[1]
		self.entry_nombre.set_posicion( (x,y) )
		y += sep*3 + self.entry_nombre.get_tamanio()[1]

		self.label_edad.set_posicion( (x,y) )
		y += self.label_edad.get_tamanio()[1]
		self.entry_edad.set_posicion( (x,y) )
		y += sep*3 + self.entry_edad.get_tamanio()[1]

		self.label_escuela.set_posicion( (x,y) )
		y += self.label_escuela.get_tamanio()[1]
		self.entry_escuela.set_posicion( (x,y) )
		y += sep*3 + self.entry_escuela.get_tamanio()[1]

		self.label_clase.set_posicion( (x,y) )
		y += self.label_clase.get_tamanio()[1]
		self.entry_clase.set_posicion( (x,y) )
		y += sep*3 + self.entry_clase.get_tamanio()[1]

		self.label_departamento.set_posicion( (x,y) )
		y += self.label_departamento.get_tamanio()[1]
		self.entry_departamento.set_posicion( (x,y) )

		w,h = fondo_size
		mitad = self.fondo.rect.w/2
		ww,hh = self.label_derecho.get_tamanio()
		x =  self.fondo.rect.x + mitad + mitad/2 - ww/2
		y = self.fondo.rect.y + sep*7
		self.label_derecho.set_posicion( (x,y) )

		ww,hh = self.jacinto.get_tamanio()
		x =  self.fondo.rect.x + mitad + mitad/2 - ww - sep
		y = self.label_derecho.get_posicion()[1] + self.label_derecho.get_tamanio()[1] + sep
		self.jacinto.set_posicion( (x,y) )

		x = self.jacinto.get_posicion()[0] + self.jacinto.get_tamanio()[0] + sep
		self.natalia.set_posicion( (x,y) )

		ww,hh = self.jose.get_tamanio()
		x =  self.fondo.rect.x + mitad + mitad/2 - ww/2
		y = self.natalia.get_posicion()[1] + self.natalia.get_tamanio()[1] + sep
		self.jose.set_posicion( (x,y) )

		ww,hh = self.boton_crear.get_tamanio()
		x =  self.fondo.rect.x + mitad + mitad/2 - ww/2
		y =  self.jose.get_posicion()[1] + self.jose.get_tamanio()[1] + sep*5
		self.boton_crear.set_posicion( (x,y) )

	def crear_usuario(self, button):
		if self.usuario['nombre'] and self.usuario['edad'] \
			and self.usuario['escuela'] and self.usuario['clase'] \
			and self.usuario['departamento'] and self.usuario['personaje']:
				self.main.crear_usuario(self.usuario)
		else:
			print "Hay un campo sin llenar"

	def select_personaje(self, button):
		self.usuario['personaje'] = button.origen_imagen
		for personaje in self.personajes:
			if not personaje == button:
				personaje.deseleccionar()
			else:
				personaje.seleccionar()

	def enter_nombre(self, button):
		x,y = button.get_posicion()
		w,h = button.get_tamanio()
		self.board.set_posicion(punto= (x+w,y))
		self.board.callback_enter = self.add_nombre
		self.board.text_buffer = button.get_text()
		self.add(self.board)
		self.run_board(button)
	def add_nombre(self, textbuffer):
		self.estado = None
		if textbuffer: self.usuario['nombre'] = textbuffer
	def enter_edad(self, button):
		x,y = button.get_posicion()
		w,h = button.get_tamanio()
		self.board.set_posicion(punto= (x+w,y))
		self.board.callback_enter = self.add_edad
		self.board.text_buffer = button.get_text()
		self.add(self.board)
		self.run_board(button)
	def add_edad(self, textbuffer):
		self.estado = None
		if textbuffer: self.usuario['edad'] = textbuffer
	def enter_escuela(self, button):
		x,y = button.get_posicion()
		w,h = button.get_tamanio()
		self.board.set_posicion(punto= (x+w,y))
		self.board.callback_enter = self.add_escuela
		self.board.text_buffer = button.get_text()
		self.add(self.board)
		self.run_board(button)
	def add_escuela(self, textbuffer):
		self.estado = None
		if textbuffer: self.usuario['escuela'] = textbuffer
	def enter_clase(self, button):
		x,y = button.get_posicion()
		w,h = button.get_tamanio()
		self.board.set_posicion(punto= (x+w,y))
		self.board.callback_enter = self.add_clase
		self.board.text_buffer = button.get_text()
		self.add(self.board)
		self.run_board(button)
	def add_clase(self, textbuffer):
		self.estado = None
		if textbuffer: self.usuario['clase'] = textbuffer
	def enter_departamento(self, button):
		x,y = button.get_posicion()
		w,h = button.get_tamanio()
		self.board.set_posicion(punto= (x+w,y))
		self.board.callback_enter = self.add_departamento
		self.board.text_buffer = button.get_text()
		self.add(self.board)
		self.run_board(button)
	def add_departamento(self, textbuffer):
		self.estado = None
		if textbuffer: self.usuario['departamento'] = textbuffer

	def run_board(self, button):
		self.estado = "board"
		self.board.draw(self.main.ventana)
		pygame.display.update()
		while self.estado == "board":
			self.main.reloj.tick(35)
			while gtk.events_pending():
			    	gtk.main_iteration(False)
			G.Traduce_posiciones(self.main.VA, self.main.VH)
			self.clear(self.main.ventana, self.main.fondo)
			self.board.update()
			pygame.event.clear()
			button.set_text( texto = self.board.text_buffer)
			self.draw(self.main.ventana)
			self.main.ventana_real.blit(pygame.transform.scale(self.main.ventana, self.main.resolucionreal), (0,0))
			pygame.display.update()
		self.board.clear(self.main.ventana, self.main.fondo)
		self.main.ventana_real.blit(pygame.transform.scale(self.main.ventana, self.main.resolucionreal), (0,0))
		pygame.display.update()
		self.remove(self.board)

class BotonUsuario(JAMButton):
	def __init__(self):
		JAMButton.__init__(self, '', None)
		self.set_tamanios(tamanio = (128,128), grosorbor = 1, detalle = 1, espesor = 1)
	def set_imagen(self, origen):
		self.origen_imagen = origen
		self.original_imagen = pygame.transform.scale(pygame.image.load(origen), (128,128))

		self.final_unselect = self.original_imagen.copy()
		self.final_select = JAMG.get_my_surface_whit_border(self.original_imagen.copy(), (255,255,255,255), 10)
		self.final_marca = JAMG.get_my_surface_whit_border(self.original_imagen.copy(), (240,150,0,255), 10)

		self.image = self.final_unselect
		self.rect = self.image.get_rect()

	def seleccionar(self):
		self.final_unselect = self.final_marca.copy()
		self.final_select = self.final_marca.copy()
		self.image = self.final_marca
	def deseleccionar(self):
		self.final_unselect = self.original_imagen.copy()
		self.final_select = JAMG.get_my_surface_whit_border(self.original_imagen.copy(), (255,255,255,255), 10)
		self.image = self.final_unselect

class Board(pygame.sprite.OrderedUpdates):
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.fuente, tamanio = JAMG.get_Font_fawn()

		self.tamanio = None
		self.base = None
		self.text_buffer = ""
		self.callback_enter = None

		self.letras, self.numeros, self.especiales = self.get_botones_letras()
		botones = self.letras + self.numeros + self.especiales
		self.set_normaliza_tamanios_botones(botones)
		self.set_posicion()

		self.base = pygame.sprite.Sprite()
		self.base.image = JAMG.get_Rectangulo_Transparente(self.tamanio)
		self.base.rect = self.base.image.get_rect()

		self.add(self.base)
		self.add(self.letras)
		self.add(self.numeros)
		self.add(self.especiales)

	def set_buffer(self, button):
		if self.text_buffer == " ": self.text_buffer = ""
		texto = button.get_text()
		if texto and texto != "Ñ": self.text_buffer += texto # hay un error en Ñ
		if self.text_buffer == " ": self.text_buffer = ""

	def set_back_space(self, button):
		if self.text_buffer:
			if len(self.text_buffer) > 1:
				self.text_buffer = self.text_buffer[:-1]
			else:
				self.text_buffer = " "

	def set_enter(self, button):
		if self.callback_enter: self.callback_enter(self.text_buffer)

	def get_botones_letras(self):
		simbols = JAMG.get_letras_up()
		botones_letras = []
		for letra in simbols:
			boton = JAMButton(letra, None)
			boton.set_font_from_file(self.fuente, tamanio = 20)
			boton.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
			boton.set_colores(colorbas = (0,153,255,255), colorbor = (0,153,255,255), colorcara = (255,255,255,255))
			#boton.set_text(color = (0,153,255,255))
			boton.connect(callback = self.set_buffer, sonido_select = None)
			botones_letras.append(boton)

		simbols = JAMG.get_numeros()
		botones_numeros = []
		for letra in simbols:
			boton = JAMButton(letra, None)
			boton.set_font_from_file(self.fuente, tamanio = 20)
			boton.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
			boton.set_colores(colorbas = (0,153,255,255), colorbor = (0,153,255,255), colorcara = (255,255,255,255))
			#boton.set_text(color = (0,153,255,255))
			boton.connect(callback = self.set_buffer, sonido_select = None)
			botones_numeros.append(boton)

		botones_especiales = []
		for letra in ['', ' ', '']:
			boton = JAMButton(letra, None)
			#boton.set_font_from_file(self.fuente, tamanio = 20)
			boton.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
			boton.set_colores(colorbas = (0,153,255,255), colorbor = (0,153,255,255), colorcara = (255,255,255,255))
			#boton.set_text(color = (0,153,255,255))
			boton.connect(callback = self.set_buffer, sonido_select = None)
			botones_especiales.append(boton)

		imagen = os.path.join(G.IMAGENES, "back.png")
		boton = botones_especiales[0]
		boton.set_imagen(origen = imagen)
		boton.connect(callback = self.set_back_space, sonido_select = None)

		imagen = os.path.join(G.IMAGENES, "enter.png")
		boton = botones_especiales[2]
		boton.set_imagen(origen = imagen)
		boton.connect(callback = self.set_enter, sonido_select = None)

		return (botones_letras, botones_numeros, botones_especiales)

	def set_normaliza_tamanios_botones(self, botones):
		''' Normaliza los Tamaños de los botones. '''
		lado = 0
		for button in botones:
			button.set_tamanios(tamanio = (0,0))
			if button.rect.w > lado:
				lado = button.rect.w
			if button.rect.h > lado:
				lado = button.rect.h
		for button in botones:
			button.set_tamanios(tamanio = (lado,lado))

	def set_posicion(self, punto = (0,0)):
		if self.base:
			self.base.rect.x, self.base.rect.y = punto
		x, y = punto
		for boton in self.numeros:
			boton.set_posicion( (x,y) )
			x += boton.get_tamanio()[0]
		x, y = punto
		y += boton.get_tamanio()[1]
		for boton in self.letras[:9]:
			boton.set_posicion( (x,y) )
			x += boton.get_tamanio()[0]
		x = punto[0]
		y += boton.get_tamanio()[1]
		for boton in self.letras[9:18]:
			boton.set_posicion( (x,y) )
			x += boton.get_tamanio()[0]
		x = punto[0]
		y += boton.get_tamanio()[1]
		for boton in self.letras[18:]:
			boton.set_posicion( (x,y) )
			x += boton.get_tamanio()[0]
		w = self.numeros[0].get_tamanio()[0]*len(self.numeros)
		h = self.numeros[0].get_tamanio()[1]*4
		self.tamanio = (w,h)

		boton = self.numeros[-1]
		x,y = boton.get_posicion()
		w,h = boton.get_tamanio()
		y += h
		self.especiales[0].set_posicion( (x,y) )
		y += h
		self.especiales[1].set_posicion( (x,y) )
		y += h
		self.especiales[2].set_posicion( (x,y) )

