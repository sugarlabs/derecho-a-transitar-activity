#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 21/04/2011 - CeibalJAM! - Uruguay
#   JAMBoardEntryText.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys, tempfile
from pygame.locals import *
gc.enable()

import JAMGlobals as VG
from JAMBoard import JAMBoard
from JAMEntryText import JAMEntryText

class JAMBoardEntryText(pygame.sprite.OrderedUpdates):
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)

		self.posicion= (100,25)
		self.text_buffer= []
		self.tamanio_buffer= 87
		self.tilde= False
		self.tildes= VG.get_tildes_up()
		self.callback_enter= None

		# Colores de la base
		self.colores= {"base":VG.get_blanco(), "bordes":VG.get_negro()}

		self.board= None
		self.entry= None
		self.frame_entry= pygame.sprite.Sprite()

		self.Reconstruye_JAMBoardEntryText(["todo"])

		self.JAMObjects= {"Buffer": self.text_buffer, "Frame": self.frame_entry, "Board": self.board, "EntryText": self.entry}

	# ------------- GETS ------------------------
	def get_tamanio(self):
		return (self.frame_entry.rect.w, self.frame_entry.rect.h)

	# ------------ SETEOS -----------------------
	def set_posicion(self, punto=(0,0)):
		''' Setea la posición de JAMBoardEntryText. '''
		if type(punto) == tuple and type(punto[0]) == int and type(punto[1]) == int:
			self.posicion= punto
			self.frame_entry.rect.x, self.frame_entry.rect.y= self.posicion
			x,y= (self.posicion[0], self.posicion[1] + self.frame_entry.rect.h - self.board.grosor_borde1/2)
			self.board.set_posicion(punto= (x,y))
			centro= (self.frame_entry.rect.centerx, self.frame_entry.rect.centery)
			x,y= (centro[0]-self.entry.frame.rect.w/2, centro[1]-self.entry.frame.rect.h/2)
			self.entry.set_posicion(punto= (x, y))

	def set_center(self, punto= None):
		''' Centra JAMBoardEntryText en el punto indicado. '''
		w,h= (0,0)
		if not punto or type(punto) != tuple or type(punto[0]) != int or type(punto[1]) != int:
			w,h= (pygame.display.Info().current_w, pygame.display.Info().current_h)
			posicion= (w/2-self.frame_entry.rect.w/2, h/2-self.frame_entry.rect.h/2-self.board.frame.rect.h/2)
			self.set_posicion(punto=posicion)
		elif type(punto) == tuple and type(punto[0]) == int and type(punto[1]) == int:
			posicion= (punto[0]-self.frame_entry.rect.w/2, punto[1]-self.frame_entry.rect.h/2-self.board.frame.rect.h/2)
			self.set_posicion(punto=posicion)

	def  set_estilo(self, colorbase, colorborde, colorcara):
		''' Setea los colores del control a partir de un estilo predefinido. '''
		self.board.set_estilo("todos", colorbase, colorborde, colorcara)
		self.entry.set_entry(tipo_letra=None, tamanio_letra=None, color_texto=None, color_fondo=colorborde)
		self.Reconstruye_JAMBoardEntryText(["estilo"])

	def connect_callback_enter(self, callback):
		''' Conecta click sobre el botón enter a una función que recibirá el texto en el buffer de JAMBoardEntryText.'''
		self.callback_enter= callback
		
	# ------------ CONSTRUCCIÓN -----------------------
	def Reconstruye_JAMBoardEntryText(self, cambios):
		'''Reconstruye JAMBoardEntryText cuando se setean valores en él. '''
		if "todo" in cambios:
			self.board= JAMBoard()
			self.entry= JAMEntryText()
			self.frame_entry.image= self.get_frame_entry()
			self.frame_entry.rect= self.frame_entry.image.get_rect()

			self.add(self.frame_entry)
			self.add(self.board)
			self.add(self.entry)

			# Reconectando Click sobre los botones de los JAMBoardTypes
			self.board.board_simbolos.set_callback(self.handle_click)
			self.board.board_letras.set_callback(self.handle_click)
			self.board.board_numeros.set_callback(self.handle_click)
			self.board.board_matematicas.set_callback(self.handle_click)
			self.board.board_otros.set_callback(self.handle_click)
			self.board.board_especiales.set_callback(self.handle_click)

			self.set_posicion(punto=self.posicion)
		
		if "estilo" in cambios:
			self.frame_entry.image= self.get_frame_entry()
			self.set_posicion(punto=self.posicion)

	def get_frame_entry(self):
		w= self.board.frame.rect.w - (self.board.grosor_borde1 + self.board.separador1)*2
		h= self.entry.frame.rect.h + (self.board.grosor_borde2 + self.board.separador2)*2
		contenedor1= VG.get_Rectangulo(self.board.colores["base"], (w,h))
		contenedor1= VG.get_my_surface_whit_border(contenedor1, self.board.colores["bordes"], self.board.grosor_borde2)
		a,b,w,h= contenedor1.get_rect()
		w += (self.board.grosor_borde1 + self.board.separador1)*2
		h += (self.board.grosor_borde1 + self.board.separador1)*2
		contenedor2= VG.get_Rectangulo(self.board.colores["base"], (w,h))
		contenedor2= VG.pegar_imagenes_centradas(contenedor1, contenedor2)
		contenedor2= VG.get_my_surface_whit_border(contenedor2, self.board.colores["bordes"], self.board.grosor_borde1)
		return contenedor2
	# ------------ CONSTRUCCIÓN -----------------------
	
	# ----------- DETECTOR DE EVENTOS ----------------
	def handle_click(self, boton=None):
		''' Detecta los click sobre los botones devolviendo la letra o simbolo que el mismo contiene. '''
		''' Correcciones del 29 de mayo de 2011 tras modificar callback de JAMButton pasandose a si mismo en la llamada. '''
		'''
		posicion = pygame.mouse.get_pos()
		for boton in self.board.board_letras.botones:
			if boton.rect.collidepoint(posicion):
				texto= boton.get_text()
				if self.tilde:
					if texto== "A":
						texto= self.tildes[0]
					elif texto== "E":
						texto= self.tildes[1]
					elif texto== "I":
						texto= self.tildes[2]
					elif texto== "O":
						texto= self.tildes[3]
					elif texto== "U":
						texto= self.tildes[4]
				
				self.text_buffer.append( texto )
				self.tilde= False
				return self.set_bufferentry() '''
		'''
		for boton in self.board.board_numeros.botones:
			if boton.rect.collidepoint(posicion):
				self.text_buffer.append( boton.get_text() )
				self.tilde= False
				return self.set_bufferentry()'''
		'''
		for boton in self.board.board_simbolos.botones:
			if boton.rect.collidepoint(posicion):
				self.text_buffer.append( boton.get_text() )
				self.tilde= False
				return self.set_bufferentry()'''
		'''
		for boton in self.board.board_otros.botones:
			if boton.rect.collidepoint(posicion):
				self.text_buffer.append( boton.get_text() )
				self.tilde= False
				return self.set_bufferentry()'''
		'''
		for boton in self.board.board_matematicas.botones:
			if boton.rect.collidepoint(posicion):
				self.text_buffer.append( boton.get_text() )
				self.tilde= False
				return self.set_bufferentry()'''
		'''
		for boton in self.board.board_especiales.botones:
			if boton.rect.collidepoint(posicion):
				texto= boton.get_text()
				if texto== "Espacio":
				# agrega un espacio en el buffer
					self.text_buffer.append( " " )
					self.tilde= False
					return self.set_bufferentry()

				elif texto== "Borrar":
				# Borra el último caracter ingresado
					if len(self.text_buffer) <= 1:
						self.text_buffer= [ " " ]
					else:
						self.text_buffer= self.text_buffer[0:-1]
					self.tilde= False
					return self.set_bufferentry()

				elif texto== "Enter":
				# Llama a la función conectada al click del botón enter, pasandole como parámetro el texto en el buffer
					self.tilde= False
					if self.callback_enter:
						buf= ""
						for x in self.text_buffer:
							buf += x
						return self.callback_enter(buf)

				elif texto== "´":
					self.tilde= True '''

		if boton in self.board.board_letras.botones:
			texto= boton.get_text()
			if self.tilde:
				if texto== "A":
					texto= self.tildes[0]
				elif texto== "E":
					texto= self.tildes[1]
				elif texto== "I":
					texto= self.tildes[2]
				elif texto== "O":
					texto= self.tildes[3]
				elif texto== "U":
					texto= self.tildes[4]
		
			self.text_buffer.append( texto )
			self.tilde= False
			return self.set_bufferentry()

		elif boton in self.board.board_numeros.botones:
			self.text_buffer.append( boton.get_text() )
			self.tilde= False
			return self.set_bufferentry()

		elif boton in self.board.board_simbolos.botones:
			self.text_buffer.append( boton.get_text() )
			self.tilde= False
			return self.set_bufferentry()

		elif boton in self.board.board_otros.botones:
			self.text_buffer.append( boton.get_text() )
			self.tilde= False
			return self.set_bufferentry()

		elif boton in self.board.board_matematicas.botones:
			self.text_buffer.append( boton.get_text() )
			self.tilde= False
			return self.set_bufferentry()

		elif boton in self.board.board_especiales.botones:
			texto= boton.get_text()
			if texto== "Espacio":
			# agrega un espacio en el buffer
				self.text_buffer.append( " " )
				self.tilde= False
				return self.set_bufferentry()

			elif texto== "Borrar":
			# Borra el último caracter ingresado
				if len(self.text_buffer) <= 1:
					self.text_buffer= [ " " ]
				else:
					self.text_buffer= self.text_buffer[0:-1]
				self.tilde= False
				return self.set_bufferentry()

			elif texto== "Enter":
			# Llama a la función conectada al click del botón enter, pasandole como parámetro el texto en el buffer
				self.tilde= False
				if self.callback_enter:
					buf= ""
					for x in self.text_buffer:
						buf += x
					return self.callback_enter(buf)

			elif texto== "´":
				self.tilde= True
				

	def set_bufferentry(self):
		if len(self.text_buffer) < self.tamanio_buffer:
			buf= ""
			for x in self.text_buffer:
				buf += x
			self.entry.set_buffer(buf)
			self.set_posicion(punto=self.posicion)

	def Describe(self):
		''' Describe la Estructura de Este Control. '''
		estructura =  '''
		Estructura JAMBoardEntryText:

			JAMObject:
				Frame
				Text_Buffer
				JAMBoard
				EntryText'''

		print estructura, "\n"
		print "Ejemplo, Configuración actual:\n"
		print "\t", self.JAMObjects.keys(), "\n"
		for k in self.JAMObjects.items():
			print k, "\n"

# ----- FIN DE CLASE JAMBoardEntryText - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
class Ejemplo(object):
	def __init__(self):
		self.ventana = None
		self.reloj = None
		self.nivel = "menu_0"

		self.fondo = None
		self.widgets = None

		self.resolucion = (1000,500)

		self.setup()
		self.Run()

	def setup(self):
		pygame.init()
		pygame.display.set_mode(self.resolucion , 0, 0)
		pygame.display.set_caption("Ejemplo")

		self.fondo = self.get_Fondo()

		self.widgets = JAMBoardEntryText()
		self.widgets.connect_callback_enter(self.Imprime_buffer)
		a,b,c= VG.get_estilo_naranja()
		self.widgets.set_estilo(a, b, c)
		self.widgets.set_center(punto= (500,250))

		self.ventana = pygame.display.get_surface()
		self.reloj = pygame.time.Clock()

		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN,
					KEYUP, USEREVENT, QUIT, ACTIVEEVENT])
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN, VIDEORESIZE, VIDEOEXPOSE])
		pygame.mouse.set_visible(True)

	def Run(self):
		self.ventana.blit(self.fondo, (0,0))
		self.widgets.draw(self.ventana)
		pygame.display.update()

		contador = 0
		while self.nivel == "menu_0":
			self.reloj.tick(35)
	
			cambios=[]
			self.widgets.clear(self.ventana, self.fondo)
			
			if contador == 150:
				# Activa la siguiente línea para provocar cambios en el tipo de botones en JAMBoardEntryText
				#contador= self.ejemplo_cambia_tipo_de_botones()
				# Activa la siguiente línea para provocar cambios de colores en JAMBoardEntryText
				#contador= self.ejemplo_cambia_colors_Board()
				# Activa la siguiente línea para provocar cambios de texto en Botones
				#contador= self.ejemplo_cambia_texto_en_JAMBoardEntryText()
				# Activa la siguiente línea para provocar cambios de posicion en JAMBoardEntryText
				#contador= self.ejemplo_cambia_posicion_de_JAMBoardEntryText()
				# Activa la siguiente línea para desconectar el sonido select sobre los botones
				#self.widgets.set_reconnect_sound(None)
				# Activa la siguiente línea para ver el contenido del buffer de JAMBoardEntryText
				#print self.widgets.text_buffer
				# Activa la siguiente línea para cambiar los estilos de colores en JAMBoardEntryText
				#contador= self.ejemplo_cambia_estilos()
				contador= 0

			self.widgets.update()
			self.handle_event()
			pygame.event.clear()
			cambios.extend ( self.widgets.draw(self.ventana) )
			pygame.display.update(cambios)
			contador += 1

	'''
	def ejemplo_cambia_estilos(self):
		import random
		estilos= [VG.get_estilo_naranja(), VG.get_estilo_gris(), VG.get_estilo_celeste()]
		a,b,c= random.choice(estilos)
		cambios = ["simbolos", "letras", "numeros", "matematicas", "otros", "especiales",
				"simbolos", "letras", "numeros", "matematicas", "otros", "especiales", "todos"]
		tipo = random.choice(cambios)
		self.widgets.set_estilo(tipo,a,b,c)

	def ejemplo_cambia_tipo_de_botones(self):
		import random
		cambios = ["rectangulo", "elipse"]
		tipo = random.choice(cambios)
		self.widgets.set_tipo_button(tipo)

	def ejemplo_cambia_texto_en_JAMBoardEntryText(self):
		import random
		cambios = ["tipo", "tamanio", "color"]
		modificar = random.choice(cambios)
		if modificar == "tipo":
			tipos= ["Arial", "Purisa", "Times New Roman", "Vardana", "Impact", pygame.font.get_default_font()]
			tipo=random.choice(tipos)
			self.widgets.set_text(tipo=random.choice(tipos), tamanio=None, color=None)
		if modificar == "tamanio":
			tamanios= [10,15,20,25]
			tamanio=random.choice(tamanios)
			self.widgets.set_text(tipo=None, tamanio=tamanio, color=None)
		if modificar == "color":
			colores= [(0,0,0,255), (100,100,255,255), (110,25,255,255), (255,125,55,255)]
			color = random.choice(colores)
			self.widgets.set_text(tipo=None, tamanio=None, color=color)
		return 0

	def ejemplo_cambia_colors_Board(self):
		import random
		cambios = ["colorbas", "colorbor", "colorcara"]
		modificar = random.choice(cambios)

		colores= [(10,20,100,255), (128,128,128,255), (255,255,255,255), (200,100,0,255), (240,150,0,255), (255,220,0,255)]
		color=random.choice(colores)

		self.widgets.set_color_base(random.choice(colores), random.choice(colores))
		
		if modificar == "colorbor":
			self.widgets.set_colors_buttons(base=None, bordes=color, cara=None)
		if modificar == "colorbas":
			self.widgets.set_colors_buttons(base=color, bordes=None, cara=None)
		if modificar == "colorcara":
			self.widgets.set_colors_buttons(base=None, bordes=None, cara=color)
		return 0
	
	def ejemplo_cambia_posicion_de_JAMBoardEntryText(self):
		import random
		tipos= ["centro", "normal"]
		tipo=random.choice(tipos)
		if tipo == "centro":
			posiciones= [(500,400), None]
			posicion= (random.choice(posiciones))
			self.widgets.set_center(punto= posicion)
		elif tipo == "normal":
			return
			posiciones= [(10,20),(25,25),(50,20), (85,100), (100,150)]
			posicion=random.choice(posiciones)
			self.widgets.set_posicion(punto=posicion)
		return 0 '''

	def Imprime_buffer(self, buf):
		print buf
		self.salir()

	def get_Fondo(self):
		superficie = pygame.Surface( self.resolucion, flags=HWSURFACE )
		superficie.fill(VG.get_gris1())
		return superficie

	def handle_event(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				self.salir()
		pygame.event.clear()

	def salir(self):
		print "\n"
		self.widgets.Describe()
		pygame.quit()
		sys.exit()



if __name__ == "__main__":
	Ejemplo()
