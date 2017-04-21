#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 18/04/2011 - CeibalJAM! - Uruguay
#   JAMEntryText.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys
from pygame.locals import *
gc.enable()
pygame.font.init()

import JAMGlobals as VG
from JAMLabel import JAMLabel

class JAMEntryText(pygame.sprite.OrderedUpdates):
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.buffertext= ""

		# teclas
		self.handlekey= None

		#self.sensitive= False

		self.texto= {"fondo":VG.get_blanco(), "tipo":pygame.font.get_default_font(), "tamanio": 20, "color":VG.get_negro()}

		self.separador= 5
		self.posicion= (0,0)

		self.label_buffer= None
		self.label_promp = None
		self.frame= pygame.sprite.Sprite()

		self.JAMObjects= {"base":self.frame, "etiqueta_buffer":self.label_buffer, "promp":self.label_promp,
			"buffertext": self.buffertext, "handle_key":self.handlekey}

		self.Reconstruye_JAMEntryText(["todo"])

	# ------------- GETS ------------------------
	def get_tamanio(self):
		return (self.frame.rect.w, self.frame.rect.h)

	# ------------ SETEOS -----------------------
	#def set_mouse_sensitive(self, valor):
	#	self.sensitive= bool(valor)

	def set_handle_key(self, valor):
		''' Habilita y desabilita la detección de eventos de tecla.
		Por defecto no lo hace ya que JAMEntryText está pensado como objeto parte de JAMBoardEntryText. '''
		if bool(valor) == True:
			self.handlekey= JAMHandleKeyEvent(self)
		else:
			self.handlekey= None

	def set_callback_enter(self, callback=None):
		''' Setea una función para ejecutarse cuando el usuario presione enter.
		La función debe recibir un string para el buffer de texto de JAMEntryText'''
		if self.handlekey:
			self.handlekey.callback_enter= callback

	def set_buffer(self, texto):
		''' Setea el buffer de texto de JAMEntryText. '''
		if texto != self.buffertext:
			self.buffertext = texto
			self.label_buffer.set_text(tipo=self.texto["tipo"], tamanio=self.texto["tamanio"], color=self.texto["color"], texto=self.buffertext)
			self.Reconstruye_JAMEntryText(["buffer"])

	def set_entry(self, tipo_letra=None, tamanio_letra=None, color_texto=None, color_fondo=None):
		''' Setea colores, tamaño y tipo de letra. '''
		cambios= False
		if tipo_letra and tipo_letra != self.texto["tipo"]:
			self.texto["tipo"]= tipo_letra
			cambios= True
		if tamanio_letra and tamanio_letra != self.texto["tamanio"]:
			self.texto["tamanio"]= tamanio_letra
			cambios= True
		if color_texto and color_texto != self.texto["color"]:
			self.texto["color"]= color_texto
			cambios= True
		if color_fondo and color_fondo != self.texto["fondo"]:
			self.texto["fondo"]= color_fondo
			cambios= True
		if cambios:
			if self.texto["tipo"] and self.texto["tamanio"] and self.texto["color"] and self.texto["fondo"]:
				self.label_buffer.set_text(tipo=self.texto["tipo"], tamanio=self.texto["tamanio"], color=self.texto["color"], texto=self.buffertext)
				self.Reconstruye_JAMEntryText(["colores"])

	def set_posicion(self, punto=(0,0)):
		''' Setea la posición de JAMEntryText. '''
		self.posicion= punto
		self.frame.rect.x, self.frame.rect.y= self.posicion
		x, y= (self.frame.rect.x + self.separador, self.frame.rect.y + self.separador)
		self.label_buffer.set_posicion(punto=(x, y))
		x+= self.label_buffer.rect.w
		self.label_promp.set_posicion(punto=(x, y))

	def set_center(self, punto= None):
		''' Centra JAMEntryText en el punto indicado. '''
		w,h= (0,0)
		if not punto or type(punto) != tuple or type(punto[0]) != int or type(punto[1]) != int:
			w,h= (pygame.display.Info().current_w, pygame.display.Info().current_h)
			posicion= (w/2-self.frame.rect.w/2, h/2-self.frame.rect.h/2)
			self.set_posicion(punto=posicion)
		elif type(punto) == tuple and type(punto[0]) == int and type(punto[1]) == int:
			posicion= (punto[0]-self.frame.rect.w/2, punto[1]-self.frame.rect.h/2)
			self.set_posicion(punto=posicion)

	# ------------ CONSTRUCCIÓN -----------------------
	def Reconstruye_JAMEntryText(self, cambios):
		if "todo" in cambios:
			self.label_buffer= JAMLabel(self.buffertext)
			self.label_promp = Promp(self)
			self.frame.image= self.get_base()
			self.frame.rect= self.frame.image.get_rect()
			self.add(self.frame)
			self.add(self.label_buffer)
			self.add(self.label_promp)
			self.set_posicion(punto=self.posicion)

		if "colores" in cambios:
			self.label_promp.Reconstruye_Promp(["todo"])
			self.frame.image= self.get_base()
			self.frame.rect= self.frame.image.get_rect()
			self.set_posicion(punto=self.posicion)

		if "buffer" in cambios:
			self.frame.image= self.get_base()
			self.frame.rect= self.frame.image.get_rect()
			self.set_posicion(punto=self.posicion)

	def get_base(self):
		''' Construye el sprite base. '''
		(a,b,c,d)= self.label_buffer.rect
		(aa,bb,cc,dd)= self.label_promp.rect

		ancho= c + cc + self.separador*2
		alto= 0
		if d > dd:
			alto= d
		else:
			alto= dd
		alto+= self.separador*2

		frame1= VG.get_Rectangulo(self.texto["fondo"], (ancho,alto))
		return frame1

	def Describe(self):
		''' Describe la Estructura de Este Control. '''
		estructura = '''
		Estructura JAMEntryText:

			JAMObject:
				frame
				etiqueta_buffer
				promp
				buffertext
				handle_key

		Detalle Estructural:
				frame: es una imagen construida en tiempo de ejecución sobre la cual se pegan las imágenes de las etiquetas
				etiqueta_buffer: JAMLabel con el texto que el usuario va escribiendo
				promp: Imagen que representa al promp con su efecto intermitente
				buffertext: El texto que el usuario va ingresando
				handle_key: Detector de eventos de teclado '''

		print estructura, "\n"
		print "Ejemplo, Configuración actual:\n"
		print "\t", self.JAMObjects.keys(), "\n"
		for k in self.JAMObjects.items():
			print k, "\n"

class Promp(pygame.sprite.Sprite):
	def __init__(self, entry):
		pygame.sprite.Sprite.__init__(self)
		''' Es el promp. '''
		self.entry= entry
		self.velocidad= 15
		self.contador= 0
		self.image= None
		self.rect= None
		self.imagen1= None
		self.imagen2= None

		self.Reconstruye_Promp(["todo"])
	
	def Reconstruye_Promp(self, cambios):
		''' Reconstruye las imágenes para efecto Titilar. '''
		if "todo" in cambios:
			self.set_imagenes_promp()
			self.image= self.imagen1
			self.rect= self.image.get_rect()

	def set_posicion(self, punto=(0,0)):
		''' Reposiciona el sprite. '''
		self.rect.x= punto[0]
		self.rect.y= punto[1]

	def set_imagenes_promp(self):
		''' Construye las imagenes del promp. '''
		self.imagen1= self.get_promp(self.entry.texto["color"])
		self.imagen2= self.get_promp(self.entry.texto["fondo"])

	def get_promp(self, color):
		''' Devuelve una Superficie con la Imagen del Texto. '''
		fuente = pygame.font.Font(pygame.font.match_font(self.entry.texto["tipo"], True, False), self.entry.texto["tamanio"])
		string_to_render = unicode( str("|".decode("utf-8")) )
		imagen_fuente = fuente.render(string_to_render, 1, (color))
		return imagen_fuente

	def update(self):
		''' Efecto Titilar. '''
		if self.entry.handlekey:
			if self.contador == self.velocidad:
				if self.image == self.imagen1:
					self.image= self.imagen2
				else:
					self.image= self.imagen1
				self.contador= 0
			else:
				self.contador += 1
		else:
			if self.image == self.imagen1:
				self.image = self.imagen2

		# teclas
		if self.entry.handlekey: self.entry.handlekey.handle()

class JAMHandleKeyEvent():
	def __init__(self, objeto_destino):
		''' Detecta eventos de teclado.'''
		self.letras= VG.get_letras_down()
		self.numeros= VG.get_numeros()

		self.objeto_destino= objeto_destino
		self.text_buffer= []
		self.callback_enter= None
	
	def handle(self):
		''' Trata los eventos del teclado. '''
		eventos= pygame.event.get()
		for event in eventos:
			if event.type == pygame.KEYDOWN:
				letra= pygame.key.name(event.key)
				self.gestiona_event(letra)
		
		for event in eventos:
		# Republica los Eventos. Porque se supone que hay un handle general para los eventos del programa mayor.
			pygame.event.post(event)

	def gestiona_event(self, texto):
		''' Cuando el usuario presiona una espacio, borrar, enter o tilde. '''
		if texto in self.letras:
			self.text_buffer.append( texto )
			return self.set_bufferentry()

		elif texto in self.numeros:
			self.text_buffer.append( texto )
			return self.set_bufferentry()

		elif texto== "space":
		# agrega un espacio en el buffer
			self.text_buffer.append( " " )
			return self.set_bufferentry()

		elif texto== "backspace":
		# Borra el último caracter ingresado
			if len(self.text_buffer) <= 1:
				self.text_buffer= [ " " ]
			else:
				self.text_buffer= self.text_buffer[0:-1]
			return self.set_bufferentry()

		elif texto== "return":
		# Llama a la función conectada al click del botón enter, pasandole como parámetro el texto en el buffer
			if self.callback_enter:
				buf= ""
				try:
					primercaracter= self.text_buffer[0]
					if primercaracter != " ":
						buf= primercaracter
					else:
						buf= ""
				
					for x in self.text_buffer[1:]:				
						buf += x
				except:
					return
				if buf:
					return self.callback_enter(buf)

	def set_bufferentry(self):
		''' Convierte el buffer en cadena de texto y lo devuelve a la función set_buffer del objeto destino. '''
		buf= ""
		for x in self.text_buffer:
			buf += x
		self.objeto_destino.set_buffer(buf)

'''
# Ejemplos para tratar los códigos de teclas posteriormente
	def handle_key_enter(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				letra= pygame.key.name(event.key)
				print letra

teclas = pygame.key.get_pressed()
	print teclas.index(1)

All the keyboard event.key constants:

Letters:
    K_a ... K_z

Numbers:
    K_0  ... K_9

Control:
    K_TAB
    K_RETURN
    K_ESCAPE
    K_SCROLLOCK
    K_SYSREQ
    K_BREAK
    K_DELETE
    K_BACKSPACE
    K_CAPSLOCK
    K_CLEAR
    K_NUMLOCK

Punctuation:
    K_SPACE
    K_PERIOD
    K_COMMA
    K_QUESTION
    K_AMPERSAND
    K_ASTERISK
    K_AT
    K_CARET
    K_BACKQUOTE
    K_DOLLAR
    K_EQUALS
    K_EURO
    K_EXCLAIM
    K_SLASH,      K_BACKSLASH
    K_COLON,      K_SEMICOLON
    K_QUOTE,      K_QUOTEDBL
    K_MINUS,      K_PLUS
    K_GREATER,    K_LESS

Brackets:
    K_RIGHTBRACKET,  K_LEFTBRACKET
    K_RIGHTPAREN,    K_LEFTPAREN

F-Keys:
    K_F1 ... K_F15

Edit keys:
    K_HELP
    K_HOME
    K_END
    K_INSERT
    K_PRINT
    K_PAGEUP, K_PAGEDOWN
    K_FIRST,  K_LAST

Keypad:
    K_KP0 ... K_KP9
    K_KP_DIVIDE
    K_KP_ENTER
    K_KP_EQUALS
    K_KP_MINUS
    K_KP_MULTIPLY
    K_KP_PERIOD
    K_KP_PLUS

SHF,CTL,ALT etc:
    K_LALT,   K_RALT
    K_LCTRL,  K_RCTRL
    K_LSUPER, K_RSUPER
    K_LSHIFT, K_RSHIFT
    K_RMETA,  K_LMETA

Arrows:
    K_LEFT
    K_UP
    K_RIGHT
    K_DOWN

Other:
    K_MENU
    K_MODE
    K_PAUSE
    K_POWER
    K_UNDERSCORE
    K_HASH

    K_UNKNOWN '''

# ----- FIN DE CLASE JAMEntryText - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
class Ejemplo(object):
	def __init__(self):
		self.ventana = None
		self.reloj = None
		self.nivel = "menu_0"

		self.fondo = None
		self.widgets = None

		self.resolucion = (400,250)

		self.setup()
		self.Run()

	def setup(self):
		pygame.init()
		pygame.display.set_mode(self.resolucion , 0, 0)
		pygame.display.set_caption("Ejemplo")

		self.fondo = self.get_Fondo()

		self.widgets = JAMEntryText()
		self.widgets.set_handle_key(True)
		#self.widgets.set_mouse_sensitive(True)
		self.widgets.set_callback_enter(self.print_buffer)

		self.ventana = pygame.display.get_surface()
		self.reloj = pygame.time.Clock()

		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN,
					USEREVENT, QUIT, ACTIVEEVENT])
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN, KEYUP, VIDEORESIZE, VIDEOEXPOSE])
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
			if contador == 15:
				# Activa la siguiente línea para provocar cambios de texto en JAMEntryText
				#contador= self.ejemplo_cambia_texto_en_buffer()
				# Activa la siguiente línea para provocar cambios de color en JAMEntryText
				#contador= self.ejemplo_cambia_colors()
				# Activa la siguiente línea para provocar cambios de Posición en JAMEntryText
				#contador= self.ejemplo_cambia_posicion()
				pass

			self.widgets.update()
			self.handle_event()
			pygame.event.clear()
			cambios.extend ( self.widgets.draw(self.ventana) )
			pygame.display.update(cambios)
			contador += 1

	def ejemplo_cambia_posicion(self):
		import random
		valores= [100,205,130,140,150,180]
		x, y= (random.choice(valores), random.choice(valores))
		self.widgets.set_center(punto= (x,y))
		return 0

	def ejemplo_cambia_texto_en_buffer(self):
		texto= "El usuario ingresa texto y el mismo aparece aqui . . ."
		x= len(self.widgets.buffertext)
		if len(texto) > x:
			self.widgets.set_buffer(str(texto[0:x+1]))
		else:
			self.widgets.set_buffer("")
		return 0

	def ejemplo_cambia_colors(self):
		import random
		colores= [(128,128,128,255), (255,100,100,255), (255,255,100,255), (255,0,0,255)]
		color=random.choice(colores)
		self.widgets.set_entry(tipo_letra=None, tamanio_letra=None, color_texto=color, color_fondo=None)
		return 0

	def get_Fondo(self):
		superficie = pygame.Surface( self.resolucion, flags=HWSURFACE )
		superficie.fill((128,128,128,255))
		return superficie

	def handle_event(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				teclas = pygame.key.get_pressed()
				if teclas[pygame.K_ESCAPE]:
					self.salir()
		pygame.event.clear()

	def print_buffer(self, buffertext):
		print self.widgets.buffertext
		print buffertext

	def salir(self):
		print "\n"
		self.widgets.Describe()
		pygame.quit()
		sys.exit()



if __name__ == "__main__":
	Ejemplo()
