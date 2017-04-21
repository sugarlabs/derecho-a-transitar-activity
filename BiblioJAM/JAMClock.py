#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 21/05/2011 - CeibalJAM! - Uruguay
#   JAMClock.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys, gobject, time, datetime, os
from pygame.locals import *
gc.enable()
pygame.font.init()

import JAMGlobals as VG
from JAMButton import JAMButton

class JAMClock(pygame.sprite.OrderedUpdates):
	''' Un reloj hecho en pygame. '''
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)
		COLORCARA, COLORBAS, COLORBOR, GROSORBOR, DETALLE, ESPESOR= VG.get_default_jambutton_values()
		self.datos_base= {"color": VG.get_blanco(), "colorborde": COLORBAS, "tamanio": (225,225), "grosorborde": 4}
		self.datos_agujas= {"segundero":1, "minutero":2, "hora":3, "color": VG.get_negro()}
		self.datos_numeros={"tipo": pygame.font.get_default_font(), "tamanio": 16, "color": VG.get_negro(), "colorbase": None,
			"colorborde": None, "colorcara": None}
		self.retiro= 4
		self.posicion= (0,0)

		self.sonido= VG.get_sound_clock_tick1()
		self.sonido.set_volume(1.0)

		self.sonido_alarma= None
		self.alarma= (100,100)
		self.duracion_alarma= 0
	
		self.alarma_activada= False

		self.sonido.play(-1)
		self.Reconstruye("todo")

	def Reconstruye(self, cambios):
		''' Reconstruye el reloj según cambios.'''
		if "todo" in cambios:
			self.empty()
			self.label= Digital(self)
			self.base_interna= Base_Interna(self)
			self.numeros= Numeros(self)
			self.base_externa= Base_Externa(self)
			self.segundero= Aguja(self, self.datos_agujas["segundero"], self.datos_agujas["color"], self.retiro)
			self.minutero= Aguja(self, self.datos_agujas["minutero"], self.datos_agujas["color"], self.retiro*2)
			self.horario= Aguja(self, self.datos_agujas["hora"], self.datos_agujas["color"], self.retiro*5)
			self.timer= Timer(self)

			self.add(self.base_externa)
			self.add(self.base_interna)
			self.add(self.label)
			self.add(self.numeros)
			self.add(self.horario)
			self.add(self.minutero)
			self.add(self.segundero)
			self.add(self.timer)

			self.timer.update()
			self.set_posicion(punto= self.posicion)

	def control_alarma(self, tiempo):
		''' Control de Alarma. '''
		if not self.sonido_alarma: return
		h= tiempo[0]
		m= tiempo[1]
		if (h,m) == self.alarma and not self.alarma_activada and self.sonido_alarma:
			self.alarma_activada= True
			try:
				self.sonido_alarma.set_volume(1.0)
				self.sonido_alarma.play(self.duracion_alarma)
			except:
				pass
			print "ALARMA SONANDO !!!"
		elif h > self.alarma[0] or m > self.alarma[1] and self.alarma_activada:
			self.alarma_activada= False
			print "ALARMA DESACTIVADA - VOLVERÁ A SONAR EN 24 HORAS A MENOS QUE LA DESACTIVES !!!"

	# ---------------- SETEOS -------------------
	def set_alarma(self, tiempo, sound, duracion):
		''' Setea las alarmas, en (horas,minutos), sonido y duración. '''
		self.alarma= tiempo
		self.duracion_alarma= duracion
		self.sonido_alarma= sound
		self.alarma_activada= False # 24/11/2011 De lo contrario sólo se puede configurar la alarma 1 vez.

	def set_sound(self, sound, play):
		''' Setea el sonido del segundero del reloj. '''
		if self.sonido:
			try:
				self.sonido.stop()
			except:
				pass

		self.sonido= sound
		if self.sonido and play:
			try:
				self.sonido.set_volume(1.0)
				self.sonido.play(-1)
			except:
				pass
			
	def set_tamanios(self, valor):
		''' Setea el tamaño del reloj segun valores predefinidos. '''
		if type(valor)== int and valor>0 and valor<5:
			UNO= {"tamaniobase": (225,225), "tamanioletra": 16}
			DOS= {"tamaniobase": (440,440), "tamanioletra": 35}
			TRES= {"tamaniobase": (550,550), "tamanioletra": 45}
			CUATRO= {"tamaniobase": (748,748), "tamanioletra": 70}
			if valor== 1:
				self.datos_base["tamanio"]= UNO["tamaniobase"]
				self.datos_numeros["tamanio"]= UNO["tamanioletra"]
			elif valor== 2:
				self.datos_base["tamanio"]= DOS["tamaniobase"]
				self.datos_numeros["tamanio"]= DOS["tamanioletra"]
			if valor== 3:
				self.datos_base["tamanio"]= TRES["tamaniobase"]
				self.datos_numeros["tamanio"]= TRES["tamanioletra"]
			elif valor== 4:
				self.datos_base["tamanio"]= CUATRO["tamaniobase"]
				self.datos_numeros["tamanio"]= CUATRO["tamanioletra"]
			self.Reconstruye("todo")

	def set_colors_base(self, colorcara, colorborde):
		''' Setea los colores de la base y los bordes. '''
		self.datos_base["color"]= colorcara
		self.datos_base["colorborde"]= colorborde
		self.Reconstruye("todo")

	def set_colors_agujas(self, color):
		''' Setea los colores de las agujas. '''
		self.datos_agujas["color"]= color
		self.Reconstruye("todo")
	
	def set_colors_numeros(self, colornum, colorbase, colorborde, colorcara):
		'''Setea los colores de los números y sus bases. '''
		self.datos_numeros["color"]= colornum
		self.datos_numeros["colorbase"]= colorbase
		self.datos_numeros["colorborde"]= colorborde
		self.datos_numeros["colorcara"]= colorcara
		self.numeros.set_colors()
		self.label.set_text(color= self.datos_numeros["color"])

		self.label.set_colores(colorbas= self.datos_numeros["colorbase"], colorbor= self.datos_numeros["colorborde"],
			colorcara= self.datos_numeros["colorcara"])
		
	def set_posicion(self, punto= None):
		''' Setea la posición en pantalla. '''
		if len(punto)== 2 and type(punto)== tuple and type(punto[0])== int and type(punto[1])== int:
			self.posicion= punto
			self.base_externa.set_posicion(punto= self.posicion)
			self.base_interna.rect.center= self.base_externa.rect.center

			x= self.base_interna.rect.x + self.base_interna.rect.w/2 - self.label.rect.w/2
			y= self.base_interna.rect.y + self.base_interna.rect.h/2 + self.retiro*2
			self.label.set_posicion(punto= (x,y))

			self.segundero.rect.center= self.base_interna.rect.center
			self.minutero.rect.center= self.base_interna.rect.center
			self.horario.rect.center= self.base_interna.rect.center
			self.timer.rect.center= self.base_interna.rect.center
			self.numeros.set_posicion()

	# ------------- GETS ------------------------
	def get_tamanio(self):
		return (self.base_externa.rect.w, self.base_externa.rect.h)

class Digital(JAMButton):
	''' Etiqueta con la hora en forma digital.'''
	def __init__(self, clock):
		JAMButton.__init__(self, "", None)
		self.clock= clock	
		tipo= self.clock.datos_numeros["tipo"]
		tamanio= self.clock.datos_numeros["tamanio"]/3+self.clock.datos_numeros["tamanio"]
		color= self.clock.datos_numeros["color"]
		self.set_text(tipo= tipo, tamanio= tamanio, color= color)
		self.set_tamanios(tamanio=(0,0), grosorbor=1, espesor=1)
		self.set_colores(colorbas= self.clock.datos_numeros["colorbase"], colorbor= self.clock.datos_numeros["colorborde"],
			colorcara= self.clock.datos_numeros["colorcara"])

	def update(self):
		''' Sobrecarga de update para anular la detección de eventos.'''
		pass

class Timer(pygame.sprite.Sprite):
	''' El centro del reloj - la máquina.'''
	def __init__(self, clock):
		pygame.sprite.Sprite.__init__(self)
		self.clock= clock
		self.hora= ("00:00:00")
		superficie= VG.get_Elipse(self.clock.datos_agujas["color"], (self.clock.retiro*2,self.clock.retiro*2))
		self.image= VG.get_my_surface_whit_elipse_border(superficie, self.clock.datos_base["color"], self.clock.datos_base["grosorborde"]/2)
		self.rect= self.image.get_rect()

	def update(self):
		hora = time.strftime("%H:%M:%S")
		fecha= str(datetime.date.today())
		if hora != self.hora:
			self.clock.label.set_text(texto= hora)
			h,m,s= hora.split(":")	
			hh, mm, ss= self.hora.split(":")

			if s != ss:
				self.clock.segundero.rota(int(s)*6)
			if m != mm:
				self.clock.minutero.rota(int(m)*6)
				self.clock.control_alarma( (int(h),int(m)) )
				self.clock.horario.rota(int(h)*30+int(m)/2)
			#if h != hh:
			#	self.clock.horario.rota(int(h)*30)
			self.hora= hora

class Aguja(pygame.sprite.Sprite):
	''' Clase base para las agujas.'''
	def __init__(self, clock, grosor, color, retiro):
		pygame.sprite.Sprite.__init__(self)
		self.clock= clock

		superficie= VG.get_Rectangulo(self.clock.datos_base["color"], self.clock.datos_base["tamanio"])
		superficie.set_colorkey(self.clock.datos_base["color"])
		x,y,w,h= superficie.get_rect() 
		punto= (w/2,h/2)
		pygame.draw.line(superficie, color, punto, (w/2,y+retiro), grosor)
		self.imagen_original= superficie

		self.image= self.imagen_original.copy()
		self.rect= self.image.get_rect()

	def rota(self, valor):
		self.image = pygame.transform.rotate(self.imagen_original, -valor)
		self.rect= self.image.get_rect()
		self.rect.center= self.clock.base_interna.rect.center

class Base_Externa(pygame.sprite.Sprite):
	def __init__(self, clock):
		pygame.sprite.Sprite.__init__(self)
		self.clock= clock

		w,h= self.clock.datos_base["tamanio"]
		w+= self.clock.retiro*2+self.clock.datos_base["grosorborde"]
		h+= self.clock.retiro*2+self.clock.datos_base["grosorborde"]
		superficie= VG.get_Rectangulo(self.clock.datos_base["color"], (w,h))
		superficie= VG.get_my_surface_whit_border(superficie, self.clock.datos_base["colorborde"], self.clock.datos_base["grosorborde"]/2)

		w+= self.clock.retiro*2+self.clock.datos_base["grosorborde"]*2
		h+= self.clock.retiro*2+self.clock.datos_base["grosorborde"]*2
		superficie2= VG.get_Rectangulo(self.clock.datos_base["color"], (w,h))
		superficie2= VG.pegar_imagenes_centradas(superficie, superficie2)
		self.image= VG.get_my_surface_whit_border(superficie2, self.clock.datos_base["colorborde"], self.clock.datos_base["grosorborde"])
		self.rect= self.image.get_rect()

	def set_posicion(self, punto= None):
		''' Setea la posición en pantalla. ES INTERNO'''
		if len(punto)== 2 and type(punto)== tuple and type(punto[0])== int and type(punto[1])== int:
			self.rect.x, self.rect.y= punto

class Base_Interna(pygame.sprite.Sprite):
	def __init__(self, clock):
		pygame.sprite.Sprite.__init__(self)
		self.clock= clock

		superficie= VG.get_Rectangulo(self.clock.datos_base["color"], self.clock.datos_base["tamanio"])
		self.image= superficie
		self.rect= self.image.get_rect()

class Numeros(pygame.sprite.OrderedUpdates):
	''' Los números en el fondo del reloj.'''
	def __init__(self, clock):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.clock= clock
		self.numeros= []
		self.Reconstruye(["todo"])

	def Reconstruye(self, cambios):
		''' Reconstruye el objeto según cambios.'''
		if "todo" in cambios:
			self.empty()
			self.cuadricula= VG.get_cuadricula(self.clock.base_interna.image, 11, 11)
			ancho, alto= (self.cuadricula[0][2],self.cuadricula[0][3])
			self.numeros= []
			for x in range(1,13):
				numero= Numero(x)
				numero.set_tamanios(tamanio=(ancho,alto))
				self.numeros.append(numero)
				self.add(numero)
			self.set_text()
			self.set_colors()
			self.set_posicion()

	def set_colors(self):
		''' Setea el color de los números y sus bases. ES INTERNO'''
		for numero in self.numeros:
			numero.set_text(color= self.clock.datos_numeros["color"])
			numero.set_colores(colorbas= self.clock.datos_numeros["colorbase"], colorbor= self.clock.datos_numeros["colorborde"],
				colorcara= self.clock.datos_numeros["colorcara"])
			
	def set_text(self):
		''' Setea los números en el fondo del reloj. ES INTERNO'''
		tipo= self.clock.datos_numeros["tipo"]
		tamanio= self.clock.datos_numeros["tamanio"]
		color= self.clock.datos_numeros["color"]
		lado= 0
		for numero in self.numeros:
			numero.set_text(tipo= tipo, tamanio= tamanio, color= color)
			numero.set_tamanios(tamanio=(0,0), grosorbor=1, espesor=1)
			a,b,c,d= numero.rect
			if lado< c: lado= c
			if lado< d: lado= d
		for numero in self.numeros:
			numero.set_tamanios(tamanio=(lado,lado), grosorbor=1, espesor=1)

	def set_posicion(self):
		''' Setea la posición en pantalla. ES INTERNO'''
		x,y= (self.clock.base_interna.rect.x, self.clock.base_interna.rect.y)
		self.numeros[0].set_posicion(punto=(x+self.cuadricula[8][0],y+self.cuadricula[8][1]))
		self.numeros[1].set_posicion(punto=(x+self.cuadricula[32][0],y+self.cuadricula[32][1]))
		self.numeros[2].set_posicion(punto=(x+self.cuadricula[65][0],y+self.cuadricula[65][1]))
		self.numeros[3].set_posicion(punto=(x+self.cuadricula[98][0],y+self.cuadricula[98][1]))
		self.numeros[4].set_posicion(punto=(x+self.cuadricula[118][0],y+self.cuadricula[118][1]))
		self.numeros[5].set_posicion(punto=(x+self.cuadricula[115][0],y+self.cuadricula[115][1]))
		self.numeros[6].set_posicion(punto=(x+self.cuadricula[112][0],y+self.cuadricula[112][1]))
		self.numeros[7].set_posicion(punto=(x+self.cuadricula[88][0],y+self.cuadricula[88][1]))
		self.numeros[8].set_posicion(punto=(x+self.cuadricula[55][0],y+self.cuadricula[55][1]))
		self.numeros[9].set_posicion(punto=(x+self.cuadricula[22][0],y+self.cuadricula[22][1]))
		self.numeros[10].set_posicion(punto=(x+self.cuadricula[2][0],y+self.cuadricula[2][1]))
		self.numeros[11].set_posicion(punto=(x+self.cuadricula[5][0],y+self.cuadricula[5][1]))

class Numero(JAMButton):
	def __init__(self, x):
		JAMButton.__init__(self, x, None)
	def update(self):
		''' Sobrecarga de update para anular la detección de eventos.'''
		pass

# ----- FIN DE CLASE JAMClock - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
class Ejemplo(object):
	def __init__(self):
		self.ventana = None
		self.reloj = None
		self.nivel = "menu_0"

		self.fondo = None
		self.widgets = None

		self.resolucion = (1024,768)

		self.setup()
		self.Run()

	def setup(self):
		pygame.init()
		pygame.display.set_mode(self.resolucion , 0, 0)
		pygame.display.set_caption("Ejemplo")
		self.fondo = self.get_Fondo()
		self.widgets = JAMClock()
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
		ALARMA= (19,50)
		SUENA= 5
		self.widgets.set_alarma(ALARMA, VG.get_alarma_reloj2(), SUENA)
		contador = 0
		while self.nivel == "menu_0":
			self.reloj.tick(35)
	
			cambios=[]
			self.widgets.clear(self.ventana, self.fondo)

			self.widgets.update()
			self.handle_event()
			#pygame.event.clear()
			cambios.extend ( self.widgets.draw(self.ventana) )
			pygame.display.update(cambios)
			contador += 1
			if contador== 50:
				colornum= VG.get_negro()
				colorbase,colorborde,colorcara= VG.get_estilo_papel_quemado()
				self.widgets.set_tamanios(2)
				self.widgets.set_colors_base(colorborde, colorcara)
			'''
				#self.widgets.set_colors_base(colorcara, colorborde)
				#self.widgets.set_colors_agujas(colorbase)
				self.widgets.set_colors_agujas(colornum)
				self.widgets.set_colors_numeros(colornum, colorbase, colorborde, colorcara)
				#self.widgets.set_tamanios(1)
			
			if contador== 200:
				colornum= VG.get_negro()
				colorbase,colorborde,colorcara= VG.get_estilo_celeste()

				self.widgets.set_colors_base(colorborde, colorcara)
				#self.widgets.set_colors_base(colorcara, colorborde)
				#self.widgets.set_colors_agujas(colorbase)
				self.widgets.set_colors_agujas(colornum)
				self.widgets.set_colors_numeros(colornum, colorbase, colorborde, colorcara)
				self.widgets.set_tamanios(2)
				
			if contador== 300:
				colornum= VG.get_negro()
				colorbase,colorborde,colorcara= VG.get_estilo_gris()

				self.widgets.set_colors_base(colorborde, colorcara)
				#self.widgets.set_colors_base(colorcara, colorborde)
				#self.widgets.set_colors_agujas(colorbase)
				self.widgets.set_colors_agujas(colornum)
				self.widgets.set_colors_numeros(colornum, colorbase, colorborde, colorcara)
				#self.widgets.set_tamanios(3)
			if contador== 400:
				contador= 0
				#self.widgets.set_tamanios(4)
				self.widgets.set_alarma((22,1), VG.get_alarma_reloj2(), 10)'''

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
