#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 21/05/2011 - CeibalJAM! - Uruguay
#   JAMNubes.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys, random
from pygame.locals import *
gc.enable()

import JAMGlobals as VG

class JAMNubes(pygame.sprite.OrderedUpdates):
	''' Un reloj hecho en pygame. '''
	def __init__(self, intensidad=5, rectangulo= (0,0,1200,300)):
		pygame.sprite.OrderedUpdates.__init__(self)

		self.lluvia= False
		self.nubes= pygame.sprite.OrderedUpdates()

		self.rectangulo= rectangulo
		self.tamanios_posibles= []

		self.redefine_tamanios()

		# cantidad de nubes
		self.intensidad= intensidad

		# velocidades para las nubes
		self.velocidades= [1, 2, 3, -1, -2, 3]
		# latencia de actualización para las nubes
		self.latencia= 1
		# genera nubes iniciales y las reposiciona
		for c in range(0, self.intensidad+1):
			self.genera_nube()
		for x in range(self.rectangulo[2]/2):
			self.update()

		self.sonido= VG.get_sound_lluvia()
		self.suelo= self.rectangulo[1] + self.rectangulo[3] + self.rectangulo[3]/3

	# ---------------- SETEOS ----------------------------
	def set_suelo(self, valor):
		''' Setea un valor y para el suelo (es donde desaparecen las gotas de lluvia). '''
		if not type(valor)== int: return
		self.suelo= valor

	def set_lluvia(self, valor):
		''' Activa o desactiva la lluvia. '''
		if not type(valor)== bool: return
		if valor == self.lluvia:
			return
		else:
			self.lluvia= valor
			if self.lluvia:
				self.sonido.play(-1)
			else:
				self.sonido.stop()

	def set_intensidad(self, intensidad):
		''' Setea una nueva intensidad para las nubes. '''
		if not type(intensidad)== int: return
		self.intensidad= intensidad

	def set_latencia(self, latencia):
		''' Setea una nueva latencia de actualización para las nubes. '''
		if not type(latencia)== int: return
		self.latencia= latencia

	def set_rectangulo(self, rectangulo):
		''' Setea un nuevo rectángulo donde dibujar las nubes. '''
		if not type(rectangulo)== tuple: return
		for x in rectangulo:
			if not type(x)== int: return
		self.rectangulo= rectangulo
		self.redefine_tamanios()

	def set_velocidad(self, velocidades):
		''' Setea las velocidad de las nubes a partir de una lista de enteros. '''
		if not type(velocidades)== list: return
		for nube in self.sprites():
			random.seed()
			velocidad= random.choice(velocidades)
			if not type(velocidad)== int: return
			nube.velocidad= velocidad
		self.velocidades= velocidades

	# ------------------ Construcción ---------------------
	def redefine_tamanios(self):
		''' redefinición de tamaños para las nubes y el rectángulo general donde se dibujan. '''
		x,y,w,h= self.rectangulo
		tamanio_base= self.rectangulo[2]
		a= int(tamanio_base/4)
		b= int(tamanio_base/3)
		c= int(tamanio_base/2)
		d= int(tamanio_base/1.5)
		anchos= [a, b, b, c, c, c, d, d, d, d, d]

		altos= [2,3,4,5]
		self.tamanios_posibles= []
		for ancho in anchos:
			random.seed()
			self.tamanios_posibles.append( (ancho,ancho/random.choice(altos)) )

	def genera_nube(self):
		''' Nace una nube. '''
		nube= Nube(self)
		x,y,w,h= nube.rect

		# posiciona la nube a derecha o izquierda según su dirección
		random.seed()
		if nube.velocidad > 0:
			x= self.rectangulo[0]-w + 1
		elif nube.velocidad < 0:
			x= self.rectangulo[0]+self.rectangulo[2] - 1

		# posiciona la nube a una altura al azar
		y= random.choice(range(self.rectangulo[1]-int(h/3 *2), self.rectangulo[1]+self.rectangulo[3]-h))

		nube.set_posicion(punto= (x, y))
		self.nubes.add(nube)
		self.add(nube)


class Nube(pygame.sprite.Sprite):
	''' Una nube. '''
	def __init__(self, nubes):
		pygame.sprite.Sprite.__init__(self)
		self.efecto= nubes

		self.posicion= (0,0)
		self.latencia= self.efecto.latencia
		self.cuenta= 0

		random.seed()
		self.velocidad= random.choice(self.efecto.velocidades)

		# define el tamanio de la nube
		random.seed()
		tamanio= random.choice(self.efecto.tamanios_posibles)
		self.image= pygame.transform.scale(VG.get_nube(), tamanio)
		random.seed()
		if random.choice([True, False]):
			self.image= pygame.transform.flip(self.image, True, False)
		self.rect= self.image.get_rect()
	
	def set_posicion(self, punto=(0,0)):
		''' Setea la posicion de la nube. '''
		self.posicion= punto
		self.rect.x, self.rect.y= self.posicion

	def update(self):
		''' Se mueve la nube según velocidad y orientacion. '''
		self.cuenta += 1
		if self.cuenta == self.latencia:
			self.cuenta= 0
			self.set_posicion(punto=(self.posicion[0] + self.velocidad, self.posicion[1]))
			if not self.rect.colliderect(self.efecto.rectangulo):
				if len(self.efecto.nubes.sprites())-1 < self.efecto.intensidad:
					while len(self.efecto.nubes.sprites())-1 != self.efecto.intensidad:
						self.efecto.genera_nube()
				self.kill()
			else:
				if self.efecto.lluvia: self.efecto.add(Gota(self.efecto, self.rect))


class Gota(pygame.sprite.Sprite):
	''' Una gota de lluvia. '''
	def __init__(self, nubes, rect):
		pygame.sprite.Sprite.__init__(self)
		self.efecto= nubes
		x,y,w,h= rect

		random.seed()
		tamanio= random.randrange(1, 3)
		colores= [VG.get_blanco(), VG.get_celeste_pastel_claro1()]
		self.image= VG.get_Elipse(random.choice(colores), (tamanio,tamanio))
		self.rect= self.image.get_rect()
		random.seed()
		x= random.randrange(x, x+w)
		y= y+h
		self.posicion=(0,0)
		self.set_posicion(punto=(x,y-1))

		self.suelo= self.efecto.suelo
		random.seed()
		self.velocidad= random.randrange(3, 6)

	def set_posicion(self, punto=(0,0)):
		self.posicion= punto
		self.rect.x, self.rect.y= self.posicion

	def update(self):
		x= self.rect.x
		y= self.rect.y + self.velocidad
		if y > self.suelo:
			 self.kill()
		else:
			self.set_posicion(punto=(x,y))

# ----- FIN DE CLASE JAMNube - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
class Ejemplo(object):
	def __init__(self):
		self.ventana = None
		self.reloj = None
		self.nivel = "menu_0"

		self.fondo = None
		self.widgets = None

		self.resolucion = (1200,700)

		self.setup()
		self.Run()

	def setup(self):
		pygame.init()
		pygame.display.set_mode(self.resolucion , 0, 0)
		pygame.display.set_caption("Ejemplo")
		self.fondo = self.get_Fondo()
		self.widgets = JAMNubes(rectangulo= (0,0,1200,400))
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

			self.widgets.update()
			self.handle_event()
			pygame.event.clear()
			cambios.extend ( self.widgets.draw(self.ventana) )
			pygame.display.update(cambios)
	
			if contador== 200:
				self.widgets.set_lluvia(True)
				#self.widgets.set_intensidad(1)
			if contador== 500:
				#self.widgets.set_lluvia(False)
				#self.widgets.set_intensidad(5)
				contador= 0
			contador += 1

	def get_Fondo(self):
		import os
		superficie = pygame.Surface( self.resolucion, flags=HWSURFACE )
		superficie.fill(VG.get_celeste_cielo3())
		im= os.getcwd() + "/Recursos/Praderas/pradera1.png"
		imagen= pygame.transform.scale(pygame.image.load(im), (1200,300))
		superficie.blit(imagen, (0,400))
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
