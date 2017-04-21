#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 19/04/2011 - CeibalJAM! - Uruguay
#   JAMBoardTypes.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys
from pygame.locals import *
gc.enable()

import JAMGlobals as VG
from JAMLabel import JAMLabel
from JAMButton import JAMButton

class JAMBoardTypes(pygame.sprite.OrderedUpdates):
	def __init__(self, tipo="letras"):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.tipo= tipo

		if self.tipo == "letras" or self.tipo == "letras_down" or self.tipo == "simbolos":
			self.columnas, self.filas= (9, 3)
		elif self.tipo == "numeros":
			self.columnas, self.filas= (5,2)
		elif self.tipo == "otros":
			self.columnas, self.filas= (6, 1)
		elif self.tipo == "matematicas":
			self.columnas, self.filas= (5,1)
		elif self.tipo == "especiales":
			self.columnas, self.filas= (4, 1)
		else:
			self.tipo= "letras"
			self.columnas, self.filas= (9, 3)

		self.tipo_buttons= "rectangulo"
		self.posicion= (0,0)
		self.text_buffer= ""

		self.colores= {"base":VG.get_blanco(), "bordes":VG.get_negro(), "cara":VG.get_blanco(), "frame": VG.get_blanco()}

		self.botones= None
		self.frame= pygame.sprite.Sprite()
		self.grilla= None

		self.callback= self.handle_click
		self.sonido= VG.get_sound_select()

		self.Reconstruye_JAMBoardTypes(["todo"])

		self.JAMObjects= {"frame": self.frame, "grilla":self.grilla, "botones":self.botones, "text_buffer": self.text_buffer}

	# ------------- GETS ------------------------
	def get_tamanio(self):
		return (self.frame.rect.w, self.frame.rect.h)

	# ------------ SETEOS -----------------------
	def set_buffer(self, texto):
		''' Setea el buffer de texto. '''
		if texto != self.text_buffer:
			self.text_buffer = texto

	def set_colors_buttons(self, base=None, bordes=None, cara=None):
		''' Setea los Colores de los botones. '''
		if not base: base= VG.get_blanco()
		if not bordes: bordes= VG.get_negro()
		if not cara: cara= VG.get_blanco()

		cambios= False
		if base != self.colores["base"]:
			self.colores["base"]= base
			cambios= True
		if bordes != self.colores["bordes"]:
			self.colores["bordes"]= bordes
			cambios= True
		if cara != self.colores["cara"]:
			self.colores["cara"]= cara
			cambios= True
		if cambios:
			self.Reconstruye_JAMBoardTypes(["colores"])

	def set_color_base(self, color):
		''' Setea el color de la base de JAMBoardTypes. '''
		if color and type(color) == tuple and color != self.colores["frame"]:
			self.colores["frame"]= color
			self.get_frame_and_grilla()
			self.set_posicion(punto=self.posicion)

	def set_text(self, tipo=None, tamanio=None, color=None):
		''' Setea el tipo, tamaño y color de las letras en los botones. '''
		cambiosx= False
		for button in self.botones:
			cambios= False
			if type(tipo) == str:
				cambios= True
			if type(tamanio) == int:
				cambios= True
			if type(color) == tuple:
				cambios= True
			if cambios:
				button.set_text(tipo=tipo, tamanio=tamanio, color=color)#, texto=None)
				cambiosx= True
		if cambiosx:
			self.Reconstruye_JAMBoardTypes(["texto"])

	def set_font_from_file(self, direccion_archivo, tamanio= None):
		''' Setea la fuente desde un archivo. '''
		for button in self.botones:
			button.set_font_from_file(direccion_archivo, tamanio)
			self.Reconstruye_JAMBoardTypes(["texto"])

	def set_reconnect_sound(self, sonido):
		''' Reconecta un sonido para "select" sobre el botón. '''
		self.sonido= sonido
		for button in self.botones:
			button.connect(callback= button.callback, sonido_select= self.sonido)
	def set_callback(self, callback):
		''' Reconecta a una función para click sobre el botón. '''
		self.callback= callback
		for button in self.botones:
			button.connect(callback=self.callback, sonido_select=button.sonido_select)

	def set_center(self, punto= None):
		''' Centra JAMBoardTypes en el punto indicado. '''
		if not punto or type(punto) != tuple or type(punto[0]) != int or type(punto[1]) != int:
			posicion= (pygame.display.Info().current_w/2, pygame.display.Info().current_h/2)
			self.set_center(punto= posicion)
		elif type(punto) == tuple and type(punto[0]) == int and type(punto[1]) == int:
			posicion= (punto[0]-self.frame.rect.w/2, punto[1]-self.frame.rect.h/2)
			self.set_posicion(punto=posicion)

	def set_posicion(self, punto=(0,0)):
		''' Setea la posición de cada sprite según la posición proporcionada por el usuario para todo el control. '''
		if type(punto) == tuple and type(punto[0]) == int and type(punto[1]) == int:
			# SE MUEVE LA BASE DE LAS LETRAS
			self.posicion= punto
			x,y= self.posicion
			self.frame.rect.x= x
			self.frame.rect.y= y
			# SE MUEVEN LAS LETRAS
			for n in range (0, len(self.botones)):
				xx, yy= (self.grilla[n][0]+x, self.grilla[n][1]+y)
				self.botones[n].set_posicion(punto=(xx,yy))

	def set_tipo_button(self, tipo):
		''' Cambia el tipo de los botones. (puede ser "rectangulo" o "elipse"). '''
		if tipo == "rectangulo" or tipo == "elipse" and tipo != self.tipo_buttons:
			self.tipo_buttons= tipo
			for button in self.botones:
				button.set_tipo(self.tipo_buttons)
			self.Reconstruye_JAMBoardTypes(["tipo"])
	# ------------ SETEOS -----------------------

	# ------------ CONSTRUCCIÓN -----------------------
	def Reconstruye_JAMBoardTypes(self, cambios):
		''' Reconstruye JAMBoardTypes cuando se setean valores en él. '''
		if "todo" in cambios:
			self.botones= self.get_botones_letras()
			self.set_normaliza_tamanios_botones()
			self.get_frame_and_grilla()
			self.add(self.frame)
			self.add(self.botones)
			self.set_posicion(punto=self.posicion)
		if "tipo" in cambios or "texto" in cambios:
			self.set_normaliza_tamanios_botones()
			self.get_frame_and_grilla()
			self.set_posicion(punto=self.posicion)
		if "colores" in cambios:
			for button in self.botones:
				button.set_colores(colorbas=self.colores["base"], colorbor=self.colores["bordes"], colorcara=self.colores["cara"])

	def get_botones_letras(self):
		''' Construye y Devuelve los Botones. '''
		if self.tipo == "letras":
			simbols= VG.get_letras_up()
		elif self.tipo == "numeros":
			simbols= VG.get_numeros()
		elif self.tipo == "letras_down":
			simbols= VG.get_letras_down()
		elif self.tipo == "simbolos":
			simbols= VG.get_simbols()
		elif self.tipo == "otros":
			simbols= VG.get_otros()
		elif self.tipo == "matematicas":
			simbols= VG.get_matematicas()
		elif self.tipo == "especiales":
			simbols= VG.get_especiales()
		else:
			self.tipo= "letras"
			simbols= VG.get_letras_up()
		botones_letras= []
		for letra in simbols:
			boton= JAMButton(letra, None, tipo= self.tipo_buttons)
			botones_letras.append(boton)
			boton.connect(callback=self.callback, sonido_select=self.sonido)
		return botones_letras
	def set_normaliza_tamanios_botones(self):
		''' Normaliza los Tamaños de los botones. '''
		if self.tipo == "especiales":
			alto= 0
			for button in self.botones:
				button.set_tamanios(tamanio=(0,0)) # Para que queden lo más pequeño posible.
				if button.rect.h > alto: alto= button.rect.h
			for button in self.botones:
				button.set_tamanios(tamanio=(button.rect.w,alto))
		else:
			lado= 0
			for button in self.botones:
				button.set_tamanios(tamanio=(0,0)) # Para que queden lo más pequeño posible.
				if button.rect.w > lado:
					lado= button.rect.w
				if button.rect.h > lado:
					lado= button.rect.h
			for button in self.botones:
				button.set_tamanios(tamanio=(lado,lado))

	def get_frame_and_grilla(self):
		''' Construye el sprite base para los botones de letras y una lista de posiciones para cada botón. '''
		if self.tipo == "especiales":
			ancho, alto= (0,0)
			posiciones= []
			for button in self.botones: # es una sola fila
				posiciones.append( (ancho,alto) )
				ancho += button.rect.w
			alto= button.rect.h
			self.frame.image= VG.get_Rectangulo(self.colores["frame"], (ancho, alto))
			self.frame.rect= self.frame.image.get_rect()
			self.grilla= posiciones
		else:
		# Contenedor para los botones
			ancho, alto=(0,0)
			for x in range(self.columnas):
				ancho+= self.botones[x].rect.w
			for x in range(self.filas):
				alto+= self.botones[x].rect.h
			self.frame.image= VG.get_Rectangulo(self.colores["frame"], (ancho, alto))
			self.frame.rect= self.frame.image.get_rect()
			self.grilla= VG.get_grilla(self.frame.image, self.columnas, self.filas)
	# ------------ CONSTRUCCIÓN -----------------------

	# ----------- DETECTOR DE EVENTOS (es el callback de los botones)----------------
	def handle_click(self, boton=None):
		''' Detecta los click sobre los botones devolviendo la letra o simbolo que el mismo contiene. '''
		''' Modificaciones del 29 de Mayo tras modificar callback de JAMButton para pasarse a si mismo. '''
		'''
		posicion = pygame.mouse.get_pos()
		for boton in self.botones:
			if boton.rect.collidepoint(posicion):
				if self.text_buffer == " ":
					self.text_buffer = ""
				self.text_buffer += boton.get_text()
				#print self.text_buffer
				return '''
		if self.text_buffer == " ":
			self.text_buffer = ""
		self.text_buffer += boton.get_text()
		#print self.text_buffer
		return

	def Describe(self):
		''' Describe la Estructura de Este Control. '''
		estructura =  '''
		Estructura JAMBoardTypes:

			JAMObject:
				Frame
				Grilla
				Botones
				Text_Buffer

			Descripción:

				Frame es un sprite que sirve de imagen base sobre la que se dibujarán los botones.
				Grilla es una lista de posiciones x,y para cada botón.
				Botones son los botones con las letras.
				Text_Buffer donde se guarda el texto que se genera al presionar los botones.
			'''

		print estructura, "\n"
		print "Ejemplo, Configuración actual:\n"
		print "\t", self.JAMObjects.keys(), "\n"
		for k in self.JAMObjects.items():
			print k, "\n"

# ----- FIN DE CLASE JAMBoardTypes - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
class Ejemplo(object):
	def __init__(self):
		self.ventana = None
		self.reloj = None
		self.nivel = "menu_0"

		self.fondo = None
		self.widgets = None

		self.resolucion = (1000,800)

		self.setup()
		self.Run()

	def setup(self):
		pygame.init()
		pygame.display.set_mode(self.resolucion , 0, 0)
		pygame.display.set_caption("Ejemplo")

		self.fondo = self.get_Fondo()

		self.widgets = JAMBoardTypes(tipo="letras")
		self.widgets.set_posicion(punto=(25,25))
		self.widgets.set_tipo_button("elipse")

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
				# Activa la siguiente línea para provocar cambios en el tipo de botones en JAMBoardTypes
				contador= self.ejemplo_cambia_tipo_de_botones()
				# Activa la siguiente línea para provocar cambios de colores en JAMBoardTypes
				contador= self.ejemplo_cambia_colors_Board()
				# Activa la siguiente línea para provocar cambios de texto en Botones
				contador= self.ejemplo_cambia_texto_en_JAMBoardTypes()
				# Activa la siguiente línea para provocar cambios de posicion en JAMBoardTypes
				contador= self.ejemplo_cambia_posicion_de_JAMBoardTypes()
				# Activa la siguiente línea para desconectar el sonido select sobre los botones
				#self.widgets.set_reconnect_sound(None)
				# Activa la siguiente línea para ver el contenido del buffer de JAMBoardTypes
				#print self.widgets.text_buffer
				contador= 0

			self.widgets.update()
			self.handle_event()
			pygame.event.clear()
			cambios.extend ( self.widgets.draw(self.ventana) )
			pygame.display.update(cambios)
			contador += 1

	def ejemplo_cambia_tipo_de_botones(self):
		import random
		cambios = ["rectangulo", "elipse"]
		tipo = random.choice(cambios)
		self.widgets.set_tipo_button(tipo)

	def ejemplo_cambia_texto_en_JAMBoardTypes(self):
		import random
		cambios = ["tipo", "tamanio", "color"]
		modificar = random.choice(cambios)
		if modificar == "tipo":
			tipos= ["Arial", "Purisa", "Times New Roman", "Vardana", "Impact", pygame.font.get_default_font()]
			tipo=random.choice(tipos)
			self.widgets.set_text(tipo=random.choice(tipos), tamanio=None, color=None)
		if modificar == "tamanio":
			tamanios= [8,12,16,20,24,28]
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

		colores= [(10,20,100,255), (128,128,128,255), (255,255,255,255)]
		color=random.choice(colores)
		
		if modificar == "colorbor":
			self.widgets.set_colors_buttons(base=None, bordes=color, cara=None)
		if modificar == "colorbas":
			self.widgets.set_colors_buttons(base=color, bordes=None, cara=None)
		if modificar == "colorcara":
			self.widgets.set_colors_buttons(base=None, bordes=None, cara=color)

		self.widgets.set_color_base(random.choice(colores))
		return 0

	def ejemplo_cambia_posicion_de_JAMBoardTypes(self):
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
		return 0

	def get_Fondo(self):
		superficie = pygame.Surface( self.resolucion, flags=HWSURFACE )
		superficie.fill(VG.get_negro())
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
