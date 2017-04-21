#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 31/05/2011 - CeibalJAM! - Uruguay
#   JAMFire.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys, os
from pygame.locals import *
gc.enable()

import JAMGlobals as VG

class JAMFire(pygame.sprite.OrderedUpdates):
	''' Efecto Fuego. '''
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.posicion= (0,0)
		self.latencia= 6
		self.disminucion= 5
		self.deformacion= (0,0)

		self.fuego= Fuego(self) 
		self.add(self.fuego)

	def set_posicion(self, punto= (0,0)):
		''' Setea la posición desde donde se dibujará el efecto, es decir que punto es la base del fuego.'''
		if type(punto)== tuple:
			if len(punto)== 2 and type(punto[0])==int and type(punto[1]):
				self.fuego.rect.x= punto[0]-self.fuego.rect.w/2
				self.fuego.rect.y= punto[1]-self.fuego.rect.h
				self.posicion= punto

	def set_deforma_fire(self, valor):
		''' Divide por valor el tamaño del fuego. '''
		if type(valor)== tuple:
			if len(valor)==2 and type(valor[0])== int and type(valor[1])== int:
				self.deformacion= valor
				self.fuego.deforma_imagenes()
				self.set_posicion(punto= self.posicion)

	def set_disminuye_fire(self, valor):
		''' Divide por valor el tamaño del fuego. '''
		if type(valor)== int and valor > 0:
			self.disminucion= valor
			self.fuego.load_imagenes()
			self.set_posicion(punto= self.posicion)

	def set_latencia(self, latencia):
		''' Setea la velocidad de secuenciación de imágenes para el fuego. '''
		if type(latencia)== int: self.latencia= latencia

	def get_tamanio(self):
		''' Devuelve el tamanio actual del fuego. '''
		return (self.fuego.rect.w, self.fuego.rect.h)

class Fuego(pygame.sprite.Sprite):
	''' El Sprite para el efecto. '''
	def __init__(self, fire):
		pygame.sprite.Sprite.__init__(self)
		self.fire= fire
		self.imagenes= []
		self.indice_actual= 0
		self.image= None
		self.rect= None
		self.contador= 0
		self.load_imagenes()

	def load_imagenes(self):
		''' carga las imagenes ajustando su tamaño según el indice de disminución especificado. '''
		self.imagenes= []
		for imagen in VG.get_fire():
			tam= imagen.get_size()
			im= pygame.transform.scale(imagen, (tam[0]/self.fire.disminucion,tam[1]/self.fire.disminucion)) 
			self.imagenes.append(im)
		self.indice_actual= 0
		self.image= self.imagenes[self.indice_actual]
		self.rect= self.image.get_rect()
		self.contador= 0

	def deforma_imagenes(self):
		''' carga las imagenes ajustando su tamaño según la información en self.fire.deformacion. '''
		self.imagenes= []
		for imagen in VG.get_fire():
			im= pygame.transform.scale(imagen, self.fire.deformacion) 
			self.imagenes.append(im)
		self.indice_actual= 0
		self.image= self.imagenes[self.indice_actual]
		self.rect= self.image.get_rect()
		self.contador= 0
			
	def update(self):
		''' Secuencia las imágenes. '''
		if self.contador == self.fire.latencia:
			try:
				self.indice_actual += 1 
				self.image= self.imagenes[self.indice_actual]
			except:
				self.indice_actual = 0
				self.image= self.imagenes[self.indice_actual]
			self.contador = 0
		self.contador += 1

# ----- FIN DE CLASE JAMFire - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
class Ejemplo(object):
	def __init__(self):
		self.ventana = None
		self.reloj = None
		self.nivel = "menu_0"

		self.fondo = None
		self.widgets = None

		self.resolucion = (800,600)

		self.setup()
		self.Run()

	def setup(self):
		pygame.init()
		pygame.display.set_mode(self.resolucion , 0, 0)
		pygame.display.set_caption("Ejemplo de Efecto JAMFire")
		self.fondo = self.get_Fondo()

		#from JAMDragAndDrop import JAMDragAndDrop
		#fire= JAMFire()
		#self.widgets= JAMDragAndDrop(fire)
		self.widgets = JAMFire()
		self.widgets.set_posicion(punto= (400,300))
		#self.widgets.set_disminuye_fire(1)
		#self.widgets.set_deforma_fire((50,100))
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

		contador= 0
		while self.nivel == "menu_0":
			self.reloj.tick(35)
	
			cambios=[]
			self.widgets.clear(self.ventana, self.fondo)

			'''
			if contador==100:
				self.widgets.set_posicion(punto= (200,300))
				self.widgets.set_disminuye_fire(2)
			if contador==200:
				self.widgets.set_posicion(punto= (400,300))
				self.widgets.set_disminuye_fire(3)
			if contador==300:
				self.widgets.set_posicion(punto= (200,300))
				self.widgets.set_disminuye_fire(4)
			if contador==400:
				self.widgets.set_posicion(punto= (400,300))
				self.widgets.set_disminuye_fire(5)
			if contador==500:
				self.widgets.set_posicion(punto= (200,300))
				self.widgets.set_disminuye_fire(6)
			if contador==600:
				self.widgets.set_posicion(punto= (400,300))
				self.widgets.set_disminuye_fire(7)
			if contador==700:
				self.widgets.set_posicion(punto= (200,300))
				self.widgets.set_disminuye_fire(8)
			if contador==800:
				self.widgets.set_posicion(punto= (400,300))
				self.widgets.set_disminuye_fire(9)
			if contador==900:
				self.widgets.set_posicion(punto= (200,300))
				self.widgets.set_disminuye_fire(1)
			if contador==1000:
				self.widgets.set_posicion(punto= (400,300))
				self.widgets.set_disminuye_fire(10)
				contador= 0
			contador += 1'''

			self.widgets.update()
			self.handle_event()
			pygame.event.clear()
			cambios.extend ( self.widgets.draw(self.ventana) )
			pygame.display.update(cambios)

	def get_Fondo(self):
		superficie = pygame.Surface( self.resolucion, flags=HWSURFACE )
		superficie.fill(VG.get_gris1())
		#superficie.fill(VG.get_negro())
		#superficie.fill(VG.get_blanco())
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
