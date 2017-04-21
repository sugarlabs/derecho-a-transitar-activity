#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Globals.py por: Flavio Danesse fdanesse@gmail.com
#   https://sites.google.com/site/flaviodanesse/
#   https://sites.google.com/site/sugaractivities/
#   http://codigosdeejemplo.blogspot.com/

import pygame, gc, sys, os, random, platform
from pygame.locals import *
gc.enable()

if "olpc" in platform.platform():
	os.environ['SDL_AUDIODRIVER'] = 'alsa'

DIRECTORIO_BASE= os.path.dirname(__file__)

def Traduce_posiciones(VA, VH):
# Escala eventos de Posición
	eventos= pygame.event.get(pygame.MOUSEBUTTONDOWN)
	for event in eventos:
		x, y = event.pos
		xx= x/VA
		yy= y/VH
		event_pos= (xx, yy)
	for event in eventos:
		evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos= event_pos, button=event.button)
		pygame.event.post(evt)

	eventos= pygame.event.get(pygame.MOUSEMOTION)
	for event in eventos:
		x, y = event.pos
		xx= x/VA
		yy= y/VH
		event_pos= (xx, yy)
	for event in eventos:
		evt = pygame.event.Event(pygame.MOUSEMOTION, pos= event_pos, rel=event.rel, buttons=event.buttons)
		pygame.event.post(evt)

# ---- Generales
RESOLUCION = (1200,900)
def get_Fondo_Inicial():
	return pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/Pantalla-Inicio.jpg"), RESOLUCION)
def get_Fondo():
	return pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/fondo1.jpg"), (1200,900))
def get_Flecha():
	return (DIRECTORIO_BASE+"/Imagenes/flecha.png")
def get_Sonidos():
	frenada1= pygame.mixer.Sound(DIRECTORIO_BASE+"/Sonidos/frenada1.ogg")
	aplausos1= pygame.mixer.Sound(DIRECTORIO_BASE+"/Sonidos/aplausos1.ogg")
	return frenada1, aplausos1
def get_ambiente():
	ambiente= None#pygame.mixer.music.load(DIRECTORIO_BASE+"/Sonidos/ambiente.ogg")
	return ambiente
def get_Imagen_Cartel1():
	''' Devuelve la imagen para los carteles. '''
	return pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/cartel1.png"), (276,145))
def get_Imagen_CartelMenu():
	''' Devuelve la imagen para los carteles. '''
	un= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/cartel2.png"), (250,162))
	dos= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/cartel3.png"), (250,162))
	return (un, dos)
def get_Imagen_Gruber1():
	return pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/cebra1.png"), (250,310))
def get_Imagen_Gruber2():
	return pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/cebra2.png"), (250,310))
def get_Imagen_Gruber3():
	return pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/cebra3.png"), (250,310))
	
def get_sound_clock():
	clock1= pygame.mixer.Sound(DIRECTORIO_BASE+"/Sonidos/clock_tick1.ogg")
	clock2= pygame.mixer.Sound(DIRECTORIO_BASE+"/Sonidos/clock_tick2.ogg")
	clock3= pygame.mixer.Sound(DIRECTORIO_BASE+"/Sonidos/clock_tick3.ogg")
	return [clock1, clock2, clock3]
def get_instruc(name):
	return pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/Instructivos/%s.jpg" % (name)), (1200,900))
def get_Presentacion():
	directorio= DIRECTORIO_BASE+"/Imagenes/Presentacion/"
	imagenes= []
	for archivo in os.listdir(directorio):
		imagen= pygame.transform.scale(pygame.image.load(directorio + "%s" % (archivo)), (1200,900))
		imagenes.append(imagen)
	return imagenes
def get_cartel_presenta():
	img1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/pandilla1.png"), (175,175))
	img2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/pandilla2.png"), (175,175))
	return img1, img2
# -------------  T0101  -------------
# Imagenes:
def get_Fondos_FGR_T0101():
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0101/fondo1.jpg"), (1200,900))
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0101/fondo2.jpg"), (1200,900))
	return (fondo1, fondo2)

def get_Seniales_FGR_T0101():
	''' Devuelve las señales y sus posiciones. '''
	seniales= {}
	seniales["Sentido obligatorio"]= (pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/Seniales1/senial1.png"),(145,145)))
	seniales["Curva Peligrosa"]= (pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/Seniales1/senial2.png"),(145,145)))
	seniales["Prohibido Adelantar o Rebasar"]= (pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/Seniales1/senial3.png"),(145,145)))
	seniales["¡Peligro! Paso a nivel sin barrera"]= (pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/Seniales1/senial4.png"),(145,145)))
	seniales["Prohibido acceso a peatones"]= (pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/Seniales1/senial5.png"),(145,145)))
	return seniales
def get_Posicion_Seniales_FGR_T0101():
	return [(190,323), (395,272), (600,339), (805,269), (1010,338)]

def get_Carteles_FGR_T0101():
	''' Devuelve los textos de los carteles. '''
	carteles= {}
	carteles["Sentido obligatorio"]= None
	carteles["Curva Peligrosa"]= None
	carteles["Prohibido Adelantar o Rebasar"]= None
	carteles["¡Peligro! Paso a nivel sin barrera"]= None
	carteles["Prohibido acceso a peatones"]= None
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
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0102/fondo1.jpg"), (1200,900))
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0102/fondo2.jpg"), (1200,900))
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
# Imagenes:
def get_Fondos_FGR_T0103():
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0103/fondo1.jpg"), (1200,900))
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0103/fondo2.jpg"), (1200,900))
	return (fondo1, fondo2)

# Textos:
INTRO_FGR_T0103= ''' . . . . . . . . . '''
def get_Textos_FGR_T0103():
	textos= []
	for linea in INTRO_FGR_T0103.split("\n"):
		textos.append(linea)
	return textos

def get_frases_FGR_T0103():
	return {"Sólo cruzamos cuando el semáforo está en verde de forma fija.": True,
		"Estamos atentos a las señales de tránsito posicionadas en un palo vertical, y también a las marcas viales, las señales, pintadas sobre el pavimento o calzada.":False, "Cumplimos siempre las indicaciones que nos comunican las señales de tránsito. Somos conscientes de que cumplirlas es muy importante.": True, "Cuando vemos una señal de peligro, extremamos la prudencia.": True, "Jamás cruzamos la calle con semáforo en rojo, aunque no circulen vehículos por la calzada.": True, "Si circulamos en bicicleta y vemos un stop, lo respetamos": False, "Si una calle es peatonal (porque así lo indica una señal de tránsito), hacemos caso a la señal y no circulamos por ella en bicicleta.": False, "Si vamos en bicicleta y vemos una señal de peligro o prevención, que indica que por donde estamos circulando suelen haber niños y niñas, extremamos las precauciones.": True, "Si vemos a un amigo o amiga no cumplir la indicación de una señal de tráfico, le explicamos que si todo el mundo respeta las señales de tránsito se evitanrían la mayor parte de los accidentes de circulación.": False, "Sólo cruzamos la calle por el paso o senda peatonal, aunque el semáforo esté en verde.": True}

# -------------  T0103  -------------


# -------------  T0201  -------------
# Imagenes:
def get_Fondos_FGR_T0201():
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0201/fondo1.jpg"), (1200,900))
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0201/fondo2.jpg"), (1200,900))
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
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/fondo1.jpg"), (1200,900))
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0202/fondo2.jpg"), (1200,900))
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
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0301/fondo1.jpg"), (1200,900))
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0301/fondo2.jpg"), (1200,900))
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
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/fondo1.jpg"), (1200,900))
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0302/fondo2.jpg"), (1200,900))
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
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0401/fondo1.jpg"), (1200,900))
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0401/fondo2.jpg"), (1200,900))
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
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0501/fondo1.jpg"), (1200,900))
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0501/fondo2.jpg"), (1200,900))
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
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0303/fondo1.jpg"), (1200,900))
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0303/fondo2.jpg"), (1200,900))
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
	fondo1= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/fondo1.jpg"), (1200,900))
	fondo2= pygame.transform.scale(pygame.image.load(DIRECTORIO_BASE+"/Imagenes/FGR_T0402/fondo2.jpg"), (1200,900))
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
