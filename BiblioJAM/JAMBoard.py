#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 21/04/2011 - CeibalJAM! - Uruguay
#   JAMBoard.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys
from pygame.locals import *
gc.enable()

import JAMGlobals as VG
from JAMBoardTypes import JAMBoardTypes

class JAMBoard(pygame.sprite.OrderedUpdates):
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)

		self.tipo_buttons= "rectangulo"
		self.posicion= (0,0)
		self.text_buffer= ""

		self.grosor_borde1= 7
		self.separador1= 4
		self.grosor_borde2= 1
		self.separador2= 2

		# Colores de la base
		self.colores= {"base":VG.get_blanco(), "bordes":VG.get_negro()}

		self.xysimbolos= (0,0)
		self.xyletras= (0,0)
		self.xynumeros= (0,0)
		self.xymatematicas= (0,0)
		self.xyotros= (0,0)
		self.xyespeciales= (0,0)

		self.board_simbolos= None
		self.board_letras= None
		self.board_numeros= None
		self.board_matematicas= None
		self.board_otros= None
		self.board_especiales= None

		self.frame= pygame.sprite.Sprite()

		self.Reconstruye_JAMBoard(["todo"])

		self.JAMObjects= {"Buffer": self.text_buffer, "Frame": self.frame, "Simbolos": self.board_simbolos,
				"Letras": self.board_letras, "Numeros": self.board_numeros, "Matematicas": self.board_matematicas,
				"Otros": self.board_otros, "Especiales": self.board_especiales}

	# ------------ SETEOS -----------------------
	def set_estilo(self, board, colorbase, colorborde, colorcara):
		''' Setea una gama de Colores para la base y los botones de cada JAMBoardType según indique el usuario.'''		
		for color in [colorbase, colorborde, colorcara]:
			if type(color) != tuple or len(color) != 4: return
			for valor in color:
				if type(valor) != int: return
		if board == "simbolos":
			self.board_simbolos.set_color_base(colorborde)
			self.board_simbolos.set_colors_buttons(base=colorbase, bordes=colorborde, cara=colorcara)
		if board == "letras":
			self.board_letras.set_color_base(colorborde)
			self.board_letras.set_colors_buttons(base=colorbase, bordes=colorborde, cara=colorcara)
		if board == "numeros":
			self.board_numeros.set_color_base(colorborde)
			self.board_numeros.set_colors_buttons(base=colorbase, bordes=colorborde, cara=colorcara)
		if board == "matematicas":
			self.board_matematicas.set_color_base(colorborde)
			self.board_matematicas.set_colors_buttons(base=colorbase, bordes=colorborde, cara=colorcara)
		if board == "otros":
			self.board_otros.set_color_base(colorborde)
			self.board_otros.set_colors_buttons(base=colorbase, bordes=colorborde, cara=colorcara)
		if board == "especiales":
			self.board_especiales.set_color_base(colorborde)
			self.board_especiales.set_colors_buttons(base=colorbase, bordes=colorborde, cara=colorcara)
		elif board == "todos":
			self.set_color_base(colorborde, colorbase)
			self.set_colors_buttons(base=colorbase, bordes=colorborde, cara=colorcara)

	def set_colors_buttons(self, base=None, bordes=None, cara=None):
		''' Setea los Colores de los botones.'''
		self.board_simbolos.set_colors_buttons(base=base, bordes=bordes, cara=cara)
		self.board_letras.set_colors_buttons(base=base, bordes=bordes, cara=cara)
		self.board_numeros.set_colors_buttons(base=base, bordes=bordes, cara=cara)
		self.board_matematicas.set_colors_buttons(base=base, bordes=bordes, cara=cara)
		self.board_otros.set_colors_buttons(base=base, bordes=bordes, cara=cara)
		self.board_especiales.set_colors_buttons(base=base, bordes=bordes, cara=cara)

	def set_color_base(self, colorbase, colorborde):
		''' Setea el color de la base de JAMBoard. '''
		cambios= False
		if colorbase and type(colorbase) == tuple and colorbase != self.colores["base"]:
			self.colores["base"]= colorbase
			cambios= True
		if colorborde and type(colorborde) == tuple and colorborde != self.colores["bordes"]:
			self.colores["bordes"]= colorborde
			cambios= True
		if cambios:
			self.Reconstruye_JAMBoard(["colors"])

	def set_text(self, tipo=None, tamanio=None, color=None):
		''' Setea el tipo, tamaño y color de las letras en los botones.'''
		cambios= False
		if type(tipo) == str:
			cambios= True
		if type(tamanio) == int:
			cambios= True
		if type(color) == tuple:
			cambios= True
		if cambios:
			self.board_simbolos.set_text(tipo=tipo, tamanio=tamanio, color=color)#, texto=None)
			self.board_letras.set_text(tipo=tipo, tamanio=tamanio, color=color)#, texto=None)
			self.board_numeros.set_text(tipo=tipo, tamanio=tamanio, color=color)#, texto=None)
			self.board_matematicas.set_text(tipo=tipo, tamanio=tamanio, color=color)#, texto=None)
			self.board_otros.set_text(tipo=tipo, tamanio=tamanio, color=color)#, texto=None)
			self.board_especiales.set_text(tipo=tipo, tamanio=tamanio, color=color)#, texto=None)
			self.Reconstruye_JAMBoard(["texto"])

	def set_font_from_file(self, direccion_archivo, tamanio= None):
		''' Setea la fuente desde un archivo. '''
		self.board_simbolos.set_font_from_file(direccion_archivo, tamanio)
		self.board_letras.set_font_from_file(direccion_archivo, tamanio)
		self.board_numeros.set_font_from_file(direccion_archivo, tamanio)
		self.board_matematicas.set_font_from_file(direccion_archivo, tamanio)
		self.board_otros.set_font_from_file(direccion_archivo, tamanio)
		self.board_especiales.set_font_from_file(direccion_archivo, tamanio)
		self.Reconstruye_JAMBoard(["texto"])

	def set_reconnect_sound(self, sonido):
		''' Reconecta un sonido para "select" sobre el botón. '''
		self.board_simbolos.set_reconnect_sound(sonido)
		self.board_letras.set_reconnect_sound(sonido)
		self.board_numeros.set_reconnect_sound(sonido)
		self.board_matematicas.set_reconnect_sound(sonido)
		self.board_otros.set_reconnect_sound(sonido)
		self.board_especiales.set_reconnect_sound(sonido)

	def set_center(self, punto= None):
		''' Centra JAMBoard en el punto indicado. '''
		w,h= (0,0)
		if not punto or type(punto) != tuple or type(punto[0]) != int or type(punto[1]) != int:
			w,h= (pygame.display.Info().current_w, pygame.display.Info().current_h)
			posicion= (w/2-self.frame.rect.w/2, h/2-self.frame.rect.h/2)
			self.set_posicion(punto=posicion)
		elif type(punto) == tuple and type(punto[0]) == int and type(punto[1]) == int:
			posicion= (punto[0]-self.frame.rect.w/2, punto[1]-self.frame.rect.h/2)
			self.set_posicion(punto=posicion)

	def set_posicion(self, punto=(0,0)):
		''' Setea la posición de cada sprite según la posición proporcionada por el usuario para todo el control. '''
		if type(punto) == tuple and type(punto[0]) == int and type(punto[1]) == int:
			self.posicion= punto
			self.frame.rect.x,self.frame.rect.y= self.posicion 
			posicion= (self.xysimbolos[0]+self.posicion[0], self.xysimbolos[1]+self.posicion[1])
			self.board_simbolos.set_posicion(punto=posicion)
			posicion= (self.xyletras[0]+self.posicion[0], self.xyletras[1]+self.posicion[1])
			self.board_letras.set_posicion(punto=posicion)
			posicion= (self.xynumeros[0]+self.posicion[0], self.xynumeros[1]+self.posicion[1])
			self.board_numeros.set_posicion(punto=posicion)
			posicion= (self.xymatematicas[0]+self.posicion[0], self.xymatematicas[1]+self.posicion[1])
			self.board_matematicas.set_posicion(punto=posicion)
			posicion= (self.xyotros[0]+self.posicion[0], self.xyotros[1]+self.posicion[1])
			self.board_otros.set_posicion(punto=posicion)
			posicion= (self.xyespeciales[0]+self.posicion[0], self.xyespeciales[1]+self.posicion[1])
			self.board_especiales.set_posicion(punto=posicion)

	def set_tipo_button(self, tipo):
		''' Cambia el tipo de los botones. (puede ser "rectangulo" o "elipse"). '''
		if tipo == "rectangulo" or tipo == "elipse" and tipo != self.tipo_buttons:
			self.tipo_buttons= tipo
			self.board_simbolos.set_tipo_button(self.tipo_buttons)
			self.board_letras.set_tipo_button(self.tipo_buttons)
			self.board_numeros.set_tipo_button(self.tipo_buttons)
			self.board_matematicas.set_tipo_button(self.tipo_buttons)
			self.board_otros.set_tipo_button(self.tipo_buttons)
			self.board_especiales.set_tipo_button(self.tipo_buttons)
			self.Reconstruye_JAMBoard(["tipo"])

	# ------------- GETS ------------------------
	def get_tamanio(self):
		return (self.frame.rect.w, self.frame.rect.h)

	# ------------ CONSTRUCCIÓN -----------------------
	def Reconstruye_JAMBoard(self, cambios):
		'''Reconstruye JAMBoard cuando se setean valores en él. '''
		if "todo" in cambios:
			self.board_simbolos= JAMBoardTypes("simbolos")
			self.board_letras= JAMBoardTypes("letras")
			self.board_numeros= JAMBoardTypes("numeros")
			self.board_matematicas= JAMBoardTypes("matematicas")
			self.board_otros= JAMBoardTypes("otros")
			self.board_especiales= JAMBoardTypes("especiales")

			self.get_frame()

			self.add(self.frame)
			self.add(self.board_simbolos)
			self.add(self.board_letras)
			self.add(self.board_numeros)
			self.add(self.board_matematicas)
			self.add(self.board_otros)
			self.add(self.board_especiales)

			# Reconectando Click sobre los botones de los JAMBoardTypes
			self.board_simbolos.set_callback(self.handle_click)
			self.board_letras.set_callback(self.handle_click)
			self.board_numeros.set_callback(self.handle_click)
			self.board_matematicas.set_callback(self.handle_click)
			self.board_otros.set_callback(self.handle_click)
			self.board_especiales.set_callback(self.handle_click)

			self.set_posicion(punto=self.posicion)
		
		if "tipo" in cambios or "texto" in cambios:
			self.get_frame()
			self.set_posicion(punto=self.posicion)
		if "colors" in cambios:
			self.get_frame()
			self.board_simbolos.set_color_base(self.colores["base"])
			self.board_letras.set_color_base(self.colores["base"])
			self.board_numeros.set_color_base(self.colores["base"])
			self.board_matematicas.set_color_base(self.colores["base"])
			self.board_otros.set_color_base(self.colores["base"])
			self.board_especiales.set_color_base(self.colores["base"])
			self.set_posicion(punto=self.posicion)

	def get_frame(self):
		# recuadro interior
		sep= self.grosor_borde1 + self.separador1 + self.grosor_borde2 + self.separador2

		espacio1, espacio2=(0,0)
		if self.board_letras.frame.rect.w > self.board_simbolos.frame.rect.w:
			espacio1= self.board_letras.frame.rect.w
		else:
			espacio1= self.board_simbolos.frame.rect.w

		if self.board_especiales.frame.rect.w > self.board_otros.frame.rect.w:
			espacio2= self.board_especiales.frame.rect.w
		else:
			espacio2= self.board_otros.frame.rect.w

		w= (self.grosor_borde2 + self.separador2)*2 + espacio1 + self.separador1 + espacio2
		h= self.board_simbolos.frame.rect.h + (self.grosor_borde2 + self.separador2)*2 + self.separador1 + self.board_letras.frame.rect.h

		# posicion para board letras
		self.xysimbolos= (sep,sep)
		self.xynumeros= (self.xysimbolos[0] + self.board_simbolos.frame.rect.w + self.separador1, self.xysimbolos[1])
		self.xymatematicas= (self.xynumeros[0], self.xynumeros[1] + self.board_numeros.frame.rect.h + self.separador1)

		self.xyletras= (self.xysimbolos[0], self.xysimbolos[1] + self.board_simbolos.frame.rect.h + self.separador1)

		self.xyotros= (self.xyletras[0] + self.board_letras.frame.rect.w + self.separador1, self.xyletras[1] + self.board_letras.frame.rect.h - self.board_otros.frame.rect.h)

		self.xyespeciales= (self.xyletras[0] + self.board_letras.frame.rect.w + self.separador1, self.xyotros[1] - self.separador1 - self.board_especiales.frame.rect.h)

		tamanio= (w,h)
		superficie= VG.get_Rectangulo(self.colores["base"], tamanio)
		superficie= VG.get_my_surface_whit_border(superficie, self.colores["bordes"], self.grosor_borde2)

		# recuadro exterior
		tamanio= (w + (self.grosor_borde1 + self.separador1)*2, h + (self.grosor_borde1 + self.separador1)*2)
		superficie1= VG.get_Rectangulo(self.colores["base"], tamanio)
		superficie1= VG.get_my_surface_whit_border(superficie1, self.colores["bordes"], self.grosor_borde1)

		# armado final de la base
		self.frame.image= VG.pegar_imagenes_centradas(superficie, superficie1)
		self.frame.rect= self.frame.image.get_rect()
	# ------------ CONSTRUCCIÓN -----------------------
	
	# ----------- DETECTOR DE EVENTOS ----------------
	def handle_click(self, boton=None):
		''' Detecta los click sobre los botones devolviendo la letra o simbolo que el mismo contiene. '''
		''' Modificaciones del 29 de Mayo tras modificar callback de JAMButton para pasarse a si mismo. '''
		'''
		posicion = pygame.mouse.get_pos()
		for boton in self.board_letras.botones:
			if boton.rect.collidepoint(posicion):
				if self.text_buffer == " ":
					self.text_buffer = ""
				self.text_buffer += boton.get_text()
				print self.text_buffer
				return
		for boton in self.board_numeros.botones:
			if boton.rect.collidepoint(posicion):
				if self.text_buffer == " ":
					self.text_buffer = ""
				self.text_buffer += boton.get_text()
				print self.text_buffer
				return

		for boton in self.board_simbolos.botones:
			if boton.rect.collidepoint(posicion):
				if self.text_buffer == " ":
					self.text_buffer = ""
				self.text_buffer += boton.get_text()
				print self.text_buffer
				return

		for boton in self.board_otros.botones:
			if boton.rect.collidepoint(posicion):
				if self.text_buffer == " ":
					self.text_buffer = ""
				self.text_buffer += boton.get_text()
				print self.text_buffer
				return

		for boton in self.board_matematicas.botones:
			if boton.rect.collidepoint(posicion):
				if self.text_buffer == " ":
					self.text_buffer = ""
				self.text_buffer += boton.get_text()
				print self.text_buffer
				return

		for boton in self.board_especiales.botones:
			if boton.rect.collidepoint(posicion):
				if self.text_buffer == " ":
					self.text_buffer = ""
				self.text_buffer += boton.get_text()
				print self.text_buffer
				return '''

		if boton in self.board_letras.botones:
			if self.text_buffer == " ":
				self.text_buffer = ""
			self.text_buffer += boton.get_text()
			print self.text_buffer
			return
		elif boton in self.board_numeros.botones:
			if self.text_buffer == " ":
				self.text_buffer = ""
			self.text_buffer += boton.get_text()
			print self.text_buffer
			return
		elif boton in self.board_simbolos.botones:
			if self.text_buffer == " ":
				self.text_buffer = ""
			self.text_buffer += boton.get_text()
			print self.text_buffer
			return
		elif boton in self.board_otros.botones:
			if self.text_buffer == " ":
				self.text_buffer = ""
			self.text_buffer += boton.get_text()
			print self.text_buffer
			return
		elif boton in self.board_matematicas.botones:
			if self.text_buffer == " ":
				self.text_buffer = ""
			self.text_buffer += boton.get_text()
			print self.text_buffer
			return
		elif boton in self.board_especiales.botones:
			if self.text_buffer == " ":
				self.text_buffer = ""
			self.text_buffer += boton.get_text()
			print self.text_buffer
			return


	def Describe(self):
		''' Describe la Estructura de Este Control. '''
		estructura =  '''
		Estructura JAMBoard:

			JAMObject:
				Frame
				Text_Buffer
				JAMBoardTypes simbolos
				JAMBoardTypes letras
				JAMBoardTypes numeros
				JAMBoardTypes matematicas
				JAMBoardTypes otros
				JAMBoardTypes especiales'''

		print estructura, "\n"
		print "Ejemplo, Configuración actual:\n"
		print "\t", self.JAMObjects.keys(), "\n"
		for k in self.JAMObjects.items():
			print k, "\n"

# ----- FIN DE CLASE JAMBoard - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
class Ejemplo(object):
	def __init__(self):
		self.ventana = None
		self.reloj = None
		self.nivel = "menu_0"

		self.fondo = None
		self.widgets = None

		self.resolucion = (1200,800)

		self.setup()
		self.Run()

	def setup(self):
		pygame.init()
		pygame.display.set_mode(self.resolucion , 0, 0)
		pygame.display.set_caption("Ejemplo")

		self.fondo = self.get_Fondo()

		self.widgets = JAMBoard()
		self.widgets.set_posicion(punto=(25,25))
			
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
				# Activa la siguiente línea para provocar cambios en el tipo de botones en JAMBoard
				contador= self.ejemplo_cambia_tipo_de_botones()
				# Activa la siguiente línea para provocar cambios de colores en JAMBoard
				contador= self.ejemplo_cambia_colors_Board()
				# Activa la siguiente línea para provocar cambios de texto en Botones
				contador= self.ejemplo_cambia_texto_en_JAMBoard()
				# Activa la siguiente línea para provocar cambios de posicion en JAMBoard
				contador= self.ejemplo_cambia_posicion_de_JAMBoard()
				# Activa la siguiente línea para desconectar el sonido select sobre los botones
				#self.widgets.set_reconnect_sound(None)
				# Activa la siguiente línea para ver el contenido del buffer de JAMBoard
				#print self.widgets.text_buffer
				# Activa la siguiente línea para cambiar los estilos de colores en JAMBoard
				contador= self.ejemplo_cambia_estilos()
				contador= 0

			self.widgets.update()
			self.handle_event()
			pygame.event.clear()
			cambios.extend ( self.widgets.draw(self.ventana) )
			pygame.display.update(cambios)
			contador += 1

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

	def ejemplo_cambia_texto_en_JAMBoard(self):
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
	
	def ejemplo_cambia_posicion_de_JAMBoard(self):
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
