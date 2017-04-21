#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 29/05/2011 - CeibalJAM! - Uruguay
#   JAMDragAndDrop.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys
from pygame.locals import *
gc.enable()

import JAMGlobals as VG

class JAMDragAndDrop():
	''' Recibe un grupo de Sprites y hace drag and drop con el grupo entero. '''
	def __init__(self, objetivo):
		self.objetivo= objetivo
		self.rectangulo= (self.objetivo.posicion, self.busca_tamanio())
		self.select= False
		self.callback_drop= None
		self.callback_drag= None

	def busca_tamanio(self):
		''' Calcula el tamaño para un rectángulo que contenga a todos los rectángulos del objetivo. '''
		inicio= self.objetivo.posicion
		ancho= 0
		alto= 0
		for sprite in self.objetivo.sprites():
			rectangulo= sprite.rect
			x,y,w,h= rectangulo
			if w > ancho: ancho= w
			if h > alto: alto= h
		return (ancho,alto)

	# ------------------ Sobrecargas para pygame.sprite.OrderedUpdates ---------------------
	def draw(self, uno):
		return self.objetivo.draw(uno)
	def clear(self, uno, dos):
		return self.objetivo.clear(uno, dos)
	def update(self):
		''' Verifica cuando se selecciona o se suelta el objeto. '''
		self.rectangulo= pygame.Rect(self.objetivo.posicion, self.busca_tamanio())
		posicion = pygame.mouse.get_pos()
		if self.rectangulo.collidepoint(posicion):
			if pygame.event.get(pygame.MOUSEBUTTONDOWN):
				if self.select:
					self.select= False
					if self.callback_drop:
						return self.callback_drop(self, self.objetivo)
				else: 
					self.select= True
					if self.callback_drag:
						return self.callback_drag(self, self.objetivo)

		x,y,w,h= self.rectangulo
		xx,yy= (posicion[0]- w/2, posicion[1]- h/2)
		if self.select:
			self.objetivo.set_posicion(punto= (xx,yy))

	# ------------------ SETEOS -------------------------------------------------
	def connect_drop(self, callback):
		''' Conecta el evento "soltar objetivo" a una función. La función a la que se llama debe tener 2 parámetros para
		recibir self y self.objetivo, de esa manera se sabe cual es el DrangDrop y cual el grupo afectado por él.'''
		self.callback_drop= callback
		
	def connect_drag(self, callback):
		''' Conecta el evento "soltar objetivo" a una función. La función a la que se llama debe tener 2 parámetros para
		recibir self y self.objetivo, de esa manera se sabe cual es el DrangDrop y cual el grupo afectado por él.'''
		self.callback_drag= callback

# ----- FIN DE CLASE JAMDragAndDrop - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
class Ejemplo(object):
	def __init__(self):
		self.ventana = None
		self.reloj = None
		self.nivel = "menu_0"

		self.fondo = None
		self.widgets = None

		self.resolucion = (1024,758)

		self.setup()
		self.Run()

	def setup(self):
		pygame.init()
		pygame.display.set_mode(self.resolucion , 0, 0)
		pygame.display.set_caption("Ejemplo")
		self.fondo = self.get_Fondo()

		from JAMCalendar import JAMCalendar
		from JAMClock import JAMClock
		self.calendario= JAMCalendar() # Mi grupo de Sprites.
		self.draganddrop= JAMDragAndDrop(self.calendario) # JAMDragAndDrop con el grupo que se va a arrastrar. 
		self.draganddrop.connect_drop(self.reposiciona) # Callback para evento "soltar objetivo".
		self.draganddrop.connect_drag(self.imprime_hola) # Callback para evento "tomar objetivo".

		self.widgets= self.draganddrop # Lo que se dibuja y actualiza es ahora JAMDragAndDrop

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

		self.contador = 0
		mes= 0
		while self.nivel == "menu_0":
			self.reloj.tick(35)
	
			cambios=[]
			self.widgets.clear(self.ventana, self.fondo)

			self.widgets.update()
			self.handle_event()
			pygame.event.clear()
			cambios.extend ( self.widgets.draw(self.ventana) )
			pygame.display.update(cambios)
			if self.contador > 0:
				self.contador += 1
				print "%s para reactivar JAMDragAndDrop sobre el Calendario" % (150 - self.contador)
			if self.contador== 150:
				print "JAMDragAndDrop reactivado"
				self.widgets= self.draganddrop  # Lo que se dibuja y actualiza es ahora JAMDragAndDrop
				self.contador = 0

	def imprime_hola(self, drag, group):
		''' Callback para tomar objetivo. '''
		print "Objeto seleccionado:", group, "en:", drag
	def reposiciona(self, drag, group):
		''' Callback para soltar objetivo.
		Cuando haces click sobre el grupo lo seleccionas y lo mueves, cuando vuelves a hacer click lo sueltas y
		en este ejemplo, se intercambia JAMDragAndDrop por el grupo que contenía para de esa manera desabilitar el DragAndDrop y
		habilitar los eventos sobre el grupo que contenía.'''
		group.set_posicion(punto= (0,0))
		self.widgets= group#self.calendario  # Lo que se dibuja y actualiza es ahora Mi grupo de Sprites.
		self.contador= 1

	def get_Fondo(self):
		superficie = pygame.Surface( self.resolucion, flags=HWSURFACE )
		superficie.fill((0,0,0,255))
		return superficie

	def handle_event(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				teclas = pygame.key.get_pressed()
				if teclas[pygame.K_ESCAPE]:
					self.salir()
		pygame.event.clear()

	def salir(self):
		pygame.quit()
		sys.exit()

if __name__ == "__main__":
	Ejemplo()
