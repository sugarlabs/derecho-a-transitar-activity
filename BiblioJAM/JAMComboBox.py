#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 21/05/2011 - CeibalJAM! - Uruguay
#   JAMComboBox.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys, gobject, time, datetime, os
from pygame.locals import *
gc.enable()
pygame.font.init()

import JAMGlobals as VG
from JAMButton import JAMButton

class JAMComboBox(pygame.sprite.OrderedUpdates):
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)

		self.buttoncaption= None
		self.buttonaction= None
		self.items= {}
		self.buttonsitems= []

		self.limitecaracteres= 40
		self.text= {"tipo": None, "tamanio": None, "color": None, "font_from_file": None}
		self.colores= {"colorbas": None, "colorbor": None, "colorcara": None}

		self.posicion= (0,0)

		self.Reconstruye("todo")

	def Reconstruye(self, cambios):
		''' Reconstruye según cambios.'''
		if "todo" in cambios:
			self.buttoncaption= ButtonCaption(self)
			self.buttonaction= ButtonAction(self)

			self.set_posicion(punto= self.posicion)
			
			self.add(self.buttoncaption)
			self.add(self.buttonaction)
			
	def set_item_inicial(self):
		''' Pone el primer item en el caption del combo. '''
		self.set_item_in_caption(0)

	def set_item_in_caption(self, num):
		''' Pone el item indicado en el caption del combo. '''
		if self.buttonsitems and len(self.buttonsitems) >= num:
			boton_item= self.buttonsitems[num]
			self.buttoncaption.set_text(texto= boton_item.get_text())

	def ordena_items(self):
		''' Todos del mismo tamanio. '''
		self.buttoncaption.set_tamanios(tamanio=(0,0), grosorbor=1, detalle=1, espesor=1)
		self.buttonaction.set_tamanios(tamanio=(0,0), grosorbor=1, detalle=1, espesor=1)
		for item in self.buttonsitems:
			item.set_tamanios(tamanio=(0,0), grosorbor=1, detalle=1, espesor=1)


		ancho, alto= self.buttoncaption.get_tamanio()
		w,h= self.buttonaction.get_tamanio()
		if alto < h: alto= h
		for item in self.buttonsitems:
			ww,hh= item.get_tamanio()
			if ancho < ww: ancho= ww
			if alto < hh: alto= hh

		self.buttoncaption.set_tamanios(tamanio=(ancho,alto), grosorbor=1, detalle=1, espesor=1)
		self.buttonaction.set_tamanios(tamanio=(self.buttonaction.get_tamanio()[0],alto), grosorbor=1, detalle=1, espesor=1)
		for item in self.buttonsitems:
			item.set_tamanios(tamanio=(ancho,alto), grosorbor=1, detalle=1, espesor=1)

		if self.buttoncaption.get_text()== "JAMComboBox":
			self.set_item_inicial()
		self.set_posicion(punto= self.posicion)

	def show_items(self, buttonaction):
		''' Muestra los Items en el Combo. '''
		if self.buttonsitems:
			self.empty()
			self.add(self.buttonsitems)
		else:
			self.buttoncaption.set_text(texto= "JAMComboBox")

	def callback(self, button):
		''' Cuando se hace click sobre un item, la lista se contrae y muestra solo el elegido.
		Luego ejecuta el callback de ese boton.'''
		if button:
			self.empty()
			self.buttoncaption.set_text(texto= button.get_text())
			#self.buttoncaption.set_imagen(origen= button"direccion de archivo" , tamanio=(ancho,alto))
			self.add(self.buttoncaption)
			self.add(self.buttonaction)
			callback= self.items[button]
			if callback: return callback(button)
		else:
		# cuando se borra un item mientras se está mostrando la lista de items
			self.empty()
			self.buttoncaption.set_text(texto= "JAMComboBox")
			self.add(self.buttoncaption)
			self.add(self.buttonaction)

	# ----------- SETEOS ------------------------------
	def add_item(self, item, callback):
		''' Agrega un Item y su callback al Combo. '''
		if len(item) > self.limitecaracteres:
			item= "%s" % (item[:self.limitecaracteres])

		# hay que verificar que el nuevo item no exista ya en el combo.
		button= JAMButton(item, None)
		button.set_text(tipo= self.text["tipo"], tamanio= self.text["tamanio"], color= self.text["color"])
		button.connect(callback= self.callback, sonido_select= None)
		if self.colores["colorbas"] and self.colores["colorbor"] and self.colores["colorcara"]:
			a= self.colores["colorbas"]
			b= self.colores["colorbor"]
			c= self.colores["colorcara"]
			button.set_colores(colorbas= a, colorbor= b, colorcara= c)

		if self.text["font_from_file"]:
			button.set_font_from_file(self.text["font_from_file"], tamanio= self.text["tamanio"])

		self.items[button]= callback

		self.buttonsitems.append(button)
		self.ordena_items()

	def remove_item(self, item):
		''' Elimina un item del combo segun caption. '''
		for boton in self.buttonsitems:
			if boton.get_text()== item:
				del self.items[boton]
				self.buttonsitems.remove(boton)
				boton.kill()
				if not self.buttonsitems:
					self.callback(None)
				self.ordena_items()

	def remove_item_index(self, index):
		''' Elimina un item del combo segun indice. '''
		if len(self.buttonsitems) > 0 and index < len(self.buttonsitems):
			boton= self.buttonsitems[index]
			del self.items[boton]
			self.buttonsitems.remove(boton)
			boton.kill()
			if not self.buttonsitems:
				self.callback(None)
			self.ordena_items()

	def clear_items(self):
		''' Elimina todos los items en el combo.'''
		for boton in self.buttonsitems:
			self.items.clear()
			#self.buttonsitems.remove(boton)
			self.buttonsitems= []
			boton.kill()
			if not self.buttonsitems:
				self.callback(None)
			self.ordena_items()

	def connect_item(self, item, callback, sound):
		''' Conecta un item a una función. '''
		for boton in self.buttonsitems:
			if boton.get_text()== item:
				self.items[boton]= callback
				boton.connect(callback=callback, sonido_select=sound)

	def set_colores(self, colorbas= None, colorbor= None, colorcara= None):
		''' Setea los colores de todos los items. '''
		if colorbas and type(colorbas)== tuple:
			self.colores["colorbas"]= colorbas
		if colorbor and type(colorbor)== tuple:
			self.colores["colorbor"]= colorbor
		if colorcara and type(colorcara)== tuple:
			self.colores["colorcara"]= colorcara

		self.buttoncaption.set_colores(colorbas=colorbas, colorbor=colorbor, colorcara=colorcara)
		self.buttonaction.set_colores(colorbas=colorbas, colorbor=colorbor, colorcara=colorcara)
		for boton in self.buttonsitems:
			boton.set_colores(colorbas=colorbas, colorbor=colorbor, colorcara=colorcara)

	def set_text(self, tipo= None, tamanio= None, color= None):
		''' Seteo de tipo, tamaño y color de letra. '''
		cambios= False
		if tipo:
			self.text["font_from_file"]= None
			self.text["tipo"]= tipo
			cambios= True
		if tamanio and type(tamanio)== int:
			self.text["tamanio"]= tamanio
			cambios= True
		if color:
			self.text["color"]= color
			cambios= True

		if not cambios: return
		self.buttoncaption.set_text(tipo= self.text["tipo"], tamanio= self.text["tamanio"], color= self.text["color"])
		self.buttonaction.set_text(tipo= self.text["tipo"], tamanio= self.text["tamanio"], color= self.text["color"])
		for boton in self.buttonsitems:
			boton.set_text(tipo= self.text["tipo"], tamanio= self.text["tamanio"], color= self.text["color"])

		self.ordena_items()

	def set_font_from_file(self, fuente, tamanio= None):
		''' Seteo de tipo y tamaño de letra desde un archivo defuentes. '''
		if tamanio and type(tamanio)== int:
			self.text["tamanio"]= tamanio
		if fuente:
			self.text["font_from_file"]= fuente
			self.buttoncaption.set_font_from_file(self.text["font_from_file"], tamanio= self.text["tamanio"])
			self.buttonaction.set_font_from_file(self.text["font_from_file"], tamanio= self.text["tamanio"])
			for boton in self.buttonsitems:
				boton.set_font_from_file(self.text["font_from_file"], tamanio= self.text["tamanio"])

			self.ordena_items()

	def set_tamanios(self, tamanio=(0,0)):
		''' Setea el tamaño de los items. '''
		self.buttoncaption.set_tamanios(tamanio= tamanio)#, grosorbor=1, detalle=1, espesor=1)
		self.buttonaction.set_tamanios(tamanio= (self.buttonaction.get_tamanio()[0],tamanio[1]) )
		for item in self.buttonsitems:
			item.set_tamanios(tamanio= tamanio)

		ancho, alto= self.buttoncaption.get_tamanio()
		w,h= self.buttonaction.get_tamanio()
		if alto < h: alto= h
		for item in self.buttonsitems:
			ww,hh= item.get_tamanio()
			if ancho < ww: ancho= ww
			if alto < hh: alto= hh

		self.buttoncaption.set_tamanios(tamanio=(ancho,alto), grosorbor=1, detalle=1, espesor=1)
		self.buttonaction.set_tamanios(tamanio=(self.buttonaction.get_tamanio()[0],alto), grosorbor=1, detalle=1, espesor=1)
		for item in self.buttonsitems:
			item.set_tamanios(tamanio=(ancho,alto), grosorbor=1, detalle=1, espesor=1)

		self.set_posicion(punto= self.posicion)

	def set_alineacion_text(self, alineacion):
		''' La alineación del texto en los items. '''
		for item in self.buttonsitems:
			item.set_alineacion_label(alineacion)
		
	# ----------- SETEOS ------------------------------

	# -----------------SETEOS Que no afectan al tamaño -------------------
	def set_posicion(self, punto= (0,0)):
		if type(punto)== tuple and len(punto)== 2:
			if type(punto[0])== int and type(punto[1])== int:
				self.posicion= punto
				self.buttoncaption.set_posicion(punto= self.posicion)
				w,h= self.buttoncaption.get_tamanio()
				self.buttonaction.set_posicion(punto= (self.posicion[0]+w, self.posicion[1]) )

				x,y= self.posicion
				for item in self.buttonsitems:
					item.set_posicion(punto= (x,y))
					y+= item.get_tamanio()[1]

	def get_caption(self):
		''' Devuelve el texto del item en el caption de JAMComboBox. '''
		return self.buttoncaption.get_text()

	def get_tamanio_caption(self):
		''' Devuelve el ancho de caption y la altura de action.'''
		w= self.buttoncaption.get_tamanio()[0]
		h= self.buttonaction.get_tamanio()[1]
		return (w,h)

	def get_tamanio(self):
		''' Devuelve el tamaño de JAMComboBox. '''
		alto= 0
		ancho= self.buttoncaption.get_tamanio()[0] + self.buttonaction.get_tamanio()[0]
		if self.buttonsitems:
			for item in self.buttonsitems:
				alto+= item.get_tamanio()[1]
		else:
			alto= self.buttoncaption.get_tamanio()[1]
		return (ancho, alto)

	def get_posicion(self):
		''' Devuelve la posicion de JAMComboBox. '''
		return self.posicion

class ButtonCaption(JAMButton):
	def __init__(self, main):
		JAMButton.__init__(self, "JAMComboBox", None)
		self.main= main
		self.set_tamanios(tamanio=(0,0), grosorbor=1, detalle=1, espesor=1)
		if self.main.colores["colorbas"] and self.main.colores["colorbor"] and self.main.colores["colorcara"]:
			a= self.main.colores["colorbas"]
			b= self.main.colores["colorbor"]
			c= self.main.colores["colorcara"]
			self.set_colores(colorbas= a, colorbor= b, colorcara= c)
		if self.main.text["font_from_file"]:
			self.set_font_from_file(self.main.text["font_from_file"], tamanio= self.main.text["tamanio"])

	def update(self):
		''' Sobrecarga de update para anular la detección de eventos.'''
		pass

class ButtonAction(JAMButton):
	def __init__(self, main):
		JAMButton.__init__(self, ">", None)
		self.main= main
		self.set_tamanios(tamanio=(0,0), grosorbor=1, detalle=1, espesor=1)
		self.connect(callback= main.show_items, sonido_select= None)
		if self.main.colores["colorbas"] and self.main.colores["colorbor"] and self.main.colores["colorcara"]:
			a= self.main.colores["colorbas"]
			b= self.main.colores["colorbor"]
			c= self.main.colores["colorcara"]
			self.set_colores(colorbas= a, colorbor= b, colorcara= c)
		if self.main.text["font_from_file"]:
			self.set_font_from_file(self.main.text["font_from_file"], tamanio= self.main.text["tamanio"])

# ----- FIN DE CLASE JAMComboBox - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
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

		self.widgets = JAMComboBox()
		self.widgets.add_item("Salir", callback= self.salir)
		self.widgets.add_item("Prueba de Item 1", callback= None)
		self.widgets.add_item("Ultima Prueba de Item", callback= None)
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
				colorbase,colorborde,colorcara= VG.get_estilo_papel_quemado()
				self.widgets.set_colores(colorbas= colorbase, colorbor= colorborde, colorcara= colorcara)
				#self.widgets.set_font_from_file(VG.get_Font_fawn()[0], tamanio= 20)
	
			if contador== 200:
				self.widgets.set_tamanios(tamanio=(300,10))
				#self.widgets.set_text(tipo= "Purisa", tamanio= 10, color= VG.get_azul1())
				#self.widgets.remove_item("Prueba de Item 1")
				self.widgets.remove_item_index(0)
				#self.widgets.clear_items()
				contador= 0
			'''
			if contador== 300:
				self.widgets.set_alineacion_text("izquierda")'''

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

	def salir(self, button):
		pygame.quit()
		sys.exit()

if __name__ == "__main__":
	Ejemplo()
