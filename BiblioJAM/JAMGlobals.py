#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BiblioJAM (Versión 2.0) - 16/04/2011 - CeibalJAM! - Uruguay
#   JAMGlobals.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys, os, platform
from pygame.locals import *
gc.enable()

'''
if "olpc" in platform.platform():
	os.environ['SDL_AUDIODRIVER'] = 'alsa'

if not pygame.mixer.get_init():
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.mixer.init(44100, -16, 2, 2048)'''

#pygame.init()

DIRECTORIO_BIBLIOJAM= os.path.dirname(__file__)

# fuentes
def get_Font_fawn():
	return (DIRECTORIO_BIBLIOJAM + "/Recursos/Fuentes/fawn.ttf", 43)
def get_Font_KOMIKND():
	return (DIRECTORIO_BIBLIOJAM + "/Recursos/Fuentes/KOMIKND.ttf", 43)

# COLORES
def get_magenta():
	return (255, 0, 255, 255)
def get_blanco():
	return (255,255,255,255)
def get_negro():
	return (0,0,0,255)
def get_gris1():
	return (128,128,128,255)
def get_naranja1():
	return (240,150,0,255)
def get_celeste1():
	return (0,240,240,255)
def get_celeste_pastel_claro1():
	return (220,255,255,255)
def get_celeste_cielo1():
	return (51,121,183,255)
def get_celeste_cielo2():
	return (37,115,177,255)
def get_celeste_cielo3():
	return (91,152,209,255)
def get_celeste_cielo4():
	return (206,229,237,255)
def get_rojo1():
	return (255,0,0,255)
def get_amarillo1():
	return (255,255,0,255)
def get_verde1():
	return (0,183,0,255)
def get_bordo1():
	return (178,0,0,255)
def get_azul1():
	return (55,93,237,255)
def get_rojo1():
	return (255,0,0,255)

# DE BiblioJAM
def get_jamimagenes():
	''' Devuelve las imágenes de BiblioJAM. '''
	return (DIRECTORIO_BIBLIOJAM + "/Recursos/Iconos/CeibalJAM.png", DIRECTORIO_BIBLIOJAM + "/Recursos/Iconos/bandera_uruguay.png",
	DIRECTORIO_BIBLIOJAM + "/Recursos/Iconos/licencia.png")
def get_terron():
	''' Devuelve Terron de CeibalJAM! '''
	return DIRECTORIO_BIBLIOJAM + "/Recursos/Iconos/icono_jam.png"

def get_sound_select():
	''' Carga y Devuelve el sonido "select" de BiblioJAM para JAMButton '''
	#pygame.mixer.init()
	return pygame.mixer.Sound(DIRECTORIO_BIBLIOJAM + "/Recursos/Sonidos/select.ogg")
def get_sound_clock_tick1():
	''' Carga y Devuelve el sonido "clock1" de BiblioJAM. '''
	#pygame.mixer.init()
	return pygame.mixer.Sound(DIRECTORIO_BIBLIOJAM + "/Recursos/Sonidos/clock_tick1.ogg")
def get_alarma_reloj1():
	''' Carga y Devuelve el sonido "alarma-reloj1" de BiblioJAM. '''
	#pygame.mixer.init()
	return pygame.mixer.Sound(DIRECTORIO_BIBLIOJAM + "/Recursos/Sonidos/alarma-reloj1.ogg")
def get_alarma_reloj2():
	''' Carga y Devuelve el sonido "alarma-reloj2" de BiblioJAM. '''
	#pygame.mixer.init()
	return pygame.mixer.Sound(DIRECTORIO_BIBLIOJAM + "/Recursos/Sonidos/alarma-reloj2.ogg")

# ICONOS
def get_icon_back():
	''' Devuelve las imágenes para botones atras, delante, play y salir. '''
	atras= DIRECTORIO_BIBLIOJAM + "/Recursos/Iconos/anterior.png"
	return atras
def get_icon_next():
	''' Devuelve las imágenes para botones atras, delante, play y salir. '''
	delante= DIRECTORIO_BIBLIOJAM + "/Recursos/Iconos/siguiente.png"
	return delante
def get_icon_play():
	''' Devuelve las imágenes para botones atras, delante, play y salir. '''
	play= DIRECTORIO_BIBLIOJAM + "/Recursos/Iconos/play.png"
	return play
def get_icon_exit():
	''' Devuelve las imágenes para botones atras, delante, play y salir. '''
	salir= DIRECTORIO_BIBLIOJAM + "/Recursos/Iconos/cerrar.png"
	return salir
#def get_icon_stop():
#	''' Devuelve las imágenes para botones atras, delante, play y salir. '''
#	stop= DIRECTORIO_BIBLIOJAM + "/Recursos/Iconos/??.png"
#	return stop
def get_icon_ok():
	''' Devuelve las imágenes para botones ok y cancel. '''
	ok= DIRECTORIO_BIBLIOJAM + "/Recursos/Iconos/tick_ok.png"
	return ok
def get_icon_cancel():
	''' Devuelve las imágenes para botones ok y cancel. '''
	cancel= DIRECTORIO_BIBLIOJAM + "/Recursos/Iconos/tick_cancel.png"
	return cancel

# IMAGENES Y SUPERFICIES
def get_Rectangulo(color, tamanio):
	''' Devuelve una superficie según color y tamaño. '''
	superficie = pygame.Surface( tamanio, flags=HWSURFACE )
	superficie.fill(color)
	return superficie
def get_Rectangulo_Transparente(tamanio):
	''' Devuelve una superficie según color y tamaño. '''
	superficie = pygame.Surface( tamanio, flags=HWSURFACE )
	superficie.fill(get_magenta())
	superficie.set_colorkey(get_magenta(), pygame.RLEACCEL)
	return superficie
def get_my_surface_whit_border(superficie, color, grosor):
	''' Pinta un Borde Rectangular sobre una superficie y devuelve el resultado. '''
	pygame.draw.rect(superficie, color, superficie.get_rect(), grosor)
	return superficie
def get_Elipse(color, tamanio):
	''' Devuelve una Elipse según color y tamaño. '''
	superficie = pygame.Surface( tamanio, flags=HWSURFACE )
	superficie.fill(get_magenta())
	superficie.set_colorkey(get_magenta(), pygame.RLEACCEL)
	rectangulo = (0, 0, tamanio[0], tamanio[1])
	pygame.draw.ellipse(superficie, color, rectangulo, 0)
	return superficie
def get_my_surface_whit_elipse_border(superficie, color, grosor):
	''' Pinta un Borde Eliptico sobre una superficie y devuelve el resultado. '''
	try:
		rectangulo= (0,0,superficie.get_size()[0],superficie.get_size()[1])
		pygame.draw.ellipse(superficie, color, rectangulo, int(grosor))
		return superficie
	except:
		print rectangulo, color, grosor
def pegar_imagenes_centradas(superficie1, superficie2):
	''' Pega superficie1 sobre superficie2. '''
	w,h= superficie2.get_size()
	w1,h1= superficie1.get_size()
	superficie2.blit(superficie1, (w/2-w1/2, h/2-h1/2))
	return superficie2
def pegar_imagenes_alineado_izquierda(superficie1, superficie2):
	''' Pega superficie1 sobre superficie2. '''
	w,h= superficie2.get_size()
	w1,h1= superficie1.get_size()
	superficie2.blit(superficie1, (0, h/2-h1/2))
	return superficie2
def pegar_imagenes_alineado_derecha(superficie1, superficie2):
	''' Pega superficie1 sobre superficie2. '''
	w,h= superficie2.get_size()
	w1,h1= superficie1.get_size()
	superficie2.blit(superficie1, (w-w1, h/2-h1/2))
	return superficie2

def get_grilla(superficie, columnas, filas): # Utilizado por JAMBoard
	''' Devuelve una lista de posiciones en una superficie, según columnas y filas. '''
	ancho, alto= superficie.get_size()
	cuadros= ancho/columnas
	posiciones= []
	for f in range(0, filas):
		for x in range(0, columnas):
			posiciones.append( (cuadros*x, cuadros*f) )
	return posiciones

def get_matriz_rect(lado, colum, filas):
	''' Devuelve una lista de columnas:
		que contiene cuadrados iguales. '''
	x,y= (0,0)
	columnas= []
	for col in range(colum):
	# para todas las columnas

		fila= []
		for rect in range(filas):
		# para todas las filas
			rectangulo= pygame.rect.Rect(x,y,lado,lado)
			fila.append(rectangulo)
			y+= lado

		columnas.append(fila)
		x+= lado
		y= 0
		
	return columnas

def get_cuadricula(superficie, columnas, filas): # Utilizado por JAMClock
	''' Devuelve una lista de rectángulos en una superficie, según columnas y filas. '''
	ancho, alto= superficie.get_size()
	cuadros= ancho/columnas
	rectangulos= []
	for f in range(0, filas):
		for x in range(0, columnas):
			rectangulos.append( (cuadros*x, cuadros*f, ancho/columnas, alto/filas) )
	return rectangulos


# Devuelve las diferentes Simbologías para sprites necesarios en JAMBoard.
def get_letras_up():
	return ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
def get_tildes_up():
	return ['Á', 'É', 'Í', 'Ó', 'Ú']
def get_letras_down():
	return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
def get_tildes_down():
	return ['á', 'é', 'í', 'ó', 'ú']
def get_numeros():
	return ['1','2','3','4','5','6','7','8','9','0']
def get_simbols():
	return ['^', '_', '~', '|', '\\', '#', '$', '€', '&', '@', '%', 'ª', 'º', '·', '¡', '!', '¿', '?', '\'', '\"', '(', ')', '{', '}', '[', ']']
def get_otros():
	return [',', '.', ':', ';', '<', '>']
def get_matematicas():
	return ['*', '+', '-', '/', '=']
def get_especiales():
	return ['´', "Espacio", "Borrar", "Enter"]

# Seteos automáticos para JAMButton.
def get_default_jambutton_values():
	''' Devuelve los valores default para JAMButton. '''
	COLORCARA = (242,242,242,255)
	COLORBAS= (128,128,128,255)
	COLORBOR= (179,179,179,255)
	GROSORBOR= 7
	DETALLE= 2
	ESPESOR= 8
	return COLORCARA, COLORBAS, COLORBOR, GROSORBOR, DETALLE, ESPESOR

# Estilos de colores para JAMBoard.
def get_estilo_naranja():
	return (200,100,0,255), (240,150,0,255), (255,220,0,255)
def get_estilo_gris():
	return (128,128,128,255), (179,179,179,255), (242,242,242,255)
def get_estilo_celeste():
	return (0,128,128,255),(0,180,180,255),(0,240,240,255)
def get_estilo_papel_quemado():
	return (148,107,54), (197,155,101), (231,207,178)

# CALENDARIO
def get_calendar(mes, anio):
	''' Devuelve una lista que representa los renglones para
	un calendario según mes y año, (anio y mes deben ser enteros). '''
	import calendar
	calendario= calendar.Calendar()
	semanas= calendario.monthdayscalendar(anio, mes)
	toodoelmes= []
	for i in (semanas):
		todalasemana=[]
		for fecha in i:
			if int(fecha)!=0:
				todalasemana.append(fecha)
		toodoelmes.append(todalasemana)
	#toodoelmes.insert(0, ["%s de %s" % (get_abrevia_mes(mes), anio)])
	toodoelmes.insert(0, "%s de %s" % (get_mes(mes), anio))
	toodoelmes.insert(1,["lu", "ma", "mie", "jue", "vie", "sa", "do"])
	return toodoelmes

def get_abrevia_mes(numero):
	''' Recibe un entero de 1 a 12 y devuelve la abreviación del mes correspondiente.'''
	numero= int(numero)
	if numero== 1: return "ene"
	if numero== 2: return "feb"
	if numero== 3: return "mar"
	if numero== 4: return "abr"
	if numero== 5: return "may"
	if numero== 6: return "jun"
	if numero== 7: return "jul"
	if numero== 8: return "ago"
	if numero== 9: return "sep"
	if numero== 10: return "oct"
	if numero== 11: return "nov"
	if numero== 12: return "dic"

def get_mes(numero):
	''' Recibe un entero de 1 a 12 y devuelve el nombre del mes correspondiente.'''
	numero= int(numero)
	if numero== 1: return "Enero"
	if numero== 2: return "Febrero"
	if numero== 3: return "Marzo"
	if numero== 4: return "Abril"
	if numero== 5: return "Mayo"
	if numero== 6: return "Junio"
	if numero== 7: return "Julio"
	if numero== 8: return "Agosto"
	if numero== 9: return "Setiembre"
	if numero== 10: return "Octubre"
	if numero== 11: return "Noviembre"
	if numero== 12: return "Diciembre"

def get_dia(numero):
	''' Recibe un entero de 1 a 7 y devuelve el nombre del día correspondiente.'''
	numero= int(numero)
	if numero== 1: return "Lunes"
	if numero== 2: return "Martes"
	if numero== 3: return "Miercoles"
	if numero== 4: return "Jueves"
	if numero== 5: return "Viernes"
	if numero== 6: return "Sabado"
	if numero== 7: return "Domingo"

# Efectos
def get_fire():
	''' Imagenes de un fuego. '''
	imagenes_cargadas= []
	imagenes= os.listdir(DIRECTORIO_BIBLIOJAM + "/Recursos/Fuego/")
	for imagen in imagenes:
		im= pygame.image.load(DIRECTORIO_BIBLIOJAM + "/Recursos/Fuego/" + imagen)
		imagenes_cargadas.append(im)
	return imagenes_cargadas

def get_nube():
	''' Imagenes de nubes. '''
	imagen= pygame.image.load(DIRECTORIO_BIBLIOJAM + "/Recursos/Nubes/nube1.png")
	#pygame.transform.scale(pygame.image.load(DIRECTORIO_BIBLIOJAM + "/Recursos/Nubes/001.png"), (125,125))
	return imagen

def get_sound_lluvia():
	''' Carga y Devuelve el sonido de la lluvia para JAMNubes '''
	#pygame.mixer.init()
	return pygame.mixer.Sound(DIRECTORIO_BIBLIOJAM + "/Recursos/Sonidos/lluvia.ogg")

'''
def get_libro():
	Libreta de lectura.
	return DIRECTORIO_BIBLIOJAM + "/Recursos/Iconos/libreta.png" 

	def get_hoja():
		Devuelve la imagen para una hoja vacía.
		imagen= pygame.image.load(VG.get_libro())
		ancho, alto= imagen.get_size()
		fondo= VG.get_Rectangulo(VG.get_blanco(), (ancho, alto*19))

		x, y= (0,0)
		for n in range(19):
			fondo.blit(imagen, (x, y))
			y+=alto
		#fondo= pygame.transform.scale(fondo,(296,420))
		return fondo
'''

def get_hoja(escala):
	''' Devuelve la imagen para una hoja vacía y un valor "margen" para el texto. '''
	imagen= pygame.image.load(DIRECTORIO_BIBLIOJAM + "/Recursos/Iconos/hoja.png")
	if type(escala)== tuple and type(escala[0])== int and type(escala[1])== int:
		imagen= pygame.transform.scale(imagen, escala)
	w,h= imagen.get_size()
	margen= w/10
	return imagen, margen

def get_Sombra(tamanio, color, opacidad):
	x= pygame.sprite.OrderedUpdates()
	sombra= pygame.sprite.Sprite()
	sombra.image= get_Rectangulo(color, tamanio)
	sombra.image.set_alpha(opacidad, SRCALPHA)
	sombra.rect= sombra.image.get_rect()
	x.add(sombra)
	return x
