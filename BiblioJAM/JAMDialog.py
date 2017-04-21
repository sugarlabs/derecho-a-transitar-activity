#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 18/04/2011 - CeibalJAM! - Uruguay
#   JAMDialog.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys
from pygame.locals import *
gc.enable()

import JAMGlobals as VG
from JAMLabel import JAMLabel
from JAMButton import JAMButton

class JAMDialog(pygame.sprite.OrderedUpdates):
	def __init__(self, mensaje="JAMDialog", funcion_ok=None, funcion_cancel=None):
		''' Es un grupo de sprite que contiene: JAMButton aceptar, JAMButton cancelar, Base.'''
		pygame.sprite.OrderedUpdates.__init__(self)
		self.resolucion= (1200,900)
		self.mensaje= mensaje
		self.funcion_ok= None #funcion_ok
		self.funcion_cancel= None #funcion_cancel

		self.separador= 20
		self.grosorbor_int= 3
		self.grosorbor_med= 2
		self.grosorbor_ext= 7
		
		self.colores= {"base":VG.get_blanco(), "bordes":VG.get_negro()}

		# Botones
		self.boton_aceptar, self.boton_cancelar= self.get_buttons()
		self.connect(funcion_ok=funcion_ok, funcion_cancel=funcion_cancel)
		# Etiqueta con mensaje
		self.label = self.get_label()
		# Base
		self.base= pygame.sprite.Sprite()
		self.base.image= self.get_base()
		self.base.rect= self.base.image.get_rect()

		self.add(self.base)
		self.add(self.boton_aceptar)
		self.add(self.boton_cancelar)

		#self.set_center()
		self.JAMObjects= {"base":self.base, "etiqueta":self.label, "botonaceptar":self.boton_aceptar, "botoncancelar": self.boton_cancelar}

		self.Reconstruye_JAMDialog(["todo"])

	# ------------ SETEOS -----------------------
	# ------ Etiqueta
	def set_text(self, tipo=None, tamanio=None, color=None, texto=None):
		''' Setea el Texto en JAMLabel. '''
		self.label.set_text(tipo=tipo, tamanio=tamanio, color=color, texto=texto)
		self.Reconstruye_JAMDialog(["texto"])

	def set_font_from_file(self, direccion_archivo, tamanio= None):
		''' Setea la fuente desde un archivo en JAMLabel. '''
		self.label.set_font_from_file(direccion_archivo, tamanio)
		self.Reconstruye_JAMDialog(["texto"])

	def set_imagen(self, origen=None, tamanio=None):
		''' Setea el Imagen en JAMLabel. '''
		self.label.set_imagen(origen=origen, tamanio=tamanio)
		self.Reconstruye_JAMDialog(["imagen"])
	# ------ Etiqueta

	# ------ Botones
	def set_text_buttons(self, tipo=None, tamanio=None, color=None, textoaceptar=None, textocancelar=None):
		''' Setea el Texto en los JAMButtons. '''
		self.boton_aceptar.set_tamanios(tamanio=(0,0))
		self.boton_cancelar.set_tamanios(tamanio=(0,0))
		self.boton_aceptar.set_text(tipo=tipo, tamanio=tamanio, color=color, texto=textoaceptar)
		self.boton_cancelar.set_text(tipo=tipo, tamanio=tamanio, color=color, texto=textocancelar)
		self.Reconstruye_JAMDialog(["tamaniosbuttons"])

	def set_colors_buttons(self, colorbas=None, colorbor=None, colorcara=None):
		''' Setea los colores de los JAMButtons. '''
		self.boton_aceptar.set_colores(colorbas=colorbas, colorbor=colorbor, colorcara=colorcara)
		self.boton_cancelar.set_colores(colorbas=colorbas, colorbor=colorbor, colorcara=colorcara)
		self.Reconstruye_JAMDialog(["colorbuttons"])
	
	def set_imagenes_buttons(self, imagenceptar=None, imagencancelar=None, tamanio=None):
		''' Setea las imágenes de los JAMButtons. '''
		self.boton_aceptar.set_tamanios(tamanio=(0,0))
		self.boton_cancelar.set_tamanios(tamanio=(0,0))
		self.boton_aceptar.set_imagen(origen=imagenceptar , tamanio=tamanio)
		self.boton_cancelar.set_imagen(origen=imagencancelar , tamanio=tamanio)
		self.Reconstruye_JAMDialog(["imagenbuttons"])

	def connect(self, funcion_ok = None, funcion_cancel = None):
		''' Conecta los Botones a Funciones. '''
		if funcion_ok != self.funcion_ok:
			self.funcion_ok = funcion_ok
			self.boton_aceptar.connect(callback = self.funcion_ok, sonido_select = None)
		if funcion_cancel != self.funcion_cancel:
			self.funcion_cancel = funcion_cancel
			self.boton_cancelar.connect(callback = self.funcion_cancel, sonido_select = None)
		if not funcion_ok or not funcion_cancel:
			self.boton_aceptar.connect(sonido_select = None)
			self.boton_cancelar.connect(sonido_select = None)
	# ------ Botones

	def set_colors_dialog(self, base=None, bordes=None):
		''' Setea los Colores del Contenedor de JAMDialog. '''
		if not base: base= VG.get_blanco()
		if not bordes: bordes= VG.get_negro()

		if base != self.colores["base"]:
			self.colores["base"]= base
		if bordes != self.colores["bordes"]:
			self.colores["bordes"]= bordes
		self.label.set_contenedor(colorbas=self.colores["base"])
		self.Reconstruye_JAMDialog(["colorsdialog"])

	def set_center(self):
		''' Centra la base y posiciona los botones. '''
		'''
		w,h= (800, 600)
		try:
			w,h= (pygame.display.Info().current_w, pygame.display.Info().current_h)
		except:
			w,h= (800, 600)'''
		
		w,h= self.resolucion
		self.base.rect.center= (w/2,h/2)
		x= self.base.rect.x+self.separador
		y= self.base.rect.y+self.base.rect.h-self.separador-self.boton_aceptar.rect.h
		self.boton_aceptar.set_posicion(punto=(x,y))
		x= self.base.rect.x+self.base.rect.w-self.separador-self.boton_cancelar.rect.w
		self.boton_cancelar.set_posicion(punto=(x,y))

	# ------------ CONSTRUCCIÓN -----------------------
	def Reconstruye_JAMDialog(self, cambios):
		self.base.image= self.get_base()
		self.base.rect= self.base.image.get_rect()
		self.set_reset_tamanios_buttons()
		self.set_center()
	
	def set_reset_tamanios_buttons(self):
		''' Los dos botones del mismo tamaño. '''
		botones= [self.boton_aceptar, self.boton_cancelar]
		for boton in botones:
			boton.set_tamanios(tamanio=(0,0))
		w,h= (0,0)
		for boton in botones:
			ww,hh= boton.get_tamanio()
			if w < ww: w= ww
			if h < hh: h= hh
		for boton in botones:
			boton.set_tamanios(tamanio=(w,h))

	def get_label(self):
		''' Construye y Devuelve JAMLabel. '''
		label= JAMLabel(self.mensaje)
		label.set_text(tipo=None, tamanio=50, color=None, texto=None)
		label.set_contenedor(colorbas=self.colores["base"], grosor=None, colorbor=None)
		return label

	def get_buttons(self):
		''' Construye y Devuelve los Botones. '''
		boton_aceptar = JAMButton ("Aceptar", None)
		boton_cancelar = JAMButton ("Cancelar", None)
		boton_aceptar.set_text(tipo=None, tamanio=30, color=None, texto=None)
		boton_cancelar.set_text(tipo=None, tamanio=30, color=None, texto=None)
		return boton_aceptar, boton_cancelar

	def get_base(self):
		''' Construye el sprite base. '''
		(a,b,c,d)= self.boton_aceptar.rect
		(aa,bb,cc,dd)= self.boton_cancelar.rect
		ancho_minimo= (c+cc+self.separador)

		(a,b,w,h)= self.label.rect
		if w < ancho_minimo: w= ancho_minimo

		# Recuadro Interior con Etiqueta
		tamanio_frame_interno= (self.grosorbor_int*2+w+self.separador*2, self.grosorbor_int*2+self.separador*2+h)
		frame1= VG.get_Rectangulo(self.colores["base"], tamanio_frame_interno)
		frame1= VG.get_my_surface_whit_border(frame1, self.colores["bordes"], self.grosorbor_int)
		frame1= VG.pegar_imagenes_centradas(self.label.image, frame1)

		ww,hh= frame1.get_size()
		# Recuadro pre-exterior con Recuadro Interior
		tamanio_frame_externo= (ww+self.separador*2, hh+self.separador*2+d)
		frame2= VG.get_Rectangulo(self.colores["base"], tamanio_frame_externo)
		frame2= VG.get_my_surface_whit_border(frame2, self.colores["bordes"], self.grosorbor_med)
		frame2.blit(frame1, (self.separador, self.separador))

		ww,hh= frame2.get_size()
		# Recuadro exterior - imagen final de la base
		tamanio_frame_externo= (ww+self.grosorbor_ext*3,hh+self.grosorbor_ext*3)
		base= VG.get_Rectangulo(self.colores["base"], tamanio_frame_externo)
		base= VG.get_my_surface_whit_border(base, self.colores["bordes"], self.grosorbor_ext)
		base= VG.pegar_imagenes_centradas(frame2, base)
		return base

	def Describe(self):
		''' Describe la Estructura de Este Control. '''
		estructura = '''
		Estructura JAMDialog:

			JAMObject:
				Base
				Etiqueta
				Boton Aceptar
				Boton Cancelar

		Detalle Estructural:
				Base: es una imagen construida en tiempo de ejecución sobre la cual se pega la imagen de la etiqueta
				Etiqueta: JAMLabel con el texto del mensaje
				Boton Aceptar: JAMButton para detectar evento click y responder con la función asignada mediante connect
				Boton Cancelar: JAMButton para detectar evento click y responder con la función asignada mediante connect '''

		print estructura, "\n"
		print "Ejemplo, Configuración actual:\n"
		print "\t", self.JAMObjects.keys(), "\n"
		for k in self.JAMObjects.items():
			print k, "\n"

# ----- FIN DE CLASE JAMDialog - INICIO DE DEBUG Y EJEMPLO DE LA CLASE -----
class Ejemplo(object):
	def __init__(self):
		self.ventana = None
		self.reloj = None
		self.nivel = "menu_0"

		self.fondo = None
		self.widgets = None

		self.resolucion = (1000,800)

		self.setup()
		self.Run()

	def setup(self):
		pygame.init()
		pygame.display.set_mode(self.resolucion , 0, 0)
		pygame.display.set_caption("Ejemplo")

		self.fondo = self.get_Fondo()

		self.widgets = JAMDialog(mensaje="Prueba JAMDialog", funcion_ok=None, funcion_cancel=None)
		self.widgets.connect(funcion_ok=self.salir, funcion_cancel=self.salir)

		self.ventana = pygame.display.get_surface()
		self.reloj = pygame.time.Clock()

		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN,
					KEYUP, USEREVENT, QUIT, ACTIVEEVENT])
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN, VIDEORESIZE, VIDEOEXPOSE])
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
			if contador == 150:
				# Activa la siguiente línea para provocar cambios de texto en JAMLabel
				contador= self.ejemplo_cambia_texto_en_Dialog()
				# Activa la siguiente línea para provocar cambios de imagen en JAMLabel
				contador= self.ejemplo_cambia_imagen_en_Dialog()
				# Activa la siguiente línea para provocar cambios de contenedor en JAMLabel
				contador= self.ejemplo_cambia_colors_Dialog()

				# Activa la siguiente línea para provocar cambios de texto en Botones
				contador= self.ejemplo_cambia_texto_en_Buttons()
				# Activa la siguiente línea para provocar cambios de imagen en Botones
				contador= self.ejemplo_cambia_imagen_en_Buttons()
				# Activa la siguiente línea para provocar cambios de color en los botones
				contador= self.ejemplo_cambia_colors_Buttons()
				pass

			self.widgets.update()
			self.handle_event()
			pygame.event.clear()
			cambios.extend ( self.widgets.draw(self.ventana) )
			pygame.display.update(cambios)
			contador += 1

	def ejemplo_cambia_texto_en_Dialog(self):
		import random
		cambios = ["tipo", "tamanio", "color", "texto"]
		modificar = random.choice(cambios)
		if modificar == "tipo":
			tipos= ["Arial", "Purisa", "Times New Roman", "Vardana", "Impact", pygame.font.get_default_font()]
			tipo=random.choice(tipos)
			self.widgets.set_text(tipo=random.choice(tipos), tamanio=None, color=None, texto=None)
		if modificar == "tamanio":
			tamanios= [10,20,30,40,45]
			tamanio=random.choice(tamanios)
			self.widgets.set_text(tipo=None, tamanio=tamanio, color=None, texto=None)
		if modificar == "color":
			colores= [(0,0,0,255), (100,100,255,255), (110,25,255,255), (255,125,55,255)]
			color = random.choice(colores)
			self.widgets.set_text(tipo=None, tamanio=None, color=color, texto=None)
		if modificar == "texto":
			textos= ["JAMLabel", "Presiona escape cuando quieras salir", "Modificando Texto en JAMLabel", "CeibalJAM 2011"]
			texto = random.choice(textos)
			self.widgets.set_text(tipo=None, tamanio=None, color=None, texto=texto)
		return 0

	def ejemplo_cambia_imagen_en_Dialog(self):
		import random
		cambios = ["origen", "tamanio"]
		modificar = random.choice(cambios)
		if modificar == "tamanio":
			tamanios= [(10,20),(30,200),(250,100)]
			tamanio=random.choice(tamanios)
			self.widgets.set_imagen(origen=None, tamanio=tamanio)
		if modificar == "origen":
			origenes= [VG.get_jamimagenes()[0], VG.get_jamimagenes()[1], -1]
			origen = random.choice(origenes)
			self.widgets.set_imagen(origen=origen, tamanio=None)
		return 0

	def ejemplo_cambia_colors_Dialog(self):
		import random
		cambios = ["colorbas", "colorbor"]
		modificar = random.choice(cambios)

		colores= [(10,20,100,255), (128,128,128,255), (255,255,255,255)]
		color=random.choice(colores)

		if modificar == "colorbor":
			self.widgets.set_colors_dialog(base=None, bordes=color)
		if modificar == "colorbas":
			self.widgets.set_colors_dialog(base=color, bordes=None)
		return 0

	def ejemplo_cambia_colors_Buttons(self):
		import random
		cambios = ["colorbas", "colorbor", "colorcara"]
		modificar = random.choice(cambios)

		colores= [(10,20,100,255), (128,128,128,255), (255,255,255,255)]
		color=random.choice(colores)

		if modificar == "colorbor":
			self.widgets.set_colors_buttons(colorbas=None, colorbor=color, colorcara=None)
		if modificar == "colorbas":
			self.widgets.set_colors_buttons(colorbas=color, colorbor=None, colorcara=None)
		if modificar == "colorcara":
			self.widgets.set_colors_buttons(colorbas=None, colorbor=None, colorcara=color)
		return 0

	def ejemplo_cambia_texto_en_Buttons(self):
		import random
		cambios = ["tipo", "tamanio", "color", "texto"]
		modificar = random.choice(cambios)
		if modificar == "tipo":
			tipos= ["Arial", "Purisa", "Times New Roman", "Vardana", "Impact", pygame.font.get_default_font()]
			tipo=random.choice(tipos)
			self.widgets.set_text_buttons(tipo=tipo)
		if modificar == "tamanio":
			tamanios= [10,20,30,40,45]
			tamanio=random.choice(tamanios)
			self.widgets.set_text_buttons(tamanio=tamanio)
		if modificar == "color":
			colores= [(0,0,0,255), (100,100,255,255), (110,25,255,255), (255,125,55,255)]
			color = random.choice(colores)
			self.widgets.set_text_buttons(color=color)
		if modificar == "texto":
			textos= ["JAMLabel", "Presiona escape cuando quieras salir", "Modificando Texto en JAMLabel", "CeibalJAM 2011"]
			texto = random.choice(textos)
			self.widgets.set_text_buttons(textoaceptar=texto, textocancelar=texto)
		return 0

	def ejemplo_cambia_imagen_en_Buttons(self):
		import random
		cambios = ["origen", "tamanio"]
		modificar = random.choice(cambios)
		if modificar == "tamanio":
			tamanios= [(10,20),(30,200),(250,100)]
			tamanio=random.choice(tamanios)
			self.widgets.set_imagenes_buttons(imagenceptar=None, imagencancelar=None, tamanio=tamanio)
		if modificar == "origen":
			origenes= [VG.get_jamimagenes()[0], VG.get_jamimagenes()[1], -1]
			origen = random.choice(origenes)
			self.widgets.set_imagenes_buttons(imagenceptar=origen, imagencancelar=origen, tamanio=None)
		return 0

	def get_Fondo(self):
		superficie = pygame.Surface( self.resolucion, flags=HWSURFACE )
		superficie.fill((128,128,128,255))
		return superficie

	def handle_event(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				self.salir()
		pygame.event.clear()

	def salir(self):
		print "\n"
		self.widgets.Describe()
		pygame.quit()
		sys.exit()



if __name__ == "__main__":
	Ejemplo()
