#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 16/04/2011 - CeibalJAM! - Uruguay
#   JAMButton.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys
from pygame.locals import *
gc.enable()

import JAMGlobals as VG
from JAMLabel import JAMLabel

class JAMButton(pygame.sprite.Sprite):
	def __init__(self, texto, imagen, tipo="rectangulo"):
		pygame.sprite.Sprite.__init__(self)

		self.image= None
		self.rect= None
		self.posicion= (0,0)
		self.select= False
		self.sonido_select= VG.get_sound_select()
		self.callback= None
		self.alineacion= "centro"
		self.tipo = tipo

		COLORCARA, COLORBAS, COLORBOR, GROSORBOR, DETALLE, ESPESOR= VG.get_default_jambutton_values()

		self.base= {"tamanio":None, "colorbas":COLORBAS, "colorbor":COLORBOR,
			"grosorbor":GROSORBOR, "detalle":DETALLE, "espesor":ESPESOR}
		self.cara= {"tamanio":None, "color":COLORCARA}
		self.borde_label= {"grosor": 0, "color":VG.get_negro()}

		self.etiqueta_unselect= JAMLabel(texto)
		self.etiqueta_unselect.set_contenedor(colorbas=self.cara["color"])
		self.etiqueta_select= JAMLabel(texto)
		self.etiqueta_select.set_contenedor(colorbas=self.base["colorbor"])

		self.JAMObjects = {"JAMLabelunselect": self.etiqueta_unselect,
			"JAMLabelselect": self.etiqueta_select, "Base": self.base,
			"Cara": self.cara, "Borde": self.borde_label}

		self.imagen_cara_unselect= None
		self.imagen_cara_select= None
		self.final_unselect= None
		self.final_select= None

		self.Reconstruye_JAMButton(["texto"])

	# ---------- SETEOS Y GET GENERALES ---------- #
	def get_text(self):
		''' Devuelve la cadena de Texto en JAMLabel. '''
		return self.etiqueta_unselect.get_text()

	def set_tipo(self, tipo):
		''' Setea el tipo de botón "elipse" o "rectangulo". '''
		if tipo and tipo != self.tipo and (tipo== "elipse" or tipo== "rectangulo"):
			self.tipo= tipo
			self.Reconstruye_JAMButton(["texto"])

	def get_posicion(self):
		''' Devuelve la posición actual. '''
		return self.posicion

	# ---------- SETEOS SOBRE LA ETIQUETA ---------- #
	def set_text(self, tipo=None, tamanio=None, color=None, texto=None):
		''' Setea el Texto en JAMLabel. '''
		self.etiqueta_unselect.set_text(tipo=tipo, tamanio=tamanio, color=color, texto=texto)
		self.etiqueta_select.set_text(tipo=tipo, tamanio=tamanio, color=color, texto=texto)
		self.Reconstruye_JAMButton(["texto"])

	def set_font_from_file(self, direccion_archivo, tamanio= None):
		''' Setea la fuente desde un archivo en JAMLabel. '''
		self.etiqueta_unselect.set_font_from_file(direccion_archivo, tamanio)
		self.etiqueta_select.set_font_from_file(direccion_archivo, tamanio)
		self.Reconstruye_JAMButton(["texto"])

	def set_imagen(self, origen=None, tamanio=None):
		''' Setea el Imagen en JAMLabel. '''
		self.etiqueta_unselect.set_imagen(origen=origen, tamanio=tamanio)
		self.etiqueta_select.set_imagen(origen=origen, tamanio=tamanio)
		self.Reconstruye_JAMButton(["imagen"])
	# ---------- SETEOS SOBRE LA ETIQUETA ---------- #

	# ---------- SETEOS SOBRE LA BASE ---------- #
	def set_tamanios(self, tamanio=None, grosorbor=None, detalle=None, espesor=None):
		cambios= False
		# desactivar tamaños
		if tamanio == -1 and tamanio != None:
			tamanio= None
			self.base["tamanio"]= None
			cambios= True
		if grosorbor == -1 and grosorbor != None:
			grosorbor= None
			self.base["grosorbor"]= 1
			cambios= True
		if detalle == -1 and detalle != None:
			detalle= None
			self.base["detalle"]= 1
			cambios= True
		if espesor == -1 and espesor != None:
			espesor= None
			self.base["espesor"]= 1
			cambios= True

		# establecer tamaños
		if tamanio and tamanio != self.base["tamanio"]:
			self.base["tamanio"]= tamanio
			cambios= True
		if grosorbor and grosorbor != self.base["grosorbor"]:
			self.base["grosorbor"]= grosorbor
			cambios= True
		if detalle and detalle != self.base["detalle"]:
			self.base["detalle"]= detalle
			cambios= True
		if espesor and espesor != self.base["espesor"]:
			self.base["espesor"]= espesor
			cambios= True

		if cambios:
			self.Reconstruye_JAMButton(["tamanio"])

	def set_colores(self, colorbas=None, colorbor=None, colorcara=None):
		''' Setea los colores del botón y la etiqueta. '''
		cambios= False
		if colorbas and colorbas != self.base["colorbas"]:
			self.base["colorbas"]= colorbas
			cambios= True
		if colorbor and colorbor != self.base["colorbor"]:
			self.base["colorbor"]= colorbor
			cambios= True
		if colorcara and colorcara != self.cara["color"]:
			self.cara["color"]= colorcara
			cambios= True

		if cambios:
			self.etiqueta_unselect.set_contenedor(colorbas=self.cara["color"])#, grosor=None, colorbor=None)
			self.etiqueta_select.set_contenedor(colorbas=self.base["colorbor"])#, grosor=None, colorbor=None)
			self.Reconstruye_JAMButton(["colores"])

	def set_borde_label(self, grosor=None, color=None):
		''' Agrega o quita un borde sobre la cara de JAMButton. '''
		cambios= False
		if grosor < 1 and grosor != self.borde_label["grosor"]:
			grosor= None
			cambios= True
		if grosor and grosor != self.borde_label["grosor"]:
			self.borde_label["grosor"]= grosor
			cambios= True
		if color and color != self.borde_label["color"]:
			self.borde_label["color"]= color
			cambios= True

		if cambios:
			self.Reconstruye_JAMButton(["borde"])

	def set_alineacion_label(self, alineacion):
		''' Setea la alineacion de JAMLabel sobre la cara de JAMButton. '''
		if alineacion == "centro" or alineacion == "izquierda" or alineacion == "derecha":
			self.alineacion= alineacion
			self.Reconstruye_JAMButton(["alineacion"])
	# ---------- SETEOS SOBRE LA BASE ---------- #

	def connect(self, callback=None, sonido_select=None):
		'''Conecta el botón a una función y un sonido para reproducir al hacer click sobre JAMButton. '''
		self.callback = callback
		self.sonido_select = sonido_select # debes pasar una referencia al audio ya cargado para no cargarlo cada vez que creas un botón

	def set_posicion(self, punto=None):
		''' Setea la posición de JAMButton en la pantalla. '''
		try:
			if punto:
				self.rect.x, self.rect.y = (punto)
				self.posicion = punto
		except:
			pass

	# ------------- GETS ------------------------
	def get_tamanio(self):
		return (self.rect.w, self.rect.h)

	# ----------- CONSTRUCCION -------------------
	def Reconstruye_JAMButton(self, cambios):
		''' Cada vez que se setea algo, se reconstruye JAMButton con sus nuevos valores. '''
		if "tamanio" in cambios:
			# reconstruye la cara en base a la etiqueta
			self.cara["tamanio"]= None
			self.imagen_cara_unselect, self.imagen_cara_select= self.construye_cara()

			# verifica tamaño minimo para la base según la cara reconstruida
			anchominimo, altominimo= self.get_minimo_tamanio_base()
			if not self.base["tamanio"]: self.base["tamanio"]= (anchominimo, altominimo)
			ancho, alto= self.base["tamanio"]
			if anchominimo > ancho:	ancho= anchominimo
			if altominimo > alto: alto= altominimo

			# Establece los nuevos tamaños
			self.base["tamanio"]= (ancho, alto)
			self.cara["tamanio"]= self.get_tamanio_cara_recalculado()
		
		self.imagen_cara_unselect, self.imagen_cara_select= self.construye_cara() 	# pegar la etiqueta sobre la cara (¿Alineaciones?)
		self.final_unselect, self.final_select = self.construye_boton() 		# pegar la cara sobre la base

		self.image = self.final_unselect
		self.rect = self.image.get_rect()

		self.set_posicion(self.posicion) # seteo automático de posición

	def get_minimo_tamanio_base(self):
		''' Devuelve el tamaño mínimo que puede tener la base del botón. '''
		x= self.base["grosorbor"] + int(self.base["espesor"]/3)
		ancho= x + self.cara["tamanio"][0] + self.base["espesor"] + self.base["grosorbor"]
		y= self.base["grosorbor"] + int(self.base["espesor"]/3)
		alto= y + self.cara["tamanio"][1] + self.base["espesor"] + self.base["grosorbor"]
		return (ancho, alto)

	def get_tamanio_cara_recalculado(self):
		''' Devuelve el tamaño que debe tener la cara luego de seteados los tamaños del JAMButton. '''
		tamanio= (0,0)
		if self.tipo == "elipse":
			(xx,yy,ss,zz)= self.etiqueta_unselect.rect
			x= self.base["grosorbor"] + int(self.base["espesor"]/3)+zz/2
			ancho= x + self.base["espesor"] + self.base["grosorbor"]+zz/2
			y= self.base["grosorbor"] + int(self.base["espesor"]/3)+zz/2
			alto= y + self.base["espesor"] + self.base["grosorbor"]+zz/2
			a,h= self.base["tamanio"]
			tamanio= (a- ancho, h -alto)
		else:
			x= self.base["grosorbor"] + int(self.base["espesor"]/3)
			ancho= x + self.base["espesor"] + self.base["grosorbor"]
			y= self.base["grosorbor"] + int(self.base["espesor"]/3)
			alto= y + self.base["espesor"] + self.base["grosorbor"]
			a,h= self.base["tamanio"]
			tamanio= (a- ancho, h -alto)
		return tamanio

	def construye_cara(self):
		''' Crea la cara del botón y pega centrado en ella el JAMLabel. '''
		unselect, select= (None, None)
		if self.tipo == "elipse":
			w, h= (0,0)
			# toma tamaño de etiqueta como referencia
			if not self.cara["tamanio"]:
				w= self.etiqueta_unselect.rect.w+self.base["detalle"]+self.etiqueta_unselect.rect.h
				h= self.etiqueta_unselect.rect.h+self.base["detalle"]+self.etiqueta_unselect.rect.h
				self.cara["tamanio"] = (w, h)
			# la cara nunca puede ser menor que la etiqueta pero si mayor
			if self.cara["tamanio"] and self.cara["tamanio"][0]<self.etiqueta_unselect.rect.w+self.base["detalle"]+self.etiqueta_unselect.rect.h:
				w= self.etiqueta_unselect.rect.w+self.base["detalle"]+self.etiqueta_unselect.rect.h
				self.cara["tamanio"] = (w, h)
			if self.cara["tamanio"] and self.cara["tamanio"][1]<self.etiqueta_unselect.rect.h+self.base["detalle"]+self.etiqueta_unselect.rect.h:
				h= self.etiqueta_unselect.rect.h+self.base["detalle"]+self.etiqueta_unselect.rect.h
				self.cara["tamanio"] = (w, h)
			unselect= VG.get_Elipse(self.cara["color"], self.cara["tamanio"])
			select= VG.get_Elipse(self.base["colorbor"], self.cara["tamanio"])

			# alineación desabilitada por bug
			self.alineacion = "centro"
			unselect= VG.pegar_imagenes_centradas(self.etiqueta_unselect.image, unselect)
			select= VG.pegar_imagenes_centradas(self.etiqueta_select.image, select)
		else:
			w, h= (0,0)
			# toma tamaño de etiqueta como referencia
			if not self.cara["tamanio"]:
				w= self.etiqueta_unselect.rect[2]+self.base["detalle"]
				h= self.etiqueta_unselect.rect[3]+self.base["detalle"]
				self.cara["tamanio"] = (w, h)
			# la cara nunca puede ser menor que la etiqueta pero si mayor
			if self.cara["tamanio"] and self.cara["tamanio"][0]<self.etiqueta_unselect.rect[2]+self.base["detalle"]:
				w= self.etiqueta_unselect.rect[2]+self.base["detalle"]
				self.cara["tamanio"] = (w, h)
			if self.cara["tamanio"] and self.cara["tamanio"][1]<self.etiqueta_unselect.rect[3]+self.base["detalle"]:
				h= self.etiqueta_unselect.rect[3]+self.base["detalle"]
				self.cara["tamanio"] = (w, h)
			unselect= VG.get_Rectangulo(self.cara["color"], self.cara["tamanio"])
			select= VG.get_Rectangulo(self.base["colorbor"], self.cara["tamanio"])

			if self.alineacion == "centro":
				unselect= VG.pegar_imagenes_centradas(self.etiqueta_unselect.image, unselect)
				select= VG.pegar_imagenes_centradas(self.etiqueta_select.image, select)
			elif self.alineacion == "izquierda":
				unselect= VG.pegar_imagenes_alineado_izquierda(self.etiqueta_unselect.image, unselect)
				select= VG.pegar_imagenes_alineado_izquierda(self.etiqueta_select.image, select)
			elif self.alineacion == "derecha":
				unselect= VG.pegar_imagenes_alineado_derecha(self.etiqueta_unselect.image, unselect)
				select= VG.pegar_imagenes_alineado_derecha(self.etiqueta_select.image, select)
			else:
				self.alineacion = "centro"
				unselect= VG.pegar_imagenes_centradas(self.etiqueta_unselect.image, unselect)
				select= VG.pegar_imagenes_centradas(self.etiqueta_select.image, select)

		if self.borde_label["grosor"] > 1 and self.borde_label["grosor"] != None:
			if not self.borde_label["color"]: self.borde_label["color"]= VG.get_negro()
			if self.tipo == "elipse":
			# desabilitado por bug
				#unselect= VG.get_my_surface_whit_elipse_border(unselect, self.borde_label["color"], self.borde_label["grosor"])
				#select= VG.get_my_surface_whit_elipse_border(select, self.borde_label["color"], self.borde_label["grosor"])
				pass
			else:
				unselect= VG.get_my_surface_whit_border(unselect, self.borde_label["color"], self.borde_label["grosor"])
				select= VG.get_my_surface_whit_border(select, self.borde_label["color"], self.borde_label["grosor"])
		return unselect, select

	def construye_boton(self):
		''' Construye las imagenes finales del botón. '''
		unselect= None
		select= None
		if self.tipo == "elipse":
			x= self.base["grosorbor"] + int(self.base["espesor"]/3)
			ancho= x + self.cara["tamanio"][0] + self.base["espesor"] + self.base["grosorbor"]
			y= self.base["grosorbor"] + int(self.base["espesor"]/3)
			alto= y + self.cara["tamanio"][1] + self.base["espesor"] + self.base["grosorbor"]
			self.base["tamanio"]= (ancho, alto)
			unselect= VG.get_Elipse(self.base["colorbas"], self.base["tamanio"])
			unselect= VG.get_my_surface_whit_elipse_border(unselect, self.base["colorbor"], self.base["grosorbor"])
			select= VG.get_Elipse(self.base["colorbas"], self.base["tamanio"])
			select= VG.get_my_surface_whit_elipse_border(select, self.base["colorbor"], self.base["grosorbor"])
		else:
			x= self.base["grosorbor"] + int(self.base["espesor"]/3)
			ancho= x + self.cara["tamanio"][0] + self.base["espesor"] + self.base["grosorbor"]
			y= self.base["grosorbor"] + int(self.base["espesor"]/3)
			alto= y + self.cara["tamanio"][1] + self.base["espesor"] + self.base["grosorbor"]
			self.base["tamanio"]= (ancho, alto)
			unselect= VG.get_Rectangulo(self.base["colorbas"], self.base["tamanio"])
			unselect= VG.get_my_surface_whit_border(unselect, self.base["colorbor"], self.base["grosorbor"])
			select= VG.get_Rectangulo(self.base["colorbas"], self.base["tamanio"])
			select= VG.get_my_surface_whit_border(select, self.base["colorbor"], self.base["grosorbor"])

		unselect.blit(self.imagen_cara_unselect, (x, y))
		select.blit(self.imagen_cara_select, (x, y))
		return unselect, select
	# -------------------- FIN DE METODOS DE CONSTRUCCION -------------------- #

	# -------------------- INICIO DE METODOS INTERNOS AUTOMÁTICOS -------------------- #
	def play_select(self):
	# reproduce un sonido cuando pasas el mouse sobre el botón
		if self.sonido_select:
			self.sonido_select.play()

	def update(self):
	# responde a los eventos del mouse sobre el sprite
		'''
		posicion = pygame.mouse.get_pos()
		# Selecciona el botón cuando el mouse pasa encima de él
		if self.rect.collidepoint(posicion):
			if self.select == False:
				self.play_select()
				self.image = self.final_select.copy()
				self.select = True

			if  pygame.event.get(pygame.MOUSEBUTTONDOWN):
				if self.callback:
					return self.callback(self) # modificación 29 de mayo el boton se pasa a si mismo.
		else:
			if self.select == True:
				self.image = self.final_unselect.copy()
				self.select = False'''

		''' Reimplementación para Compatibilidad en Plug de gtk y mejora en rendimiento:
		Los eventos se capturan por su tipo, se manejan y si es necesario se republican para habilitar la captura
		de los mismos por parte de otros controles.'''
		eventos_republicar= []
		eventos= pygame.event.get(pygame.MOUSEBUTTONDOWN)
		for event in eventos:
			posicion = event.pos
			if self.rect.collidepoint(posicion):
			# Si el mouse está presionado sobre el botón.
				if  self.callback:
				# y si además hay callback para esta acción.
					pygame.event.clear()
					return self.callback(self)
			else:
			# Si el mouse no está presionado sobre el botón.
				if not event in eventos_republicar: eventos_republicar.append(event)

		eventos= pygame.event.get(pygame.MOUSEMOTION)
		for event in eventos:
			posicion = event.pos
			if self.rect.collidepoint(posicion):
			# Si el mouse está sobre el botón.
				if self.select == False:
					self.play_select()
					self.image = self.final_select
					self.select = True
			else:
			# Si el mouse no está sobre el botón.
				if self.select == True:
					self.image = self.final_unselect
					self.select = False
			if not event in eventos_republicar: eventos_republicar.append(event)
		
		for event in eventos_republicar:
		# Se republican todos los eventos que este control no debe manejar.
			pygame.event.post(event)

# ----- FIN DE CLASE JAMButton - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
class Ejemplo(object):
	def __init__(self):
		self.ventana = None
		self.reloj = None
		self.nivel = "menu_0"

		self.fondo = None
		self.widgets = None

		self.resolucion = (800,800)

		self.setup()
		self.Run()

	def Run(self):
		self.ventana.blit(self.fondo, (0,0))
		self.widgets.draw(self.ventana)
		pygame.display.update()

		#self.widgets.sprites()[0].set_text(tipo="Arial", tamanio=25, color=None, texto="Flavio Danesse")
		#self.widgets.sprites()[0].set_imagen(origen=VG.URUGUAY, tamanio=None)
		#self.widgets.sprites()[0].set_colores(colorbas=None, colorbor=color, colorcara=None)
		#self.widgets.sprites()[0].set_tamanios(tamanio=tamanio, grosorbor=None, detalle=None, espesor=None)
		#self.widgets.sprites()[0].set_posicion(punto=(25,25))
		#self.widgets.sprites()[0].set_borde_label(grosor=2, color=VG.get_negro())
		self.widgets.sprites()[0].connect(callback= self.salir, sonido_select= VG.get_sound_select())
		contador = 0
		while self.nivel == "menu_0":
			self.reloj.tick(35)
	
			cambios=[]
			self.widgets.clear(self.ventana, self.fondo)
			

			if contador == 100:
				# Activa la siguiente línea para provocar cambios de texto en JAMButton
				contador= self.ejemplo_cambia_texto_en_button()
				# Activa la siguiente línea para provocar cambios de imagen en JAMButton
				contador= self.ejemplo_cambia_imagen_en_button()
				# Activa la siguiente línea para provocar cambios de contenedor en JAMButton
				contador= self.ejemplo_cambia_colores_en_button()
				# Activa la siguiente línea para provocar cambios de posicion en JAMButton
				contador= self.ejemplo_cambia_posicion_en_button()
				# Activa la siguiente línea para provocar cambios de tamaño en JAMButton
				contador= self.ejemplo_cambia_tamanios_en_button()
				pass # y amor

			self.widgets.update()
			self.handle_event()
			pygame.event.clear()
			cambios.extend ( self.widgets.draw(self.ventana) )
			pygame.display.update(cambios)
			contador += 1

	def ejemplo_cambia_texto_en_button(self):
		import random
		cambios = ["tipo", "tamanio", "color", "texto"]
		modificar = random.choice(cambios)
		if modificar == "tipo":
			tipos= ["Arial", "Purisa", "Times New Roman", "Vardana", "Impact", pygame.font.get_default_font()]
			tipo=random.choice(tipos)
			self.widgets.sprites()[0].set_text(tipo=random.choice(tipos), tamanio=None, color=None, texto=None)
		if modificar == "tamanio":
			tamanios= [10,20,30,40,45]
			tamanio=random.choice(tamanios)
			self.widgets.sprites()[0].set_text(tipo=None, tamanio=tamanio, color=None, texto=None)
		if modificar == "color":
			colores= [(0,0,0,255), (100,100,255,255), (110,25,255,255), (255,125,55,255)]
			color = random.choice(colores)
			self.widgets.sprites()[0].set_text(tipo=None, tamanio=None, color=color, texto=None)
		if modificar == "texto":
			textos= ["JAMLabel", "Presiona escape cuando quieras salir", "Modificando Texto en JAMLabel", "CeibalJAM 2011"]
			texto = random.choice(textos)
			self.widgets.sprites()[0].set_text(tipo=None, tamanio=None, color=None, texto=texto)
		return 0

	def ejemplo_cambia_imagen_en_button(self):
		import random
		cambios = ["origen", "tamanio"]
		modificar = random.choice(cambios)
		if modificar == "tamanio":
			tamanios= [(10,20),(30,200),(250,100),None]
			tamanio=random.choice(tamanios)
			self.widgets.sprites()[0].set_imagen(origen=None, tamanio=tamanio)
		if modificar == "origen":
			origenes= [VG.get_jamimagenes()[0], VG.get_jamimagenes()[1], -1]
			origen = random.choice(origenes)
			self.widgets.sprites()[0].set_imagen(origen=origen, tamanio=None)
		return 0

	def ejemplo_cambia_colores_en_button(self):
		import random
		cambios = ["colorbas", "colorbor", "colorcara"]
		modificar = random.choice(cambios)

		colores= [(10,20,100,255), (100,100,100,255), (255,255,255,255), (255,0,0,255)]
		color=random.choice(colores)

		if modificar == "colorbas":
			self.widgets.sprites()[0].set_colores(colorbas=color, colorbor=None, colorcara=None)
		if modificar == "colorbor":
			self.widgets.sprites()[0].set_colores(colorbas=None, colorbor=color, colorcara=None)
		if modificar == "colorcara":
			self.widgets.sprites()[0].set_colores(colorbas=None, colorbor=None, colorcara=color)
		return 0

	def ejemplo_cambia_tamanios_en_button(self):
		import random
		cambios = ["tamanio", "grosorbor", "detalle", "espesor"]
		modificar = random.choice(cambios)

		#set_tamanios(tamanio=None, grosorbor=None, detalle=None, espesor=None)
		if modificar == "tamanio":
			tamanios= [(200,100), (100,50), (20,20), (300,150), (10,500), (300,50), -1]
			tamanio = random.choice(tamanios)
			self.widgets.sprites()[0].set_tamanios(tamanio=tamanio, grosorbor=None, detalle=None, espesor=None)
		if modificar == "grosorbor":
			tamanios= [1, 5, 8, 10]
			tamanio = random.choice(tamanios)
			self.widgets.sprites()[0].set_tamanios(tamanio=None, grosorbor=tamanio, detalle=None, espesor=None)
		return 0

	def ejemplo_cambia_posicion_en_button(self):
		import random
		posiciones= [(0,0), (25,25), (25,100), (25,150)]
		posicion=random.choice(posiciones)
		self.widgets.sprites()[0].set_posicion(punto=posicion)
		return 0

	def setup(self):
		pygame.init()
		pygame.display.set_mode(self.resolucion , 0, 0)
		pygame.display.set_caption("Ejemplo")

		self.fondo = self.get_Fondo()

		self.widgets = pygame.sprite.OrderedUpdates()
		self.widgets.add(JAMButton("JAMButton Prueba", None, tipo="elipse"))

		self.ventana = pygame.display.get_surface()
		self.reloj = pygame.time.Clock()

		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN,
					KEYUP, USEREVENT, QUIT, ACTIVEEVENT])
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN, VIDEORESIZE, VIDEOEXPOSE])
		pygame.mouse.set_visible(True)

	def get_Fondo(self):
		superficie = pygame.Surface( self.resolucion, flags=HWSURFACE )
		superficie.fill(VG.get_negro())
		return superficie

	def handle_event(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				self.salir()
		pygame.event.clear()

	def salir(self, datos=None):
		pygame.quit()
		sys.exit()

if __name__ == "__main__":
	Ejemplo()
