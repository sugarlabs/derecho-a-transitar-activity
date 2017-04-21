#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Globals.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame
import gc
import sys
import os
import random
import platform
import gtk
import shelve

from pygame.locals import *
gc.enable()

import BiblioJAM
from BiblioJAM.JAMButton import JAMButton
from BiblioJAM.JAMLabel import JAMLabel
import BiblioJAM.JAMGlobals as JAMG

GRIS = gtk.gdk.Color(60156, 60156, 60156, 1)
AMARILLO1 = gtk.gdk.Color(65000,65000,40275,1)
NARANJA = gtk.gdk.Color(65000,26000,0,1)
BLANCO = gtk.gdk.Color(65535, 65535, 65535,1)
NEGRO = gtk.gdk.Color(0, 0, 0, 1)
CELESTE = gtk.gdk.Color(63000, 65535, 65535,1)

if "olpc" in platform.platform():
	os.environ['SDL_AUDIODRIVER'] = 'alsa'

DIRECTORIO_BASE = os.path.dirname(__file__)
IMAGENES = os.path.join(DIRECTORIO_BASE, "Imagenes")
SONIDOS = os.path.join(DIRECTORIO_BASE, "Sonidos")

USERS = os.path.join(os.environ["HOME"], "DerechoATransitar")
if not os.path.exists(USERS):
	os.mkdir(USERS)
	os.chmod(USERS, 0755)

def get_users():
	archivos = os.listdir(USERS)
	usuarios = []
	for archivo in archivos:
		arch = shelve.open(os.path.join(USERS, archivo))
		usuario = dict(arch)
		arch.close()
		usuarios.append(usuario)
	return usuarios

def Traduce_posiciones(VA, VH):
	eventos = pygame.event.get(pygame.MOUSEBUTTONDOWN)
	for event in eventos:
		x, y = event.pos
		xx = x/VA
		yy = y/VH
		event_pos = (xx, yy)
	for event in eventos:
		evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN,
			pos = event_pos, button = event.button)
		pygame.event.post(evt)

	eventos = pygame.event.get(pygame.MOUSEMOTION)
	for event in eventos:
		x, y = event.pos
		xx = x/VA
		yy = y/VH
		event_pos = (xx, yy)
	for event in eventos:
		evt = pygame.event.Event(pygame.MOUSEMOTION,
			pos = event_pos, rel = event.rel, buttons = event.buttons)
		pygame.event.post(evt)

# ---- Generales
RESOLUCION = (1200,900)
def get_Fondo_Inicial():
	imagen = os.path.join(IMAGENES, "Pantalla-Inicio.jpg")
	return pygame.transform.scale(pygame.image.load(imagen), RESOLUCION)
def get_Fondo():
	imagen = os.path.join(IMAGENES, "fondo1.jpg")
	return pygame.transform.scale(pygame.image.load(imagen), RESOLUCION)
def get_Flecha():
	return os.path.join(IMAGENES, "flecha.png")
def get_Sonidos():
	sonido = os.path.join(SONIDOS, "frenada1.ogg")
	frenada1 = pygame.mixer.Sound(sonido)
	sonido = os.path.join(SONIDOS, "aplausos1.ogg")
	aplausos1 = pygame.mixer.Sound(sonido)
	return frenada1, aplausos1
def get_ambiente():
	ambiente = None
	# pygame.mixer.music.load(DIRECTORIO_BASE+"/Sonidos/ambiente.ogg")
	return ambiente
def get_Imagen_Cartel1():
	imagen = os.path.join(IMAGENES, "cartel1.png")
	return pygame.transform.scale(pygame.image.load(imagen), (276,145))
def get_Imagen_CartelMenu():
	imagen = os.path.join(IMAGENES, "cartel2.png")
	un = pygame.transform.scale(pygame.image.load(imagen), (250,162))
	imagen = os.path.join(IMAGENES, "cartel3.png")
	dos = pygame.transform.scale(pygame.image.load(imagen), (250,162))
	return (un, dos)
def get_Imagen_Gruber1():
	imagen = os.path.join(IMAGENES, "cebra1.png")
	return pygame.transform.scale(pygame.image.load(imagen), (250,310))
def get_Imagen_Gruber2():
	imagen = os.path.join(IMAGENES, "cebra2.png")
	return pygame.transform.scale(pygame.image.load(imagen), (250,310))
def get_Imagen_Gruber3():
	imagen = os.path.join(IMAGENES, "cebra3.png")
	return pygame.transform.scale(pygame.image.load(imagen), (250,310))
	
def get_sound_clock():
	sonido = os.path.join(SONIDOS, "clock_tick1.ogg")
	clock1 = pygame.mixer.Sound(sonido)
	sonido = os.path.join(SONIDOS, "clock_tick2.ogg")
	clock2 = pygame.mixer.Sound(sonido)
	sonido = os.path.join(SONIDOS, "clock_tick3.ogg")
	clock3 = pygame.mixer.Sound(sonido)
	return [clock1, clock2, clock3]
def get_instruc(name):
	imagen = os.path.join(IMAGENES, "Instructivos/%s.jpg" % (name))
	return pygame.transform.scale(pygame.image.load(imagen), RESOLUCION)
def get_Presentacion():
	directorio = os.path.join(IMAGENES, "Presentacion")
	imagenes = []
	archivos = []
	for archivo in os.listdir(directorio):
		archivos.append(archivo)
	archivos.sort()
	for archivo in archivos:
		img = os.path.join(directorio, "%s" % (archivo))
		imagen = pygame.transform.scale(pygame.image.load(img), RESOLUCION)
		imagenes.append(imagen)
	return imagenes
'''
def get_cartel_presenta():
	imagen = os.path.join(IMAGENES, "pandilla1.png")
	img1 = pygame.transform.scale(pygame.image.load(imagen), (175,175))
	imagen = os.path.join(IMAGENES, "pandilla2.png")
	img2 = pygame.transform.scale(pygame.image.load(imagen), (175,175))
	return img1, img2'''
# -------------  T0101  -------------
# Imagenes:
def get_Fondos_FGR_T0101():
	imagen = os.path.join(IMAGENES, "FGR_T0101", "fondo1.jpg")
	fondo1 = pygame.transform.scale(pygame.image.load(imagen), RESOLUCION)
	imagen = os.path.join(IMAGENES, "FGR_T0101", "fondo2.jpg")
	fondo2 = pygame.transform.scale(pygame.image.load(imagen), RESOLUCION)
	return (fondo1, fondo2)

def get_Seniales_FGR_T0101():
	''' Devuelve las señales y sus posiciones. '''
	seniales = {}
	imagen = os.path.join(IMAGENES, "Seniales1", "senial1.png")
	seniales["Sentido obligatorio"] = (pygame.transform.scale(pygame.image.load(imagen),(145,145)))
	imagen = os.path.join(IMAGENES, "Seniales1", "senial2.png")
	seniales["Curva Peligrosa"] = (pygame.transform.scale(pygame.image.load(imagen),(145,145)))
	imagen = os.path.join(IMAGENES, "Seniales1", "senial3.png")
	seniales["Prohibido Adelantar o Rebasar"] = (pygame.transform.scale(pygame.image.load(imagen),(145,145)))
	imagen = os.path.join(IMAGENES, "Seniales1", "senial4.png")
	seniales["¡Peligro! Paso a nivel sin barrera"] = (pygame.transform.scale(pygame.image.load(imagen),(145,145)))
	imagen = os.path.join(IMAGENES, "Seniales1", "senial5.png")
	seniales["Prohibido acceso a peatones"] = (pygame.transform.scale(pygame.image.load(imagen),(145,145)))
	return seniales
def get_Posicion_Seniales_FGR_T0101():
	return [(190,323), (395,272), (600,339), (805,269), (1010,338)]

def get_Carteles_FGR_T0101():
	''' Devuelve los textos de los carteles. '''
	carteles= {}
	carteles["Sentido obligatorio"] = None
	carteles["Curva Peligrosa"] = None
	carteles["Prohibido Adelantar o Rebasar"] = None
	carteles["¡Peligro! Paso a nivel sin barrera"] = None
	carteles["Prohibido acceso a peatones"] = None
	return carteles
def get_Posicion_Carteles_FGR_T0101():
	''' Devuelve las posiciones de los carteles. '''
	return [(250,604), (600,604), (950,604), (370,780), (830,780)]

# Textos:
INTRO_FGR_T0101='''Primero lo primero.
Para poder formar parte de la pandilla y conseguir el objetivo final,
tienes que demostrar algunos conocimientos.
¿Te animas a unir las señales de tránsito que aparecen con sus
respectivas definiciones?  Ej: señal “Curva peligrosa” con Curva peligrosa.
Recuerda que el tiempo corre. '''

def get_Textos_FGR_T0101():
	textos= []
	for linea in INTRO_FGR_T0101.split("\n"):
		textos.append(linea)
	return textos
# -------------  T0101  -------------

# -------------  T0102  -------------
# Imagenes:
def get_Fondos_FGR_T0102():
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0102/fondo1.jpg"), RESOLUCION)
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0102/fondo2.jpg"), RESOLUCION)
	return (fondo1, fondo2)

def get_Seniales_FGR_T0102():
	''' Devuelve las imágenes de las señales. '''
	directorio= DIRECTORIO_BASE+"/Imagenes/Seniales2/"
	seniales= {}
	seniales["Camping"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Camping.png")),(100,100))), "Información")
	seniales["Ceda el Paso"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Ceda el Paso.png")),(100,100))), "Prioridad")
	seniales["Circulacion Bicicletas"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Circulacion Bicicletas.png")),(100,100))), "Peligro")
	seniales["Circulacion dos Sentidos"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Circulacion dos Sentidos.png")),(100,100))), "Peligro")
	seniales["Contramano"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Contramano.png")),(100,100))), "Prohibición")
	seniales["Hospital"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Hospital.png")),(100,100))), "Información")
	seniales["Limitacion Altura"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Limitacion Altura.png")),(100,100))), "Prohibición")
	seniales["Limitacion Peso"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Limitacion Peso.png")),(100,100))), "Prohibición")
	seniales["Luces Cortas"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Luces Cortas.png")),(100,100))), "Obligación")
	seniales["No Adelantar"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("No Adelantar.png")),(100,100))), "Prohibición")
	seniales["No Circular"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("No Circular.png")),(100,100))), "Prohibición")
	seniales["Pare"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Pare.png")),(100,100))), "Prioridad")
	seniales["Paso Animales"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Paso Animales.png")),(100,100))), "Peligro")
	seniales["Paso a Nivel"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Paso a Nivel.png")),(100,100))), "Peligro")
	seniales["Policia"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Policia.png")),(100,100))), "Información")
	seniales["Sentido Obligacion"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Sentido Obligacion.png")),(100,100))), "Obligación")
	seniales["Velocidad Maxima"]= ( (pygame.transform.scale(pygame.image.load(directorio + "%s" % ("Velocidad Maxima.png")),(100,100))), "Prohibición")
	# modificacion 12 al azar
	random.seed()
	claves= seniales.keys()
	claveslen= len(claves)-1
	while not len(seniales)== 12:
		try:
			indice= random.randrange(claveslen)
			del seniales[claves.pop(indice)]
		except:
			print "Error en: modificacion 12 al azar T0102"
	return seniales
def get_Posicion_Seniales_FGR_T0102():
	#x= 75
	x= 33
	y= 850
	posiciones= []
	for b in range(1,3):
		#x= 75
		x= 33
		for a in range(1,10):
			if a > 2 and a < 9:
				posiciones.append((x,y))
			x+= 130
		y-= 100
	return posiciones

def get_Carteles_FGR_T0102():
	''' Devuelve las imágenes de los carteles. '''
	directorio= DIRECTORIO_BASE+"/Imagenes/Personajes/"
	carteles= {}

	imagen= pygame.image.load(directorio + "%s" % ("Informacion.png"))
	w,h= imagen.get_size()
	w-= 20
	h-= 20
	carteles["Información"]= pygame.transform.scale(imagen.copy(), (w,h))

	imagen= pygame.image.load(directorio + "%s" % ("Obligacion.png"))
	w,h= imagen.get_size()
	w-= 20
	h-= 20
	carteles["Obligación"]= pygame.transform.scale(imagen.copy(), (w,h))

	imagen= pygame.image.load(directorio + "%s" % ("Peligro.png"))
	w,h= imagen.get_size()
	w-= 20
	h-= 20
	carteles["Peligro"]= pygame.transform.scale(imagen.copy(), (w,h))

	imagen= pygame.image.load(directorio + "%s" % ("Prioridad.png"))
	w,h= imagen.get_size()
	w-= 20
	h-= 20
	carteles["Prioridad"]= pygame.transform.scale(imagen.copy(), (w,h))

	imagen= pygame.image.load(directorio + "%s" % ("Prohibicion.png"))
	w,h= imagen.get_size()
	w-= 20
	h-= 20
	carteles["Prohibición"]= pygame.transform.scale(imagen.copy(), (w,h))
	return carteles

def get_Posicion_Carteles_FGR_T0102():
	return [(375, 170), (815, 170), (180, 475), (590, 475), (1010, 475)]

# Textos:
INTRO_FGR_T0102='''José Máforo:
Tenemos que colocar cada una de las señales de tránsito en el
grupo al que corresponden y así conseguiremos nuestro primer sticker.
Ej: señal: “Hospital” en Grupo: Informativa. 
Es por tiempo, no lo olvidemos!'''

def get_Textos_FGR_T0102():
	textos= []
	for linea in INTRO_FGR_T0102.split("\n"):
		textos.append(linea)
	return textos
# -------------  T0102  -------------

# -------------  T0103  -------------
def get_Fondos_FGR_T0103():
	imagen = os.path.join(IMAGENES, "FGR_T0103", "fondo1.jpg")
	fondo1 = pygame.transform.scale(pygame.image.load(imagen), RESOLUCION)
	imagen = os.path.join(IMAGENES, "FGR_T0103", "fondo2.jpg")
	fondo2 = pygame.transform.scale(pygame.image.load(imagen), RESOLUCION)
	return (fondo1, fondo2)

def get_seniales_FGR_T0103():
	return	[(os.path.join(IMAGENES, "Seniales2", "Circulacion Bicicletas.png"), "Circulacion Bicicletas", "Peligro"),
	(os.path.join(IMAGENES, "Seniales2", "No Adelantar.png"), "No Adelantar", "Prohibición"),
	(os.path.join(IMAGENES, "Seniales2", "Hospital.png"), "Hospital", "Información"),
	(os.path.join(IMAGENES, "Seniales2", "Pare.png"), "Pare", "Prioridad"),
	(os.path.join(IMAGENES, "Seniales2", "Sentido Obligacion.png"), "Sentido Obligacion", "Obligación"),
	(os.path.join(IMAGENES, "Seniales2", "Paso a Nivel.png"), "Paso a Nivel", "Peligro")]
# -------------  T0103  -------------

# -------------  T0201  -------------
# Imagenes:
def get_Fondos_FGR_T0201():
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0201/fondo1.jpg"), RESOLUCION)
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0201/fondo2.jpg"), RESOLUCION)
	return (fondo1,fondo2)

def get_Imagenes_FGR_T0201():
	imagenes= [pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0201/Bicicleta.png"), (180,180)),
	pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0201/Cebra.png"), (180,180)),
	pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0201/Semaforo.png"), (180,180))]
	return imagenes

# Textos:
INTRO_FGR_T0201= '''Natalia Vansilla:
Hoy en mi clase aprendimos sobre seguridad vial y
cómo debemos actuar como peatón.
Juguemos por tiempo a completar los espacios en blanco con
las palabras que tenemos.
Ej: Las personas que circulan a pie son: Peatones.
Titu Titu, pasa el tiempo.'''

def get_Textos_FGR_T0201():
	textos= []
	for linea in INTRO_FGR_T0201.split("\n"):
		textos.append(linea)
	return textos

def get_palabras_FGR_T0201():
	return ["PEATONES", "ACERA", "BORDE", "CALLE", "CRUZAR", "SEMAFORO", "CEBRA", "AMBOS LADOS", "CARRETERA", "ESTACIONADOS", "OPUESTA",
"FILA", "JUGAR", "VISIBILIDAD", "DISTANCIA", "VELOCIDAD", "SENTIDOS", "BANQUINA", "ACERA", "CRUZAR", "ESQUINA"]

def get_Posicion_Palabras_FGR_T0201():
	w,h= RESOLUCION
	l= w/8
	x= 40
	y= 735
	posiciones= []
	for b in range(1,4):
		x= 40
		for a in range(1,8):
			posiciones.append((x,y))
			x+= l+10
		y+= 44
	return posiciones
# -------------  T0201  -------------

# -------------  T0202  -------------
# Imagenes:
def get_Fondos_FGR_T0202():
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/fondo1.jpg"), RESOLUCION)
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/fondo2.jpg"), RESOLUCION)
	return (fondo1,fondo2)

def get_afirmaciones_FGR_T0202():
	afirmaciones= [
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/01.png"), (736,504)),
	"Las señales de tránsito están para orientar a los peatones.\nNo hay que respetarlas siempre si no es necesario", False),

	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/02.png"), (736,504)),
	"La senda peatonal (\"cebra\") indica por donde\nel peatón puede cruzar la calle", True),

	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/03.png"), (736,504)),
	"Si pasamos por la cebra tenemos prioridad absoluta,\nincluso cuando pasan los bomberos o la ambulancia.", False),

	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/04.png"), (736,504)),
	"Si tenemos que desplazarnos por una calle de doble circulación,\ndebemos mirar a ambos lados antes de cruzar.", True),

	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/05.png"), (736,504)),
	"Si vamos por una carretera vamos siempre por la \"mano\" derecha.", False),

	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/06.png"), (736,504)),
	"Por la carretera los vehículos circulan más rápido.\nCruzamos en el lugar de más visibilidad", True),

	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/07.png"), (736,504)),
	"Cruzamos con la luz verde del semáforo.\nSi no viene ningún automóvil, podemos cruzar con luz amarilla o roja", False),
	
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/08.png"), (736,504)),
	"Siempre caminamos por la acera. Nunca por la calzada.", True),

	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/09.png"), (736,504)),
	"Si cruzo por la \"cebra\" puedo ir jugando con mis amigos,\nporque ese es un lugar seguro para los peatones.", False),

	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/10.png"), (736,504)),
	"Cuando hay una entrada de garaje,\ntengo que mirar si no sale un automóvil.", True),

	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/11.png"), (736,504)),
	"Si hay dos vehículos estacionados,\ncruzo entre ellos, porque me dan protección.", False)]
	return afirmaciones

# Textos:
INTRO_FGR_T0202= '''Parece que Arturo recién está aprendiendo
cómo circular en la calle y necesita ayuda.
Enséñenle cuáles de estas afirmaciones son verdaderas y cuáles son falsas.
Ej: La senda peatonal (“cebra”) indica donde el peatón puede cruzar la calle.
Esto es verdadero. No olviden el tiempo.'''

def get_Textos_FGR_T0202():
	textos= []
	for linea in INTRO_FGR_T0202.split("\n"):
		textos.append(linea)
	return textos
# -------------  T0202  -------------

# -------------  T0301  -------------
# Imagenes:
def get_Fondos_FGR_T0301():
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0301/fondo1.jpg"), RESOLUCION)
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0301/fondo2.jpg"), RESOLUCION)
	return (fondo1,fondo2)

def get_personajes_FGR_T0301():
	return pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0301/personajes.png"), (306,207))

def get_imagen_FGR_T0301(imagen):
	return pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0301/%s.png" % (imagen)), (300,300))

# Textos:
INTRO_FGR_T0301= '''Jacinto Puesto:
Pandilla, mis padres me dijeron que si sabía las partes
más importantes de una bicicleta me la regalaban para mi cumpleaños.
José Máforo:
Genial, aprendámoslas juntos con esta sopa de letras, sólo hay que
encontrar las palabras en el recuadro. Ej: Rueda.
Tic Tac, tic tac.'''

def get_Textos_FGR_T0301():
	textos= []
	for linea in INTRO_FGR_T0301.split("\n"):
		textos.append(linea)
	return textos
# -------------  T0301  -------------

# -------------  T0302  -------------
# Imagenes:
def get_Fondos_FGR_T0302():
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/fondo1.jpg"), RESOLUCION)
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/fondo2.jpg"), RESOLUCION)
	return (fondo1,fondo2)

# Textos:
INTRO_FGR_T0302= '''Ahora que aprendieron las partes más importantes de la bici,
demuestren que saben circular correctamente en ella.
Sólo tienen que marcar la opción correcta a estas afirmaciones.
Ej: Cuando voy a atravesar un cruce sin semáforo, si hay cebra,
primero me bajo de la bici y la cruzo caminando.
No olvidar el tiempo.'''

def get_Textos_FGR_T0302():
	textos= []
	for linea in INTRO_FGR_T0302.split("\n"):
		textos.append(linea)
	return textos

def get_afirmaciones_FGR_T0302():
	# Frase disparadora
	#	imagen - opcion - valor
	#	imagen - opcion - valor
	#	imagen - opcion - valor
	afirmaciones= {
	1:("Cuando voy a atravesar un cruce sin semáforo",
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/01.png"), (345,345)),
	"Miro a ambos lados\nantes de cruzar", False),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/02.png"), (345,345)),
	"Si hay cebra, voy hacia ella,\nme bajo de la bici y\nla cruzo caminando", True),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/03.png"), (345,345)),
	"Cruzo media calzada, espero y\nluego la otra mitad", False)),
	2:("Cuando circulo por la calle",
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/04.png"), (345,345)),
	"Lo hago por donde queda espacio", False),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/05.png"), (345,345)),
	"Siempre por la izquierda", False),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/06.png"), (345,345)),
	"Siempre por la derecha", True)),
	3:("Cuando adelanto a otra bici o a un peatón",
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/07.png"), (345,345)),
	"Aviso con la bocina", True),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/08.png"), (345,345)),
	"No es necesario avisar", False),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/09.png"), (345,345)),
	"Adelanto por donde\nhaya lugar libre", False)),
	4:("Cuando circulo por la calle",
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/10.png"), (345,345)),
	"Lo hago bien pegado a\nlos autos estacionados", False),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/11.png"), (345,345)),
	"Lo hago a una distancia prudencial\nde los vehículos estacionados,\nasí no me golpean si de modo\nimprevisto abren la puerta", True),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/12.png"), (345,345)),
	"A veces voy pegado,\na veces mantengo distancia\nprudencial", False)),
	5:("El casco lo uso",
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/13.png"), (345,345)),
	"Siempre y bien abrochado", True),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/14.png"), (345,345)),
	"Cuando llueve así no me mojo", False),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/15.png"), (345,345)),
	"En realidad no es necesario;\nbasta con tener un gorro\ncon visera para evitar\nencandilarse", False)),
	6:("En la bicicleta vamos",
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/16.png"), (345,345)),
	"Siempre de a 2! Es super divertido", False),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/17.png"), (345,345)),
	"Yo y mi sentido común", True),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/18.png"), (345,345)),
	"Solo yo, aunque a veces\nalgún amigo me pide que\nlo “arrastre” cuando va\ncon sus patines", False)),
	7:("Los ciclistas tenemos prioridad sobre",
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/19.png"), (345,345)),
	"Los peatones", False),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/20.png"), (345,345)),
	"Los vehículos", False),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/21.png"), (345,345)),
	"Ninguno de los dos", True))
	}

	return afirmaciones
# -------------  T0302  -------------

# -------------  T0401  -------------
# Imagenes:
def get_Fondos_FGR_T0401():
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0401/fondo1.jpg"), RESOLUCION)
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0401/fondo2.jpg"), RESOLUCION)
	return (fondo1,fondo2)

# Textos:
INTRO_FGR_T0401= '''Les queda muy poco para conseguir su Carnet.
Veamos cuánto saben sobre la forma correcta de comportarse como pasajero.
Tienen que seleccionar para cada afirmación una respuesta correcta.
Ej: Cuando llega el transporte escolar, espero en orden y si hay
niños más pequeños les permito que suban primero.
Parece difícil, pero juntos de seguro lo van a lograr!
Recuerden que el tiempo pasa.'''

def get_Textos_FGR_T0401():
	textos= []
	for linea in INTRO_FGR_T0401.split("\n"):
		textos.append(linea)
	return textos

def get_afirmaciones_FGR_T0401():
	afirmaciones= {1:["Cuando llega el transporte escolar",
	pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0401/01.png"), (1000,500)),
	("Subo corriendo y trato de ser el primero", False),
	("Espero en orden y si hay niños más pequeños les permito que suban primero", True),
	("Me quedo jugando y siempre deben ir a buscarme", False)],

	2:["Cuando estoy en el transporte escolar",
	pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0401/02.png"), (1000,500)),
	("Me quedo parado conversando con mis amigos y juego a hacer equilibrio", False),
	("Me siento antes de que arranque el vehículo, me pongo mi cinturón\nde seguridad y coloco la mochila debajo del asiento", True),
	("Grito tan alto como puedo para que todos escuchen lo bien que me fue en la escuela", False)],

	3:["Cuando viajo en automóvil, siempre me siento",
	pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0401/03.png"), (1000,500)),
	("A upa", False),
	("En el asiento de adelante", False),
	("En el asiento de atrás", True)],

	4:["Cuando viajo en automóvil, siempre voy",
	pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0401/05.png"), (1000,500)),
	("Cantando bien fuerte", False),
	("Saltando de un lado a otro", False),
	("Disfrutando del viaje sin distraer al conductor", True)],

	5:["Cuando viajo en automóvil, me protejo",
	pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0401/04.png"), (1000,500)),
	("Arrodillado y mirando hacia atrás", False),
	("Utilizando el cinturón de seguridad o la butaca especial de acuerdo a mi altura y peso", True),
	("Parado en el medio de los asientos, bien agarrado de los respaldos", False)],

	6:["Cuando espero el ómnibus",
	pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0401/07.png"), (1000,500)),
	("Corro de un lado a otro de la vereda para esperando que llegue", False),
	("Bajo y subo el cordón de la vereda todo el tiempo a ver si viene más rápido", False),
	("Espero sin bajar de la acera, tranquilo y si hacer alboroto", True)],

	7:["Cuando llega el ómnibus",
	pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0401/08.png"), (1000,500)),
	("Atropello a todos, porque si subo primero, consigo un asiento!", False),
	("Subo ordenadamente, sin empujar y respetando a las personas mayores o con discapacidad", True),
	("Trato de meterme entre los que van bajando mientras le grito a mis amigos que se apuren", False)],

	8:["Cuando estoy en el ómnibus",
	pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0401/09.png"), (1000,500)),
	("Procuro viajar sentado, ¡es mucho más seguro!", True),
	("Saludo a todos mis amigos por la ventana, sacando la cabeza y las manos!", False),
	("Viajo parado porque es muy divertido hacer equilibrio cuando el ómnibus está en marcha", False)],

	9:["Cuando voy a bajar del ómnibus",
	pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0401/10.png"), (1000,500)),
	("Trato de bajar mientras esta en movimiento", False),
	("Espero a que pare y ¡salto los escalones hasta la acera!", False),
	("Aviso con antelación, me preparo, espero que el ómnibus se detenga completamente,\ndesciendo ordenadamente y presto atención al espacio vacío que queda entre la acera y los escalones del ómnibus", True)]
	}
	return afirmaciones
# -------------  T0401  -------------

# -------------  T0501  -------------
# Imagenes:
def get_Fondos_FGR_T0501():
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0501/fondo1.jpg"), RESOLUCION)
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0501/fondo2.jpg"), RESOLUCION)
	return (fondo1,fondo2)

# Textos:
INTRO_FGR_T0501= '''Llegaron al último nivel. Arturo también puede sumarse en esta actividad.
Ayúdenlo y demuestren todo lo que saben sobre cómo debemos
caminar por la ciudad. Es muy fácil, tienen que elegir la opción
correcta para completar las frases. Ej: Debemos caminar por la vereda y
lejos del cordón, porque el riesgo de un siniestro con los automóviles
que circulan, es menor. Juntos es más divertido finalizar el juego y así
obtener el tan esperado carnet. No se olviden que acá también corre el tiempo! '''

def get_Textos_FGR_T0501():
	textos= []
	for linea in INTRO_FGR_T0501.split("\n"):
		textos.append(linea)
	return textos

def get_afirmaciones_FGR_T0501():
	# Frase disparadora
	#	imagen - opcion - valor
	#	imagen - opcion - valor
	#	imagen - opcion - valor
	afirmaciones= {
	"Debemos caminar por la vereda y lejos del cordón, porque:":
		(("Así es más cómodo", False),
		("Si hay charcos no nos salpican", False),
		("El riesgo de un siniestro con los\nautomovilistas que circulan, es menor", True),
		pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0501/01.png"), (700,350))),

	"El adulto debe ir del lado del cordón, porque:":
		(("Es más divertido", False),
		("Los niños están más protegidos", True),
		("Así el adulto avisa cuando se puede cruzar", False),
		pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0501/02.png"), (700,350))),

	"Solo bajamos del cordón cuando empezamos el cruce, porque:":
		(("Así evitamos multas", False),
		("Es más rápido", False),
		("No se puede ir por la calzada", True),
		pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0501/03.png"), (700,350))),

	"Cruzamos en la esquina, porque:":
		(("Allí hay semáforos", False),
		("Es el lugar donde los automovilistas esperan\nque crucen los peatones", True),
		("Es más cómodo", False),
		pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0501/04.png"), (700,350))),

	"En la carretera caminamos por la banquina y contra el tránsito, porque:":
		(("Así vemos los automóviles que\nvienen en dirección opuesta", True),
		("Así nos enseñaron en casa", False),
		("Ocupamos menos espacio", False),
		pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0501/05.png"), (700,350))),

	"En un puente angosto caminamos en “fila india”, porque:":
		(("Es como un juego", False),
		("Todos los puentes se cruzan así", False),
		("Es la forma más segura para\nnosotros y los automovilistas", True),
		pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0501/06.png"), (700,350))),
		}

	return afirmaciones
# -------------  T0501  -------------


# -------------  T0303  -------------
# Imagenes:
def get_Fondos_FGR_T0303():
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0303/fondo1.jpg"), RESOLUCION)
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0303/fondo2.jpg"), RESOLUCION)
	return (fondo1,fondo2)

# Textos:
INTRO_FGR_T0303= '''Natalia Vansilla: Para finalizar este nivel y ser
“Ciclistas y peatones precavidos y expertos “ tenemos que encontrar en
la imagen las respuestas a las preguntas que tenemos.
Ej: ¿Qué personajes se desplazan en esta escena de un modo ecológico?
Los peatones y ciclistas. Tic Tac, el tiempo pasa. '''

def get_Textos_FGR_T0303():
	textos= []
	for linea in INTRO_FGR_T0303.split("\n"):
		textos.append(linea)
	return textos

def get_imagenes_FGR_T0303():
	imagenes= [(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0303/01.png"),(120,120)), (1123,592)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0303/02.png"),(120,120)), ( 851,796)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0303/03.png"),(120,120)), ( 778,621)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0303/04.png"),(120,120)), ( 855,403)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0303/05.png"),(120,120)), ( 867,267)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0303/06.png"),(120,120)), ( 614,285)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0303/07.png"),(120,120)), ( 579,612)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0303/08.png"),(120,120)), ( 368,593))]
	return imagenes

def get_afirmaciones_FGR_T0303():
	afirmaciones=[
	("¿Qué ciclistas circulan por espacios\nreservados sólo para los transeúntes?",5),
	("¿Quién acaba de ocasionar una\ncolisión de autos?",3),
	("¿Qué ciclista circula desatendiendo\nla señal de prohibición de acceso?",4),
	("¿Qué ciclista indica mal\nla dirección que va a tomar?",2),
	]
	return afirmaciones
# -------------  T0303  -------------

# -------------  T0402  -------------
# Imagenes:
def get_Fondos_FGR_T0402():
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/fondo1.jpg"), RESOLUCION)
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/fondo2.jpg"), RESOLUCION)
	return (fondo1,fondo2)

# Textos:
INTRO_FGR_T0402= '''Jacinto Puesto: Hoy en clase la maestra nos habló sobre
cómo comportarnos como pasajeros y como ya lo
habíamos estudiado, nos puso un Ste en orales a José y a mí.
José Máforo: Sí y ahora tenemos que hacer un deber que consiste
en encontrar en la imagen los 7 pasajeros imprudentes. ¿Nos ayudan?
Es muy divertido! Ej: Un niño tocando la corneta. Imprudente.'''

def get_Textos_FGR_T0402():
	textos= []
	for linea in INTRO_FGR_T0402.split("\n"):
		textos.append(linea)
	return textos

def get_imagenes_FGR_T0402():
	imagenes= [(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/01.png"),(260,260)), (302, 433)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/02.png"),(260,260)), ( 598, 403)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/03.png"),(260,260)), ( 627, 269)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/04.png"),(260,260)), ( 799, 475)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/05.png"),(260,260)), ( 843, 215)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/06.png"),(260,260)), ( 955, 402)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/07.png"),(260,260)), ( 1070, 260)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/08.png"),(260,260)), ( 307, 549)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/09.png"),(260,260)), ( 512, 553)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/10.png"),(260,260)), ( 578, 557)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/11.png"),(260,260)), ( 483, 350)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/12.png"),(260,260)), ( 746, 337)),
	(pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/13.png"),(260,260)), ( 1142, 319))]
	return imagenes

def get_afirmaciones_FGR_T0402():
	afirmaciones=[
	("Siete niños y niñas se comportan inadecuadamente dentro de\neste autobús escolar. Descubrimos los pasajeros imprudentes.",[0,1,2,3,4,5,6])
	]
	return afirmaciones
# -------------  T0402  -------------

# -------------  T0502  -------------
def get_letras_FGR_T0502():
	return [
	["C","E","L","U","L","A","R", False, False, False, False],
	["H", False, False, False, False, False, False, False, False, False, False],
	["A", "T", "R", "A", "S", False, False, False, False, "B", False],
	["L", False, False, False, False, False, False, False, False, "O", False],
	["E", False, False, False, False, "M", "U", "S", "I", "C", "A"],
	["C", "O", "D", "E", "R", "A", False, "R", False, "I", False],
	["O", False, False, False, False, "T", False, "I", False, "N", False],
	[False, False, False, False, False, "E", False, False, False, "A", False]]
def get_Fondos_FGR_T0502():
	imagen = os.path.join(IMAGENES, "FGR_T0502", "fondo1.jpg")
	fondo1 = pygame.transform.scale(pygame.image.load(imagen), RESOLUCION)
	imagen = os.path.join(IMAGENES, "FGR_T0502", "fondo2.jpg")
	fondo2 = pygame.transform.scale(pygame.image.load(imagen), RESOLUCION)
	return (fondo1, fondo2)
def get_Texto_FGR_T0502():
	return [
	"1- Papá y mamá lo usan cuando cae el sol para",
	"  ir en moto o caminar por la ruta.",
	"2- Cuando vamos de paseo, mamá y papá nunca",
	"  lo olvidan, pero en el auto, no lo usan JAMÁS!",
	"3- Cuando salimos a pasear en el auto",
	"  siempre vamos . . . y con nuestro -7-.",
	"4- Me las pongo cuando uso la bicicleta",
	"  los patines y el skate.",
	"5- Siempre que salimos a pasear mis padres lo",
	"  preparan, pero en el auto JAMÁS lo prueban.",
	"6- Me encanta que la . . . esté alta, pero para",
	"  evitar distracciones, en el auto",
	"  papá la lleva bajita.",
	"7- Siempre que voy en auto, viajo -3- y",
	"  utilizando mi . . .",
	"8- En el auto y en mi bicicleta, debo",
	"  asegurarme que funcione correctamente la . . ."]
# -------------  T0502  -------------

# -------------  T0204  -------------
def get_letras_FGR_T0204(): # 11
	return [
	[False,False,False,False,False,False,False,False,False,"F","I","L","A"],
	[False,False,False,False,False,False,False,False,False,False,False,False,"C"],
	[False,False,False,False,False,False,"C",False,"B","O","R","D","E"],
	[False,False,False,False,False,False,"R",False,"A",False,False,False,"R"],
	[False,False,False,"E","S","Q","U","I","N","A",False,False,"A"],
	[False,False,False,False,False,False,"Z",False,"Q",False,False,False,False],
	["O","P","U","E","S","T","A",False,"U",False,False,False,False],
	[False,False,False,False,False,False,"R",False,"I",False,False,False,False],
	[False,False,False,False,False,False,False,False,"N",False,False,False,False],
	[False,False,False,False,False,False,"P","E","A","T","O","N",False]]
def get_Fondos_FGR_T0204():
	imagen = os.path.join(IMAGENES, "FGR_T0204", "fondo1.jpg")
	fondo1 = pygame.transform.scale(pygame.image.load(imagen), RESOLUCION)
	imagen = os.path.join(IMAGENES, "FGR_T0204", "fondo2.jpg")
	fondo2 = pygame.transform.scale(pygame.image.load(imagen), RESOLUCION)
	return (fondo1, fondo2)
def get_Texto_FGR_T0204():
	return [
	"1- Al cruzar, siempre lo hago en la . . .",
	"2- Al caminar por la carretera,",
	"  siempre lo hago en dirección -4-",
	"  al sentido de los autos y por la . . .",
	"3- Nunca debo . . . entre dos vehículos",
	"  estacionados.",
	"4- Al caminar por la carretera,",
	"  siempre lo hago en dirección . . . al",
	"  sentido de los autos.",
	"5- Al caminar por la -6-,",
	"  nunca lo hago por el . . .",
	"6- Cuando soy -8- y voy por la",
	"  ciudad, camino por la . . .",
	"7- Al caminar por la carretera en grupo,",
	"  me desplazo en . . .",
	"8- Cualquier persona que circula",
	"  a pie es un . . ."]
# -------------  T0204  -------------

class Controles(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main = main
		self.flecha = None
		self.titulo = None
		self.puntaje = None
		self.cronometro = None
		self.progress_reloj = None
		self.sonidos_reloj = None
		self.user = None

		self.load_sprites()

	def load_sprites(self):
		imagen = self.main.usuario['personaje']
		self.user = JAMButton(self.main.usuario['nombre'],None)
		self.user.set_imagen(origen = imagen, tamanio = (60,60))
		self.user.set_colores(colorbas = (0,153,255,255),
			colorbor = (0,153,255,255), colorcara = (0,153,255,255))
		self.user.set_tamanios(tamanio = (80,80), grosorbor = 1, detalle = 1, espesor = 1)
		ww, hh = self.user.get_tamanio()
		w,h = RESOLUCION
		self.user.set_posicion(punto = (w - ww - 10, 25))
		self.user.connect(callback = None, sonido_select = None)
		self.add(self.user)

		imagen= get_Flecha()
		self.flecha= JAMButton("",None)
		self.flecha.set_imagen(origen= imagen, tamanio=(100,55))
		self.flecha.set_colores(colorbas=JAMG.get_negro(), colorcara=JAMG.get_negro())
		self.flecha.set_tamanios(tamanio=(0,0), grosorbor=1, detalle=1, espesor=1)
		self.flecha.set_posicion(punto= (10,10))
		self.flecha.connect (callback= self.main.run_dialog_game)
		self.add(self.flecha)

		x,y= self.flecha.posicion
		w,h= self.flecha.get_tamanio()
		x+= w
		ancho= RESOLUCION[0]/2 - x
		cartel_titulo= pygame.sprite.Sprite()
		cartel_titulo.image= get_Imagen_Cartel1()
		cartel_titulo.image= pygame.transform.scale(cartel_titulo.image.copy(), (ancho,cartel_titulo.image.get_size()[1]))
		cartel_titulo.rect= cartel_titulo.image.get_rect()
		cartel_titulo.rect.x= x
		cartel_titulo.rect.y= -60
		self.add(cartel_titulo)

		self.titulo= JAMLabel(self.main.nombre)
		self.titulo.set_text(color=JAMG.get_blanco())
		fuente, tamanio= JAMG.get_Font_fawn()
		self.titulo.set_font_from_file(fuente, tamanio= 40)
		w,h= RESOLUCION
		x,y= (cartel_titulo.rect.x + 50, 10)
		self.titulo.set_posicion(punto= (x,y))
		self.add(self.titulo)

		self.puntaje= JAMLabel("%s" %(self.main.puntos))
		self.puntaje.set_text(color=JAMG.get_blanco())
		fuente, tamanio= JAMG.get_Font_fawn()
		self.puntaje.set_font_from_file(fuente, tamanio= 40)
		w,h= RESOLUCION
		self.add(self.puntaje)

		self.sonidos_reloj= get_sound_clock()

		from BiblioJAM.JAMCron import JAMCron
		self.cronometro= JAMCron()
		x,y= (0-self.cronometro.cron.rect.w-1, 0-self.cronometro.cron.rect.h-1)
		self.cronometro.cron.set_posicion(punto= (x,y))
		self.cronometro.set_callback(self.main.game_over)
		self.cronometro.set_alarma(tiempo = (1,30), duracion = 3)
		self.add(self.cronometro)

		self.progress_reloj= ProgressBar(self.main)
		self.add(self.progress_reloj)

	def actualiza_puntos(self):
		puntos = "%s" %(self.main.puntos)
		self.puntaje.set_text(texto= puntos)
		x,y = self.user.get_posicion()
		w,h = self.puntaje.get_tamanio()
		x -= w+10
		self.puntaje.set_posicion(punto= (x,y))

	def switching_game(self, button):
		self.main.estado= "Intro"
		return self.main.run()

	def init(self):
		sound= self.sonidos_reloj[0]
		self.cronometro.set_sound(sound)
		self.cronometro.reset()
		self.actualiza_puntos()
		self.cronometro.play()
	def stop(self):
		self.cronometro.pause()
	def play(self):
		self.cronometro.play()

class ProgressBar(pygame.sprite.Sprite):
	def __init__(self, main):
		pygame.sprite.Sprite.__init__(self)
		self.main = main
		self.acumula = 0
		w,h = RESOLUCION
		self.tamanio = (w/2-10,10)
		self.posicion = (w/2,10)
		rect1 = JAMG.get_Rectangulo( JAMG.get_verde1(), self.tamanio)
		w,y = rect1.get_size()
		a = w/6*3
		rect2 = JAMG.get_Rectangulo( JAMG.get_amarillo1(), (a,self.tamanio[1]))
		imagen = JAMG.pegar_imagenes_alineado_derecha(rect2, rect1)
		a = w/6
		rect3 = JAMG.get_Rectangulo( JAMG.get_rojo1(), (a,self.tamanio[1]))
		self.imagen_original = JAMG.pegar_imagenes_alineado_derecha(rect3, imagen)
		self.image = self.imagen_original.copy()
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y= self.posicion

	def update(self):
		tiempo = self.main.controles.cronometro.cron.segundos_final
		transcurridos = self.main.controles.cronometro.get_tiempo_transcurrido()
		faltan = self.main.controles.cronometro.cron.segundos_faltan
		mitad = tiempo/2
		cuarto = tiempo/4
		if faltan <= mitad:
			if faltan > cuarto:
				if not self.main.controles.cronometro.sonido == self.main.controles.sonidos_reloj[1]:
					self.main.controles.stop()
					self.main.controles.cronometro.set_sound(self.main.controles.sonidos_reloj[1])
					self.main.controles.play()
			elif faltan <= cuarto:
				if not self.main.controles.cronometro.sonido == self.main.controles.sonidos_reloj[2]:
					self.main.controles.stop()
					self.main.controles.cronometro.set_sound(self.main.controles.sonidos_reloj[2])
					self.main.controles.play()
		ancho, alto = self.tamanio
		ind = float(float(ancho)/float(self.main.controles.cronometro.cron.segundos_final))
		ancho = float(float(ancho)- float(self.main.controles.cronometro.get_tiempo_transcurrido())*ind)
		dif = float(float(self.tamanio[0]) - float(ancho))
		try:
			self.image = self.imagen_original.copy().subsurface((dif,0,int(ancho), int(alto)))
		except:
			self.image = self.imagen_original.copy().subsurface((dif,0,0,0))
		self.rect = self.image.get_rect()
		x,y = self.posicion
		x += dif
		self.rect.x, self.rect.y = (x,y)

