#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 05/06/2011 - CeibalJAM! - Uruguay
#   JAMBook.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, sys, gc, subprocess
from pygame.locals import *

gc.enable()

from JAMLabel import JAMLabel
from JAMButton import JAMButton

import JAMGlobals as VG

class JAMBook(pygame.sprite.OrderedUpdates):
	''' Libreta para lectura con los botones de navegación y motor de voz. '''
	def __init__(self, lectura):
		pygame.sprite.OrderedUpdates.__init__(self)

		self.tamanio_hoja= (452,700) #(592,840)
		self.margen= 0
		self.lectura= lectura

		self.hoja= None
		self.rectangulo_texto= (0,0,0,0)
		self.texto_sprite= None
		self.botones= []

		self.posicion= (0,0)

		self.Reconstruye(["todo"])

	def Reconstruye(self, cambios):
		''' Reconstruye JAMBook según cambios. '''
		if "todo" in cambios:
			self.hoja= pygame.sprite.Sprite()
			self.hoja.image, self.margen= VG.get_hoja(self.tamanio_hoja)
			self.hoja.rect= self.hoja.image.get_rect()

			self.rectangulo_texto= Rectangulo_Texto(self, (0,0,self.hoja.rect[2]-self.margen*1.5,self.hoja.rect[3]-self.margen*2))
			self.texto_sprite= Texto_sprite(self)
			self.botones= self.get_botones()

			self.add(self.hoja)
			self.add(self.texto_sprite)
			self.add(self.botones)

			self.set_posicion(punto=self.posicion)

	# ----------------- SETEOS -----------------------------
	def set_posicion(self, punto=(0,0)):
		''' Setea la posicion de todos los sprites miembros. '''
		if not type(punto)== tuple or not len(punto)==2 or not type(punto[0])== int or not type(punto[0])== int: return
		self.posicion= punto
		self.hoja.rect.x, self.hoja.rect.y= self.posicion
		self.rectangulo_texto.set_posicion(punto=(self.hoja.rect.x+self.margen,self.hoja.rect.y+self.margen/2))

		x,y,w,h= self.hoja.rect # posicionar los botones
		self.botones[0].set_posicion(punto=(x, y+h-self.botones[1].get_tamanio()[1]))
		self.botones[1].set_posicion(punto=(x+w-self.botones[1].get_tamanio()[0], y+h-self.botones[1].get_tamanio()[1]))
		self.botones[2].set_posicion(punto=(x+w-self.botones[2].get_tamanio()[0], y))

	def set_callback_cerrar(self, callback):
		''' Setea una función para click sobre el boton cerrar. '''
		self.botones[2].connect(callback=callback)

	# ------------------ Construccion ----------------------------
	def get_botones(self):
		''' Construye los botones para cambiar de página y cerrar el libro. '''
		uno, dos, tres, cuatro= VG.get_boton_imagenes()
		boton_previous= JAMButton("", uno)
		boton_next= JAMButton("", dos)
		boton_salir= JAMButton("", cuatro)
		boton_previous.set_imagen(origen=uno , tamanio=(10,10))
		boton_previous.set_tamanios(tamanio=(0,0),grosorbor=1, espesor=1)
		boton_next.set_imagen(origen=dos , tamanio=(10,10))
		boton_next.set_tamanios(tamanio=(0,0),grosorbor=1, espesor=1)
		boton_salir.set_imagen(origen=cuatro , tamanio=(10,10))
		boton_salir.set_tamanios(tamanio=(0,0),grosorbor=1, espesor=1)
		boton_previous.connect(callback=self.texto_sprite.previous)
		boton_next.connect(callback=self.texto_sprite.next)
		return [boton_previous, boton_next, boton_salir]

class Rectangulo_Texto(pygame.rect.Rect):
	''' El rectángulo donde debe dibujarse el texto. '''
	def __init__(self, book, rectangulo):
		self.book= book
		pygame.rect.Rect.__init__(self, rectangulo)

	def set_posicion(self, punto=(0,0)):
		self.x= punto[0]
		self.y= punto[1]
		self.book.texto_sprite.set_posicion()

class Texto_sprite(pygame.sprite.OrderedUpdates):
	''' Grupo de JAMLabels por páginas con la lectura del libro. '''
	def __init__(self, book):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.book= book
		self.paginas= []
		self.set_leccion()

	def previous(self, button):
		''' Muestra la página anterior. '''
		indice= self.paginas.index(self.sprites())
		if indice > 0:
			indice -= 1
			for sprites in self.sprites():
				self.book.remove(sprites)
			self.empty()
			self.add(self.paginas[indice])
			self.book.add(self)

	def next(self,button):
		''' Muestra la página siguiente. '''
		indice= self.paginas.index(self.sprites())
		if indice < len(self.paginas)-1:
			indice += 1
			for sprites in self.sprites():
				self.book.remove(sprites)
			self.empty()
			self.add(self.paginas[indice])
			self.book.add(self)

	def set_posicion(self):
		''' Setea la posición del texto. '''
		x,y,w,h= self.book.rectangulo_texto
		for pagina in self.paginas:
			for renglon in pagina:
				renglon.set_posicion(punto=(x,y))
				y+= renglon.get_tamanio()[1]
			x,y,w,h= self.book.rectangulo_texto

	def set_leccion(self):
		''' Setea el texto en el libro. '''
		renglones= self.book.lectura.split("\n")
		label_renglones= []
		for renglon in renglones:
			label= JAMLabel(renglon)
			label.set_text(tamanio=30, color=VG.get_negro())
			label_renglones.append(label)
		self.set_posicion_renglones(label_renglones)

	def set_posicion_renglones(self, label_renglones):
		''' Posiciona los renglones, generando páginas. '''
		x,y,w,h= self.book.rectangulo_texto
		pagina= []
		for renglon in label_renglones:
			renglon.set_posicion(punto=(x,y))
			y+= renglon.get_tamanio()[1]
			pagina.append(renglon)
			if not self.book.rectangulo_texto.collidepoint(x, y):
				self.paginas.append(pagina)
				x,y,w,h= self.book.rectangulo_texto
				pagina= []

		if len(pagina)>0: self.paginas.append(pagina)
		self.set_pagina_actual()

	def set_pagina_actual(self):
		''' Muestra la página 1. '''
		self.empty()
		self.add(self.paginas[0])



# ----- FIN DE CLASE JAMBook - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
class Ejemplo(object):
	def __init__(self):

		# Variables obligatorias en tu juego para poder utilizar JAMatrix.
		self.resolucion = (1200,800)
		self.ventana = None
		self.name= "Ejemplo JAMBook"
		self.estado = False

		# Variables del juego
		self.reloj = None
		self.fondo = None

		self.jambook= None

		self.load() # crea la ventana principal

		self.estado= "menu_0"
		self.run_menu_0()

	def run_menu_0(self):
		''' Tu juego corriendo. '''
		self.ventana.blit(self.fondo, (0,0))

		self.jambook.draw(self.ventana)

		pygame.display.update()

		contador = 0
		while self.estado == "menu_0":
			self.reloj.tick(35)
	
			cambios=[]
			self.jambook.clear(self.ventana, self.fondo)

			self.jambook.update()

			self.handle_event()
			pygame.event.clear()

			if contador == 150:
				self.jambook.set_posicion(punto=(50,50))
			if contador == 200:
				self.jambook.set_posicion(punto=(10,10))
				contador = 0
			cambios.extend ( self.jambook.draw(self.ventana) )

			pygame.display.update(cambios)
			contador += 1

	def load(self):
		''' Creando y seteando todos los objetos de tu juego. '''
		pygame.init()
		pygame.display.set_mode(self.resolucion , 0, 0)
		self.ventana = pygame.display.get_surface()
		self.fondo = self.get_Fondo()
		self.reloj = pygame.time.Clock()
		
		self.jambook= JAMBook(TEXTO)
		self.jambook.set_callback_cerrar(self.salir)

		pygame.display.set_caption("Ejemplo de JAMBook")
		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN,
					KEYUP, USEREVENT, QUIT, ACTIVEEVENT])
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN, VIDEORESIZE, VIDEOEXPOSE])
		pygame.mouse.set_visible(True)
		self.estado= True # Todo se ha cargado y seteado, listo para correr el juego.

	def get_Fondo(self):
		superficie = pygame.Surface( self.resolucion, flags=HWSURFACE )
		superficie.fill(VG.get_gris1())
		return superficie

	def handle_event(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				self.salir(None)
		pygame.event.clear()

	def salir(self, button):
		pygame.quit()
		sys.exit()

TEXTO= '''
El loro pelado

Había una vez una bandada de loros
que vivía en el monte.

De mañana temprano iban a comer
choclos a la chacra, y de tarde
comían naranjas.

Hacían gran barullo con sus gritos,
y tenían siempre un loro de
centinela en los árboles más altos,
para ver si venía alguien.

Los loros son tan dañinos como la
langosta, porque abren los choclos
para picotearlos, los cuales,
después se pudren con la Lluvia.
Y como al mismo tiempo los loros
son ricos para comerlos guisados,
los peones los cazaban a tiros.

Un día un hombre bajó de un tiro a
un loro centinela, el que cayó
herido y peleó un buen rato antes
de dejarse agarrar. El peón lo
Llevó a la casa, para los hijos del
patrón; los chicos lo curaron porque
no tenía más que un ala rota.
El loro se curó muy bien, y se
amansó completamente.
Se Llamaba Pedrito. Aprendió a dar
la pata; le gustaba estar en el
hombro de las personas y les hacía
cosquillas en la oreja. '''

if __name__ == "__main__":
	Ejemplo()
