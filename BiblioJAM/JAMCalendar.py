#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 28/05/2011 - CeibalJAM! - Uruguay
#   JAMCalendar.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys, gobject, time, datetime, os
from pygame.locals import *
gc.enable()
pygame.font.init()

import JAMGlobals as VG
from JAMButton import JAMButton
from JAMLabel import JAMLabel

class JAMCalendar(pygame.sprite.OrderedUpdates):
	''' Un Calendario hecho en pygame. '''
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)

		COLORCARA, COLORBAS, COLORBOR, GROSORBOR, DETALLE, ESPESOR= VG.get_default_jambutton_values()

		self.datos_fechas_text={"tipo": pygame.font.get_default_font(), "tamanio": 16, "color": VG.get_negro(), "font_from_file": False}
		self.datos_fechas_color={"colorselect": COLORBAS, "colorcara": COLORCARA, "colorborde": COLORBOR}

		self.datos_dias_text={"tipo": pygame.font.get_default_font(), "tamanio": 16, "color": VG.get_negro(), "font_from_file": False}
		self.datos_dias_color={"colorselect": COLORBAS, "colorcara": COLORCARA, "colorborde": COLORBOR}

		self.datos_cabecera_text={"tipo": pygame.font.get_default_font(), "tamanio": 16, "color": VG.get_negro(), "font_from_file": False}
		self.datos_cabecera_color={"colorselect": COLORBAS, "colorcara": COLORCARA, "colorborde": COLORBOR}

		self.datos_base= {"colorborde": COLORBOR, "colorbase": COLORBAS, "retiro1": 2, "grosorborde1": 4,"retiro2": 1, "grosorborde2": 2}

		self.posicion= (0,0)

		self.anio, self.mes, self.dia= str(datetime.date.today()).split("-") # el dia de hoy

		self.botones_fechas= None
		self.botones_dias= None
		self.cabecera= None
		self.base= None

		self.color_hoy= None
		self.Reconstruye("todo")

	def Reconstruye(self, cambios):
		''' Reconstruye el calendario según cambios.'''
		if "todo" in cambios:
			self.empty()
			datos_calendar= VG.get_calendar(int(self.mes), int(self.anio))
			self.color_hoy= VG.get_blanco()

			self.cabecera= Cabecera(self, datos_calendar[0])
			self.botones_dias= Botones_Dias(self, datos_calendar[1])
			self.botones_fechas= Botones_Fechas(self, datos_calendar[2:])
			self.reset_tamanios()
			self.base= self.get_base()
			self.set_posicion(punto= self.posicion)

			self.add(self.base)
			self.add(self.cabecera)
			self.add(self.botones_dias)
			self.add(self.botones_fechas)

	def reset_tamanios(self):
		''' Setea el tamanio de los botones de acuerdo al tamanio de la letra. '''
		# Botones de dias y fechas
		botones= self.botones_dias.sprites()
		botones.extend(self.botones_fechas.sprites())
		lado= 0
		for boton in botones:
			boton.set_tamanios(tamanio=(0,0), grosorbor=1, detalle=1, espesor=1)
			w,h = boton.get_tamanio()
			if w > lado: lado= w
			if h > lado: lado= h
		for boton in botones:
			boton.set_tamanios(tamanio=(lado,lado), grosorbor=1, detalle=1, espesor=1)

		# Botones de la Cabecera
		ancho_cabecera= lado*7+6
		botones_cabecera= self.cabecera.sprites()
		for boton in botones_cabecera:
			boton.set_tamanios(tamanio=(0,0), grosorbor=1, detalle=1, espesor=1)
			w,h = boton.get_tamanio()
			#if w > lado: lado= w
			if h > lado: lado= h
		botones_cabecera[0].set_tamanios(tamanio=(h,h), grosorbor=1, detalle=1, espesor=1)
		a,b= botones_cabecera[0].get_tamanio()
		botones_cabecera[1].set_tamanios(tamanio=(ancho_cabecera-a*2,h), grosorbor=1, detalle=1, espesor=1)
		botones_cabecera[2].set_tamanios(tamanio=(h,h), grosorbor=1, detalle=1, espesor=1)
		
	def get_base(self):
		''' Construye la base del Calendario. '''
		altura_total= 0
		ancho_total= 0

		colorborde= self.datos_base["colorborde"]
		colorbase= self.datos_base["colorbase"]
		retiro1= self.datos_base["retiro1"]
		grosorborde1= self.datos_base["grosorborde1"]
		retiro2= self.datos_base["retiro2"]
		grosorborde2= self.datos_base["grosorborde2"]

		margen1= retiro2+grosorborde2
		margen2= retiro1+grosorborde1
		# Cabecera
		ancho_cabecera= 0
		for boton in self.cabecera.sprites():
			w,h= boton.get_tamanio()
			ancho_cabecera+= w
		altura_cabecera= h

		ancho_total= margen1*2 + ancho_cabecera
		altura_total= margen1*2 + altura_cabecera
		
		# dias
		w,altura_dias= self.botones_dias.sprites()[0].get_tamanio()

		altura_total+= altura_dias+1

		# fechas
		altura_total+= altura_dias*5+5

		rectangulo_interno= (ancho_total, altura_total)
		rectangulo_externo= (ancho_total+margen2*2, altura_total+margen2*2)

		base= pygame.sprite.Sprite()
		base.image= VG.get_Rectangulo(colorbase, (rectangulo_interno))
		base.image= VG.get_my_surface_whit_border(base.image, colorborde, grosorborde2)

		fondo= VG.get_Rectangulo(colorbase, (rectangulo_externo))
		fondo= VG.get_my_surface_whit_border(fondo, colorborde, grosorborde1)
		base.image= VG.pegar_imagenes_centradas(base.image, fondo)
		base.rect= base.image.get_rect()
		return base
	# ------------------ Gets ---------------------------
	def get_posicion(self):
		x,y,w,h= self.get_rect()
		return (x,y)
	def get_tamanio(self):
		x,y,w,h= self.get_rect()
		return (w,h)
	def get_rect(self):
		return self.base.rect
	# ------------------ Gets ---------------------------

	# ------------------ Seteos Externos ------------------
	# -----------------SETEOS Que afectan al tamaño -------------------
	def set_text_fechas(self, tipo= False, tamanio= False, color= False):
		''' Setea tipo, tamaño y color de la letra en los botones de fecha. '''
		cambios= False
		if tipo: 
			self.datos_fechas_text["tipo"]= tipo
			cambios= True
		if tamanio: 
			self.datos_fechas_text["tamanio"]= tamanio
			cambios= True
		if color: 
			self.datos_fechas_text["color"]= color
			cambios= True

		if cambios:
			self.botones_fechas.set_text()
			if tamanio:
				self.empty()
				self.reset_tamanios()
				self.base= self.get_base()
				self.set_posicion(punto= self.posicion)
				self.add(self.base)
				self.add(self.cabecera)
				self.add(self.botones_dias)
				self.add(self.botones_fechas)

	def set_font_from_file_fechas(self, fuente, tamanio= None):
		''' Setea el tipo de letra desde un archivo de fuentes. '''
		cambios= False
		if fuente:
			self.datos_fechas_text["font_from_file"]= fuente
			cambios= True
		if tamanio: 
			self.datos_fechas_text["tamanio"]= tamanio
			cambios= True

		if cambios:
			self.botones_fechas.set_text()
			if tamanio:
				self.empty()
				self.reset_tamanios()
				self.base= self.get_base()
				self.set_posicion(punto= self.posicion)
				self.add(self.base)
				self.add(self.cabecera)
				self.add(self.botones_dias)
				self.add(self.botones_fechas)

	def set_text_dias(self, tipo= False, tamanio= False, color= False):
		''' Setea tipo, tamaño y color de la letra en los botones de dias. '''
		cambios= False
		if tipo: 
			self.datos_dias_text["tipo"]= tipo
			cambios= True
		if tamanio: 
			self.datos_dias_text["tamanio"]= tamanio
			cambios= True
		if color: 
			self.datos_dias_text["color"]= color
			cambios= True

		if cambios:
			self.botones_dias.set_text()
			if tamanio:
				self.empty()
				self.reset_tamanios()
				self.base= self.get_base()
				self.set_posicion(punto= self.posicion)
				self.add(self.base)
				self.add(self.cabecera)
				self.add(self.botones_dias)
				self.add(self.botones_fechas)

	def set_font_from_file_dias(self, fuente, tamanio= None):
		''' Setea el tipo de letra desde un archivo de fuentes. '''
		cambios= False
		if fuente:
			self.datos_dias_text["font_from_file"]= fuente
			cambios= True
		if tamanio: 
			self.datos_dias_text["tamanio"]= tamanio
			cambios= True

		if cambios:
			self.botones_dias.set_text()
			if tamanio:
				self.empty()
				self.reset_tamanios()
				self.base= self.get_base()
				self.set_posicion(punto= self.posicion)
				self.add(self.base)
				self.add(self.cabecera)
				self.add(self.botones_dias)
				self.add(self.botones_fechas)


	def set_text_cabecera(self, tipo= False, tamanio= False, color= False):
		''' Setea tipo, tamaño y color de la letra en los botones de dias. '''
		cambios= False
		if tipo: 
			self.datos_cabecera_text["tipo"]= tipo
			cambios= True
		if tamanio: 
			self.datos_cabecera_text["tamanio"]= tamanio
			cambios= True
		if color: 
			self.datos_cabecera_text["color"]= color
			cambios= True

		if cambios:
			self.cabecera.set_text()
			if tamanio:
				self.empty()
				self.reset_tamanios()
				self.base= self.get_base()
				self.set_posicion(punto= self.posicion)
				self.add(self.base)
				self.add(self.cabecera)
				self.add(self.botones_dias)
				self.add(self.botones_fechas)

	def set_font_from_file_cabecera(self, fuente, tamanio= None):
		''' Setea el tipo de letra desde un archivo de fuentes. '''
		cambios= False
		if fuente:
			self.datos_cabecera_text["font_from_file"]= fuente
			cambios= True
		if tamanio: 
			self.datos_cabecera_text["tamanio"]= tamanio
			cambios= True

		if cambios:
			self.cabecera.set_text()
			if tamanio:
				self.empty()
				self.reset_tamanios()
				self.base= self.get_base()
				self.set_posicion(punto= self.posicion)
				self.add(self.base)
				self.add(self.cabecera)
				self.add(self.botones_dias)
				self.add(self.botones_fechas)

	def set_text(self, tipo= False, tamanio= False, color= False):
		''' Setea tipo, tamaño y color de la letra en los botones de dias. '''
		self.set_text_fechas(tipo= tipo, tamanio= tamanio, color= color)
		self.set_text_dias(tipo= tipo, tamanio= tamanio, color= color)
		self.set_text_cabecera(tipo= tipo, tamanio= tamanio, color= color)

	def set_font_from_file(self, fuente, tamanio= None):
		''' Setea el tipo de letra desde un archivo de fuentes. '''
		self.set_font_from_file_fechas(fuente, tamanio= tamanio)
		self.set_font_from_file_dias(fuente, tamanio= tamanio)
		self.set_font_from_file_cabecera(fuente, tamanio= tamanio)
	# -----------------SETEOS Que afectan al tamaño -------------------

	# -----------------SETEOS Que no afectan al tamaño -------------------
	def set_posicion(self, punto= (0,0)):
		if type(punto)== tuple and len(punto)== 2:
			if type(punto[0])== int and type(punto[1])== int: 
				retiro1= self.datos_base["retiro1"]
				grosorborde1= self.datos_base["grosorborde1"]
				retiro2= self.datos_base["retiro2"]
				grosorborde2= self.datos_base["grosorborde2"]

				self.posicion= punto
				# base
				self.base.rect.x, self.base.rect.y= self.posicion

				margen1= retiro2+grosorborde2
				margen2= retiro1+grosorborde1

				# cabecera
				posicion= (self.posicion[0]+margen1+margen2,self.posicion[1]+margen1+margen2)
				self.cabecera.set_posicion(punto= posicion)

				x,y= posicion
				w,h= self.cabecera.matriz_botones[0].get_tamanio()

				# dias
				posicion= (x, y+h+1)
				self.botones_dias.set_posicion(punto= posicion)

				x,y= posicion
				w,h= self.botones_dias.matriz_botones[0].get_tamanio()

				# fechas
				posicion= (x, y+h+1)
				self.botones_fechas.set_posicion(punto= posicion)

	def set_calendar(self, mes, anio):
		''' Cuando se cambia el mes o año. '''
		if not type(mes)== int or not type(anio)== int or mes not in range(1,13) or not anio > 0: return
		self.mes, self.anio= (mes, anio)
		datos_calendar= VG.get_calendar(int(self.mes), int(self.anio))
		self.botones_fechas.set_mes(datos_calendar[2:])
		self.cabecera.set_mes(datos_calendar[0])

	def set_colors_fechas(self, colorselect= False, colorbor= False, colorcara= False):
		''' Setea los colores de los botones de fecha. '''
		cambios= False
		if colorselect:
			self.datos_fechas_color["colorselect"]= colorselect
			cambios= True
		if colorbor:
			self.datos_fechas_color["colorborde"]= colorbor
			cambios= True
		if colorcara:
			self.datos_fechas_color["colorcara"]= colorcara
			cambios= True
		if cambios:self.botones_fechas.set_colors()

	def set_colors_dias(self, colorselect= False, colorbor= False, colorcara= False):
		''' Setea los colores de los botones de fecha. '''
		cambios= False
		if colorselect:
			self.datos_dias_color["colorselect"]= colorselect
			cambios= True
		if colorbor:
			self.datos_dias_color["colorborde"]= colorbor
			cambios= True
		if colorcara:
			self.datos_dias_color["colorcara"]= colorcara
			cambios= True
		if cambios:self.botones_dias.set_colors()

	def set_colors_cabecera(self, colorselect= False, colorbor= False, colorcara= False):
		''' Setea los colores de los botones de fecha. '''
		cambios= False
		if colorselect:
			self.datos_cabecera_color["colorselect"]= colorselect
			cambios= True
		if colorbor:
			self.datos_cabecera_color["colorborde"]= colorbor
			cambios= True
		if colorcara:
			self.datos_cabecera_color["colorcara"]= colorcara
			cambios= True
		if cambios:self.cabecera.set_colors()

	def set_colors_base(self, colorbase= False, colorborde= False):
		''' Setea los colores de la base. '''
		cambios= False
		if colorbase:
			if colorbase != self.datos_base["colorbase"]:
				self.datos_base["colorbase"]= colorbase
				cambios= True
		if colorborde:
			if colorborde != self.datos_base["colorborde"]:
				self.datos_base["colorborde"]= colorborde
				cambios= True
		if cambios:
			self.empty()
			self.base= self.get_base()
			self.set_posicion(punto= self.posicion)
			self.add(self.base)
			self.add(self.cabecera)
			self.add(self.botones_dias)
			self.add(self.botones_fechas)

	def set_gama_colors(self, colorselect= False, colorbor= False, colorcara= False):
		''' Setea los colores de la base. '''
		cambios= False
		if colorselect:
			self.datos_cabecera_color["colorselect"]= colorselect
			self.datos_dias_color["colorselect"]= colorselect
			self.datos_fechas_color["colorselect"]= colorselect
			self.datos_base["colorbase"]= colorselect
			cambios= True
		if colorbor:
			self.datos_cabecera_color["colorborde"]= colorbor
			self.datos_dias_color["colorborde"]= colorbor
			self.datos_fechas_color["colorborde"]= colorbor
			self.datos_base["colorborde"]= colorbor
			cambios= True
		if colorcara:
			self.datos_cabecera_color["colorcara"]= colorcara
			self.datos_dias_color["colorcara"]= colorcara
			self.datos_fechas_color["colorcara"]= colorcara
			cambios= True
		if cambios:
			self.empty()
			self.cabecera.set_colors()
			self.botones_dias.set_colors()
			self.botones_fechas.set_colors()
			self.base= self.get_base()
			self.set_posicion(punto= self.posicion)
			self.add(self.base)
			self.add(self.cabecera)
			self.add(self.botones_dias)
			self.add(self.botones_fechas)
	# -----------------SETEOS Que no afectan al tamaño -------------------

class Botones_Fechas(pygame.sprite.OrderedUpdates):
	''' Botones para fechas. '''
	def __init__(self, calendar, datos_calendar):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.calendar= calendar
		self.datos_calendar= datos_calendar

		self.matriz_botones= []
		self.posicion=(0,0)

		self.Reconstruye(["todo"])

	def Reconstruye(self, cambios):
		''' Reconstruye el objeto según cambios.'''
		if "todo" in cambios:
			self.empty()
			self.insert_empty_value_in_datos_calendar()	# Inserta elementos vacíos para emparejar con la matriz de botones.
			self.get_matriz_botones()			# Genera la matriz de botones de fechas.
			self.set_text()					# Seteos de texto en botones.
			self.set_colors()				# Setea los colores de los botones.
			self.add(self.matriz_botones)

	def get_matriz_botones(self):
		''' Genera la matriz de botones de fechas. '''
		self.matriz_botones= []
		for x in range(5):
			linea= []
			for y in range(7):
				boton= JAMButton("", None)
				boton.connect(callback= None, sonido_select= None)
				linea.append(boton)
			self.matriz_botones.append(linea)

	def insert_empty_value_in_datos_calendar(self):
		''' Inserta elementos vacíos para emparejar con la matriz de botones. '''
		while len(self.datos_calendar[0]) < 7:
			self.datos_calendar[0].insert(0, " ")
		while len(self.datos_calendar[-1]) < 7:
			self.datos_calendar[-1].append(" ")

	# -------------- SETEOS (todos internos) ----------------
	def set_mes(self, datos_calendar):
		''' Setea el mes en el calendario. '''
		self.datos_calendar= datos_calendar
		self.insert_empty_value_in_datos_calendar()
		self.set_text()
		self.set_colors()

	def set_text(self):
		''' Seteos de texto en botones. '''
		tipo= self.calendar.datos_fechas_text["tipo"]
		tamanio= self.calendar.datos_fechas_text["tamanio"]
		color= self.calendar.datos_fechas_text["color"]
		fuente= self.calendar.datos_fechas_text["font_from_file"]

		for linea in self.matriz_botones:
			indicea= self.matriz_botones.index(linea)
			for boton in linea:
				indiceb= linea.index(boton)
				try:
					texto= self.datos_calendar[indicea][indiceb]
				except:
					texto= " "
				#if texto== " ":
				#	linea[indiceb]= ButtonLabel(" ")
				boton.set_text(tipo=tipo, tamanio=tamanio, color=color, texto=texto)
				if fuente:
					boton.set_font_from_file(fuente, tamanio= tamanio)

	def set_colors(self):
		''' Setea los colores de los botones. '''
		colorbas= self.calendar.datos_fechas_color["colorselect"]
		colorbor= self.calendar.datos_fechas_color["colorborde"]
		colorcara= self.calendar.datos_fechas_color["colorcara"]
		for linea in self.matriz_botones:
			for boton in linea:
				boton.set_colores(colorbas=colorbas, colorbor=colorbor, colorcara=colorcara)
				self.control_select_hoy(boton)

	def control_select_hoy(self, boton):
		''' Pinta la fecha de hoy. '''
		anio, mes, dia= str(datetime.date.today()).split("-")
		try:
			if int(boton.get_text()) == int(dia):
				if int(anio) == int(self.calendar.anio) and int(mes)== int(self.calendar.mes):
					colorbas= self.calendar.datos_fechas_color["colorselect"]
					colorbor= self.calendar.datos_fechas_color["colorborde"]
					colorcara= self.calendar.color_hoy
					boton.set_colores(colorbas=colorbas, colorbor=colorbor, colorcara=colorcara)
					return
		except:
			pass

	def set_posicion(self, punto= (0,0)):
		if type(punto)== tuple and len(punto)== 2:
			if type(punto[0])== int and type(punto[1])== int: 
				self.posicion= punto
				x,y = self.posicion
				yy= y
				for linea in self.matriz_botones:
					xx= x
					for boton in linea:
						boton.set_posicion(punto=(xx,yy))
						w,h = boton.get_tamanio()
						xx+= w+1
					yy+= h+1

class Botones_Dias(pygame.sprite.OrderedUpdates):
	''' Botones para días. '''
	def __init__(self, calendar, datos_calendar):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.calendar= calendar
		self.datos_calendar= datos_calendar

		self.matriz_botones= []
		self.posicion=(0,0)

		self.Reconstruye(["todo"])

	def Reconstruye(self, cambios):
		''' Reconstruye el objeto según cambios.'''
		if "todo" in cambios:
			self.empty()
			self.get_matriz_botones()
			self.set_text()
			self.add(self.matriz_botones)

	def get_matriz_botones(self):
		''' Genera la matriz de botones de fechas. '''
		self.matriz_botones= []
		for dia in self.datos_calendar:
			boton= ButtonLabel(dia)
			boton.connect(callback= None, sonido_select= None)
			self.matriz_botones.append(boton)

	def set_text(self):
		''' Seteos de texto en botones. '''
		tipo= self.calendar.datos_dias_text["tipo"]
		tamanio= self.calendar.datos_dias_text["tamanio"]
		color= self.calendar.datos_dias_text["color"]
		fuente= self.calendar.datos_dias_text["font_from_file"]

		for boton in self.matriz_botones:
			boton.set_text(tipo=tipo, tamanio=tamanio, color=color)
			if fuente:
				boton.set_font_from_file(fuente, tamanio= tamanio)

	def set_posicion(self, punto= (0,0)):
		''' Setea la posición de todos los botones. '''
		if type(punto)== tuple and len(punto)== 2:
			if type(punto[0])== int and type(punto[1])== int: 
				self.posicion= punto
				x,y= self.posicion
				for boton in self.matriz_botones:
					boton.set_posicion(punto= (x,y))
					w,h= boton.get_tamanio()
					x+= w+1
	
	def set_colors(self):
		''' Setea los colores de los botones. '''
		colorbas= self.calendar.datos_dias_color["colorselect"]
		colorbor= self.calendar.datos_dias_color["colorborde"]
		colorcara= self.calendar.datos_dias_color["colorcara"]
		for boton in self.matriz_botones:
			boton.set_colores(colorbas=colorbas, colorbor=colorbor, colorcara=colorcara)


class Cabecera(pygame.sprite.OrderedUpdates):
	''' Cabecera con boton previous, next y etiqueta con mes y año. '''
	def __init__(self, calendar, datos_calendar):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.calendar= calendar
		self.datos_calendar= datos_calendar

		self.matriz_botones= []
		self.boton_previous= None
		self.label_calendar= None
		self.boton_next= None

		self.posicion=(0,0)

		self.Reconstruye(["todo"])

	def Reconstruye(self, cambios):
		''' Reconstruye el objeto según cambios.'''
		if "todo" in cambios:
			self.empty()
			self.get_matriz_botones()
			self.set_text()
			self.add(self.matriz_botones)

	def set_mes(self, datos_calendar):
		''' Cambia la cabecera del calendario. '''
		self.datos_calendar= datos_calendar
		self.label_calendar.set_text(texto= self.datos_calendar)

	def get_previous_mes(self, boton=None):
		''' Cambia el calendario al mes anterior.'''
		mes= int(self.calendar.mes)
		anio= int(self.calendar.anio)
		if mes > 1:
			mes-= 1
		else:
			mes= 12
			anio= self.get_previous_anio()
		self.calendar.set_calendar(mes, anio)

	def get_previous_anio(self):
		''' Baja un año. '''
		anio= int(self.calendar.anio)
		if anio > 1:
			anio-= 1
		else:
			anio= 2100
		return anio

	def get_next_mes(self, boton=None):
		''' Cambia el calendario al mes siguiente.'''
		mes= int(self.calendar.mes)
		anio= int(self.calendar.anio)
		if mes < 12:
			mes+= 1
		else:
			mes= 1
			anio+= 1
		self.calendar.set_calendar(mes, anio)

	def get_matriz_botones(self):
		''' Genera la matriz de botones de fechas. '''
		self.matriz_botones= []

		self.boton_previous= JAMButton("<<", None)
		self.matriz_botones.append(self.boton_previous)
		self.boton_previous.connect(callback= self.get_previous_mes, sonido_select= None)

		self.label_calendar= ButtonLabel(self.datos_calendar)
		self.matriz_botones.append(self.label_calendar)
		self.label_calendar.connect(callback= None, sonido_select= None)

		self.boton_next= JAMButton(">>", None)
		self.matriz_botones.append(self.boton_next)
		self.boton_next.connect(callback= self.get_next_mes, sonido_select= None) 

	def set_text(self):
		''' Seteos de texto en botones. '''
		tipo= self.calendar.datos_cabecera_text["tipo"]
		tamanio= self.calendar.datos_cabecera_text["tamanio"]
		color= self.calendar.datos_cabecera_text["color"]
		fuente= self.calendar.datos_cabecera_text["font_from_file"]

		for boton in self.matriz_botones:
			boton.set_text(tipo=tipo, tamanio=tamanio, color=color)
			if fuente:
				boton.set_font_from_file(fuente, tamanio= tamanio)

	def set_posicion(self, punto= (0,0)):
		''' Setea la posición de todos los botones. '''
		if type(punto)== tuple and len(punto)== 2:
			if type(punto[0])== int and type(punto[1])== int: 
				self.posicion= punto
				x,y= self.posicion
				self.boton_previous.set_posicion(punto= (x,y))
				w,h= self.boton_previous.get_tamanio()
				x+= w
				self.label_calendar.set_posicion(punto= (x,y))
				w,h= self.label_calendar.get_tamanio()
				x+= w
				self.boton_next.set_posicion(punto= (x,y))

	def set_colors(self):
		''' Setea los colores de los botones. '''
		colorbas= self.calendar.datos_cabecera_color["colorselect"]
		colorbor= self.calendar.datos_cabecera_color["colorborde"]
		colorcara= self.calendar.datos_cabecera_color["colorcara"]
		for boton in self.matriz_botones:
			boton.set_colores(colorbas=colorbas, colorbor=colorbor, colorcara=colorcara)

class ButtonLabel(JAMButton):
	''' Etiqueta con la fecha. '''
	def __init__(self, texto):
		JAMButton.__init__(self, texto, None)

	def update(self):
		pass
	




# ----- FIN DE CLASE JAMCalendar - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
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
		self.widgets = JAMCalendar()
		#self.widgets.set_posicion(punto= (50,50))
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
		mes= 0
		contador= 0
		while self.nivel == "menu_0":
			self.reloj.tick(35)
	
			cambios=[]
			self.widgets.clear(self.ventana, self.fondo)

			self.widgets.update()
			self.handle_event()

			if contador== 100:
				self.widgets.set_text_fechas(tamanio= 50, color= (0,0,0,255))
				self.widgets.set_text_dias(tamanio= 50, color= (0,0,0,255))
				self.widgets.set_text_cabecera(tamanio= 50, color= (0,0,0,255))
				a,b,c= VG.get_estilo_naranja()
				#self.widgets.set_colors_base(colorbase= b, colorborde= a)
				self.widgets.set_gama_colors(colorselect= b, colorbor= a, colorcara= c)
				#self.widgets.set_colors_dias(colorselect= b, colorbor= a, colorcara= c)
				#self.widgets.set_colors_cabecera(colorselect= b, colorbor= a, colorcara= c)
				#fuente, tamanio= VG.get_Font_KOMIKND()
				#self.widgets.set_font_from_file_cabecera(fuente, tamanio= 15)
				#self.widgets.set_calendar(6, 2012)
				self.widgets.set_posicion(punto= (50,50))
			contador += 1

			pygame.event.clear()
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
					self.salir()
		pygame.event.clear()

	def salir(self):
		pygame.quit()
		sys.exit()

if __name__ == "__main__":
	Ejemplo()
