#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 31/05/2011 - CeibalJAM! - Uruguay
#   JAMatrix.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame
from pygame.locals import *

import gc
gc.enable()

import sys, os, random, threading

from JAMLabel import JAMLabel
from JAMClock import JAMClock
from JAMCalendar import JAMCalendar

import JAMGlobals as VG

class JAMatrix():
	''' Main de JAMatrix. '''
	def __init__(self, juego, ventana, resolucion):
		self.juego= juego		# el juego base
		self.ventana= ventana		# la ventana pygame
		self.resolucion= resolucion	# la resolucion de la pantalla

		self.widgets= None		# grupo de terrones
		self.interval= 0		# intervalo para agregar terrones
		self.reloj= None		# pygame.time
		self.fondo= None		# el fondo
		self.etiqueta= None		# el mensaje sobre lo que se está cargando
		self.posicion_label= None	# la posicion de la etiqueta para cambiar el mensaje
		self.imagen_matrix= None 	# pygame.image.load(VG.get_terron())

		try:
			self.imagen_matrix= pygame.image.load(VG.get_terron())
		except:
			pass

		self.callback_handle_event= None
		self.latencia= 10
		self.setup()
		#self.ventana.blit(self.fondo, (0,0))
	
	# -------- SETEOS ----------------------
	def set_imagen_matrix(self, imagen):
		''' Setea una imagen para remplazar terron. '''
		if imagen:
			self.imagen_matrix = pygame.image.load(imagen)
		else:
			self.imagen_matrix= None

	def set_callback_event(self, callback):
		''' Conecta una función para detectar eventos mientras se ejecuta JAMatrix. '''
		self.callback_handle_event= callback
	def set_latencia(self, latencia):
		''' Setea la latencia de generación de terrones. '''
		if type(latencia)== int: self.latencia= latencia
	# -------- SETEOS ----------------------

	def carga_game(self):
		''' Carga este juego en un thread en segundo plano. '''
		thread = threading.Thread( target=self.juego.load )
		thread.start()
		while not self.juego.estado:
			self.run()
		self.unload() # descarga todo lo que puede para liberar memoria

	def unload(self):
		''' Al cambiar el estado del juego porque se han cargado todos sus objetos, se descarga JAMatrix en un thread en segundo plano. '''
		thread = threading.Thread( target=self.descarga_todo )
		thread.start()
		gc.collect()

	def run(self):
		''' JAMatrix corriendo. '''
		self.setup()
		pygame.mouse.set_visible(False)
		self.reloj.tick(35)
		if self.interval == self.latencia:
			self.genera_terrones()
			self.interval = 0
		cambios=[]
		self.widgets.clear(self.ventana, self.fondo)
		self.widgets.update()
		
		cambios.extend ( self.widgets.draw(self.ventana) )
		pygame.display.update(cambios)
		pygame.event.clear()
		#pygame.time.wait(1)
		self.interval += 1

		if self.callback_handle_event:
			return self.callback_handle_event()

	def descarga_todo(self):
		''' Libera memoria. '''
		self.widgets = None
		self.interval = 0
		self.reloj = None
		self.fondo = None
		self.etiqueta = None
		self.posicion_label = None

	def setup(self):
		''' Configura los objetos. '''
		if not self.widgets:
			self.widgets = pygame.sprite.OrderedUpdates()
		if not self.reloj:
			self.reloj = pygame.time.Clock()
		if not self.fondo:
			self.fondo = self.get_fondo(color= VG.get_negro(), tamanio=self.resolucion) # superficie
		if not self.etiqueta:
			self.etiqueta = JAMLabel (texto="Cargando %s" % (self.juego.name))
			self.etiqueta.set_text(tamanio= 50, color= VG.get_blanco())
		if not self.posicion_label:
			self.posicion_label = (self.resolucion[0]/2 - self.etiqueta.rect.w/2, self.resolucion[1]/2 - self.etiqueta.rect.h/2)
		self.etiqueta.set_posicion(punto= self.posicion_label)
		if not self.etiqueta in self.widgets.sprites():
			self.widgets.add(self.etiqueta)

	def get_fondo(self, color=(100,100,100,1), tamanio=(800,600)):
		''' El fondo de la ventana. '''
		superficie = pygame.Surface( tamanio, flags=HWSURFACE )
		superficie.fill(color)
		return superficie

	def genera_terrones(self):
		''' Nace un Terron. '''
		if not self.imagen_matrix: return
		x = random.randrange(0, self.resolucion[0], self.imagen_matrix.get_size()[0])
		terron = Terron(self)
		terron.rect.x, terron.rect.y = (x,-50)
		self.widgets.add(terron)

class Terron(pygame.sprite.Sprite):
	''' Sprite Terron. '''
	def __init__(self, base):
		pygame.sprite.Sprite.__init__(self)
		self.base= base
		self.imagen1 = self.base.imagen_matrix
		self.image = self.imagen1
		self.rect = self.image.get_rect()
		self.cuenta = 0
	def update(self):
		''' Terrón cae. '''
		self.rect.y += 4
		if self.rect.y > self.base.resolucion[1]:
			self.kill()

# ----- FIN DE CLASE JAMatrix - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
class Ejemplo(object):
	def __init__(self):

		# Variables obligatorias en tu juego para poder utilizar JAMatrix.
		self.resolucion = (800,600)
		self.ventana = None
		self.name= "Ejemplo JAMatrix"
		self.estado = False

		# Variables del juego
		self.reloj = None
		self.fondo = None

		self.jamclock= None
		self.jamcalendar= None
		self.jamclock1= None
		self.jamcalendar1= None
		self.jamclock2= None
		self.jamcalendar2= None

		self.preset() # crea la ventana principal

		# usando JAMatrix para cargar el juego
		self.matrix= JAMatrix(self, self.ventana, self.resolucion)
		self.matrix.set_callback_event(self.handle_event) # si quieres detectar eventos durante JAMatrix se ejecuta para cortar la carga.
		#self.matrix.set_imagen_matrix(os.getcwd() + "/Recursos/Iconos/bandera_uruguay.png")
		self.matrix.carga_game() # lanza JAMatrix
		
		# Comienza a ejecutar tu juego
		self.estado= "menu_0"
		self.run_menu_0()

	def run_menu_0(self):
		''' Tu juego corriendo. '''
		self.ventana.blit(self.fondo, (0,0))

		self.jamclock.draw(self.ventana)
		self.jamclock1.draw(self.ventana)
		self.jamclock2.draw(self.ventana)
		self.jamcalendar.draw(self.ventana)
		self.jamcalendar1.draw(self.ventana)
		self.jamcalendar2.draw(self.ventana)

		pygame.display.update()

		contador = 0
		while self.estado == "menu_0":
			self.reloj.tick(35)
	
			cambios=[]
			self.jamclock.clear(self.ventana, self.fondo)
			self.jamclock1.clear(self.ventana, self.fondo)
			self.jamclock2.clear(self.ventana, self.fondo)
			self.jamcalendar.clear(self.ventana, self.fondo)
			self.jamcalendar1.clear(self.ventana, self.fondo)
			self.jamcalendar2.clear(self.ventana, self.fondo)

			self.jamclock.update()
			self.jamclock1.update()
			self.jamclock2.update()
			self.jamcalendar.update()
			self.jamcalendar1.update()
			self.jamcalendar2.update()

			self.handle_event()
			pygame.event.clear()

			cambios.extend ( self.jamclock.draw(self.ventana) )
			cambios.extend ( self.jamclock1.draw(self.ventana) )
			cambios.extend ( self.jamclock2.draw(self.ventana) )
			cambios.extend ( self.jamcalendar.draw(self.ventana) )
			cambios.extend ( self.jamcalendar1.draw(self.ventana) )
			cambios.extend ( self.jamcalendar2.draw(self.ventana) )

			pygame.display.update(cambios)
			contador += 1

	def preset(self):
		''' Iniciando pygame y creando una ventana. '''
		pygame.init()
		pygame.display.set_mode(self.resolucion , 0, 0)
		self.ventana = pygame.display.get_surface()

	def load(self):
		''' Creando y seteando todos los objetos de tu juego. '''
		self.fondo = self.get_Fondo()
		self.reloj = pygame.time.Clock()
		
		self.jamclock= JAMClock()
		self.jamclock1= JAMClock()
		self.jamclock2= JAMClock()
		self.jamcalendar= JAMCalendar()
		self.jamcalendar1= JAMCalendar()
		self.jamcalendar2= JAMCalendar()

		# los tres de arriba
		posicion= (25,25)
		self.jamcalendar.set_posicion(punto= posicion)

		tamanio= self.jamcalendar.get_tamanio()
		posicion= (posicion[0]+tamanio[0], posicion[1])
		self.jamclock.set_posicion(punto= posicion)

		tamanio= self.jamclock.get_tamanio()
		posicion= (posicion[0]+tamanio[0], posicion[1])
		self.jamcalendar1.set_posicion(punto= posicion)

		# los tres de abajo
		tamanio= self.jamcalendar.get_tamanio()
		posicion= (self.jamcalendar.posicion[0], tamanio[1]+ posicion[1])
		self.jamclock1.set_posicion(punto= posicion)

		tamanio= self.jamclock1.get_tamanio()
		posicion= (self.jamclock1.posicion[0]+tamanio[0], posicion[1])
		self.jamcalendar2.set_posicion(punto= posicion)

		tamanio= self.jamcalendar2.get_tamanio()
		posicion= (self.jamclock.posicion[0]+tamanio[0], posicion[1])
		self.jamclock2.set_posicion(punto= posicion)


		pygame.display.set_caption("Ejemplo de Carga de un Juego con JAMatrix")
		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN,
					KEYUP, USEREVENT, QUIT, ACTIVEEVENT])
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN, VIDEORESIZE, VIDEOEXPOSE])
		pygame.mouse.set_visible(True)
		self.estado= True # Todo se ha cargado y seteado, listo para correr el juego.

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
		pygame.quit()
		sys.exit()



if __name__ == "__main__":
	Ejemplo()
