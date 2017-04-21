#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 13/06/2011 - CeibalJAM! - Uruguay
#   JAMCron.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys, time, os
from pygame.locals import *
gc.enable()

import JAMGlobals as VG
from JAMButton import JAMButton

class JAMCron(pygame.sprite.OrderedUpdates):
	''' Un Cronómetro. '''
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.cron= None			# el Cronómetro

		self.sonido= None		# Sonido reloj tick
		self.sonido_alarma= None	# Sonido de la larma
		self.duracion_alarma= 1		# cantidad de veces que debe sonar la alarma
		self.callback= None		# una función para ejecutar al finalizar la cuenta del cronómetro

		self.Construye()

	def Construye(self):
		self.sonido= VG.get_sound_clock_tick1()
		self.sonido_alarma= VG.get_alarma_reloj2()
		self.duracion_alarma= 1
		self.callback= None
		self.cron= Digital(self)
		self.add(self.cron)

	def run_alarma(self):
		''' Control de Alarma. '''
		self.pause()
		if self.sonido_alarma:
			self.sonido_alarma.set_volume(1.0)
			self.sonido_alarma.play(self.duracion_alarma-1)
		if self.callback:
			return self.callback(self)

	# ---------------- SETEOS -------------------
	def set_posicion(self, punto= (0,0)):
		''' Setea la posición en pantalla. '''
		self.cron.set_posicion(punto= punto)

	def set_alarma(self, tiempo= False, sound= False, duracion= False):
		''' Setea las alarmas, en (horas,minutos,segundos), sonido y duración. '''
		if tiempo and type(tiempo)== tuple and len(tiempo)==2:
			if type(tiempo[0])== int and type(tiempo[1])== int:
				self.cron.set_control(tiempo)
		if sound:
			self.sonido_alarma= sound
		if sound== None: self.sonido_alarma= None
		if duracion and type(duracion)== int:
			self.duracion_alarma= duracion

	def set_sound(self, sound= None):
		''' Setea un sonido para el segundero del cronómetro. '''
		if self.sonido:
			self.sonido.stop()
		if sound and self.sonido!= sound:
			self.sonido= sound
		if sound== None: self.sonido= None
		if self.cron.activado and self.sonido:
			self.sonido.set_volume(1.0)
			self.sonido.play(-1)

	def play(self):
		''' Activa y desactiva el cronómetro y las alarmas. '''
		self.cron.set_active_desactive(True)
	def pause(self):
		''' Activa y desactiva el cronómetro y las alarmas. '''
		self.cron.set_active_desactive(False)

	def reset(self):
		''' Pone a 0 el cronómetro. '''
		self.cron.segundos_transcurridos= 0
		self.cron.segundos_faltan= None

	def set_callback(self, callback):
		''' Setea una función para la alarma. '''
		self.callback= callback

	def get_tiempo_restante(self):
		return self.cron.segundos_faltan

	def get_tiempo_transcurrido(self):
		return self.cron.segundos_transcurridos
		
class Digital(JAMButton):
	''' Botón tipo etiqueta con el tiempo.'''
	def __init__(self, main):
		JAMButton.__init__(self, "00:00", None)
		self.main= main
		self.hora= "00:00:00" 		# La hora del sistema

		self.activado= False 		# Para pausa y play
		self.segundos_transcurridos= 0 	# Tiempo transcurrido, en segundos
		self.segundos_faltan= None	# Los segundos que faltan para terminar
		self.segundos_final= None 	# Cuando se deja de contar, en segundos

		self.set_tamanios(tamanio=(0,0), grosorbor=1, detalle=1, espesor=1)
		self.set_control((1,0))

	def set_control(self, valor):
		''' Para setear el tiempo final del cronómetro. '''
		minutos, segundos= valor
		self.segundos_final= minutos*60 + segundos

	def set_active_desactive(self, valor):
		''' pause/play. '''
		if self.main.sonido: self.main.sonido.stop()
		#if valor!= self.activado: # para poder habilitar/desabilitar el sonido
		self.activado= valor
		if self.activado:
			if self.main.sonido:
				self.main.sonido.set_volume(1.0)
				self.main.sonido.play(-1)
		if not self.activado:
			if self.main.sonido:
				self.main.sonido.stop()

	def update(self):
		''' Reloj. '''
		if not self.activado: return
		hora = time.strftime("%H:%M:%S")
		if hora != self.hora:
			self.hora= hora
			self.segundos_transcurridos+= 1
			self.actualiza_cron()

	def actualiza_cron(self):
		''' Actualiza el Cronómetro. '''
		# Calcula el tiempo que falta
		self.segundos_faltan = self.segundos_final - self.segundos_transcurridos
		m= 0
		s= self.segundos_faltan
		while s > 59:
			s= s-60
			m+= 1
		texto= "%s:%s" % (m, s)
		self.set_text(texto= texto)
		if self.segundos_faltan < 1:
			return self.main.run_alarma()


# ----- FIN DE CLASE JAMCron - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
class Ejemplo(object):
	def __init__(self):
		self.ventana = None
		self.reloj = None
		self.nivel = "menu_0"

		self.fondo = None
		self.widgets = None

		self.resolucion = (400,400)

		self.setup()
		self.Run()

	def setup(self):
		pygame.init()
		pygame.display.set_mode(self.resolucion , 0, 0)
		pygame.display.set_caption("Ejemplo de JAMCron")
		self.fondo = self.get_Fondo()

		self.widgets = JAMCron()
		self.widgets.set_posicion(punto= (50,50))

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

		self.widgets.set_alarma(tiempo= (0,5), duracion= 1)
		self.widgets.play()

		contador= 0
		while self.nivel == "menu_0":
			self.reloj.tick(35)
	
			cambios=[]
			self.widgets.clear(self.ventana, self.fondo)
			'''
			if contador == 200:
				self.widgets.pause()
			if contador == 400:
				self.widgets.play()
				contador= 0'''
			contador+= 1 
			self.widgets.update()
			self.handle_event()
			cambios.extend ( self.widgets.draw(self.ventana) )
			pygame.display.update(cambios)
	
	def get_Fondo(self):
		superficie = pygame.Surface( self.resolucion, flags=HWSURFACE )
		superficie.fill((0,0,0,255))
		return superficie

	def handle_event(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				teclas = pygame.key.get_pressed()
				if teclas[pygame.K_ESCAPE]:
					self.salir(None)
		pygame.event.clear()

	def salir(self, cron):
		pygame.quit()
		sys.exit()

if __name__ == "__main__":
	Ejemplo()
