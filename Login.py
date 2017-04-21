#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import os
import gc
import sys
import gtk
import gobject

from pygame.locals import *
import Globals as G
gc.enable()
import BiblioJAM
from BiblioJAM.JAMButton import JAMButton
from BiblioJAM.JAMLabel import JAMLabel
import BiblioJAM.JAMGlobals as JAMG

class Login(gtk.Widget):
	__gsignals__ = {"run":(gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, []),
	"crear_usuario":(gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, []),
	"load_usuario":(gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))}
	def __init__(self):
		gtk.Widget.__init__(self)
		self.ventana = None
		self.estado = False
		self.fondo = None
		self.reloj = None
		self.selector = None
		self.ventana_real = None
		self.resolucionreal = None
		self.VA = None
		self.VH = None
		self.load()
		self.estado = "Intro"

	def run(self):
		self.ventana.blit(self.fondo, (0,0))
		self.selector.draw(self.ventana)
		pygame.display.update()
		while self.estado == "Intro":
			self.reloj.tick(35)
			while gtk.events_pending():
			    	gtk.main_iteration(False)
			G.Traduce_posiciones(self.VA, self.VH)
			self.selector.clear(self.ventana, self.fondo)
			self.selector.update()
			self.handle_event_Intro()
			pygame.event.clear()
			self.selector.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
			pygame.display.update()

	def run_game(self, button):
		self.estado = None
		self.emit("run")

	def crear_usuario(self, button):
		self.estado = None
		self.emit("crear_usuario")
	
	def emit_load_usuario(self, usuario):
		self.estado = None
		self.emit("load_usuario", usuario)

	def handle_event_Intro(self):
		for event in pygame.event.get(pygame.KEYDOWN):
			tecla = event.key
			if tecla == pygame.K_ESCAPE:
				return self.run_dialog_intro(None)

	def load(self):
		pygame.display.set_mode( (0,0), pygame.DOUBLEBUF | pygame.FULLSCREEN, 0)
		A, B = G.RESOLUCION
		self.ventana = pygame.Surface( (A, B), flags=HWSURFACE )
		self.ventana_real = pygame.display.get_surface()
		C = pygame.display.Info().current_w
		D = pygame.display.Info().current_h
		self.resolucionreal = (C,D)
		self.VA = float(C)/float(A)
		self.VH = float(D)/float(B)
		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION,
			JOYBUTTONUP, JOYBUTTONDOWN, KEYUP, USEREVENT])
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN,
			KEYDOWN, VIDEORESIZE, VIDEOEXPOSE, QUIT, ACTIVEEVENT])
		pygame.mouse.set_visible(True)
		imagen = os.path.join(G.IMAGENES, "Login", "fondo.jpg")
		self.fondo = pygame.transform.scale(pygame.image.load(imagen), G.RESOLUCION)
		self.reloj = pygame.time.Clock()
		self.selector = Selector(self)
		self.selector.center(self.fondo.get_size())

	def run_dialog_intro(self, button):
		from BiblioJAM.JAMDialog import JAMDialog
		dialog = JAMDialog(mensaje = "¿Abandonas el Juego?",
		funcion_ok = self.ok_intro, funcion_cancel = self.cancel_intro)
		fuente, tamanio = JAMG.get_Font_fawn()
		dialog.set_font_from_file(fuente, tamanio = 40)
		dialog.boton_aceptar.set_font_from_file(fuente, tamanio = 25)
		dialog.boton_cancelar.set_font_from_file(fuente, tamanio = 25)
		a,b,c = JAMG.get_estilo_papel_quemado()
		dialog.set_colors_dialog(base = c, bordes = c)
		dialog.set_colors_buttons(colorbas = a, colorbor = b, colorcara = c) 
		self.estado = "Dialog"
		dialog.draw(self.ventana)
		pygame.display.update()
		while self.estado == "Dialog":
			self.reloj.tick(35)
			while gtk.events_pending():
			    	gtk.main_iteration(False)
			G.Traduce_posiciones(self.VA, self.VH)
			dialog.clear(self.ventana, self.fondo)
			dialog.update()
			pygame.event.clear()
			dialog.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana,
				self.resolucionreal), (0,0))
			pygame.display.update()
		dialog.clear(self.ventana, self.fondo)
		self.ventana_real.blit(pygame.transform.scale(self.ventana,
			self.resolucionreal), (0,0))
		pygame.display.update()

	def ok_intro(self, button):
		return self.salir()
	def cancel_intro(self, button):
		self.estado = "Intro"
	def salir(self):
		pygame.quit()
		sys.exit()

class Selector(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		fuente, tamanio= JAMG.get_Font_fawn()
		self.main = main
		self.posiciones_usuarios = (0,0)
		imagen = os.path.join(G.IMAGENES, "Login", "fondo_selecciona.png")
		imagen = pygame.transform.scale(pygame.image.load(imagen), (427,573))
		self.fondo = pygame.sprite.Sprite()
		self.fondo.image = (imagen)
		self.fondo.rect = self.fondo.image.get_rect()
		self.add(self.fondo)

		self.label = JAMLabel("Selecciona tu Usuario")
		self.label.set_font_from_file(fuente, tamanio = 40)
		self.label.set_text(color = (255,255,255,255))
		self.add(self.label)

		imagen = G.get_Flecha()
		salir = JAMButton("",None)
		salir.set_imagen(origen = imagen, tamanio = (100,55))
		salir.set_colores(colorbas = JAMG.get_negro(), colorcara = JAMG.get_negro())
		salir.set_tamanios(tamanio = (0,0), grosorbor = 1, detalle = 1, espesor = 1)
		salir.set_posicion(punto = (10,10))
		salir.connect(callback = main.run_dialog_intro)
		self.add(salir)

		self.upper = BotonScroll()
		self.upper.set_imagen("up")
		self.upper.connect(callback = self.up_user, sonido_select = None)
		self.add(self.upper)

		self.down = BotonScroll()
		self.down.set_imagen("down")
		self.down.connect(callback = self.down_user, sonido_select = None)
		self.add(self.down)

		usuarios = G.get_users()
		self.usuarios = []
		for user in usuarios:
			usuario = Usuario(user)
			usuario.connect(callback = self.emit_load_usuario, sonido_select = None)
			self.usuarios.append(usuario)

		self.usuariosenmenu = None
		if len(self.usuarios) <= 3:
			self.usuariosenmenu = self.usuarios
		else:
			self.usuariosenmenu = self.usuarios[:3]
		if self.usuariosenmenu: self.add(self.usuariosenmenu)

		self.crear = JAMButton("Crear Nuevo",None)
		self.crear.set_tamanios(grosorbor = 1, detalle = 1, espesor = 1)
		self.crear.set_font_from_file(fuente, tamanio = 25)
		self.crear.set_colores(colorbas = (0,157,224,255),
			colorbor = (0,157,224,255), colorcara = (92,193,235,255))
		self.crear.set_text(color=(255,255,255,255))
		self.crear.connect(callback = main.crear_usuario, sonido_select = None)
		self.add(self.crear)

	def up_user(self, button):
		if len(self.usuarios) <= 3:
			return
		else:
			indice = self.usuarios.index(self.usuariosenmenu[0])
			indice -= 1
			usuarios = [self.usuarios[indice], self.usuariosenmenu[0], self.usuariosenmenu[1]]
			self.remove(self.usuariosenmenu)
			self.usuariosenmenu = usuarios
			self.set_posiciones_usuarios()
			self.add(self.usuariosenmenu)

	def down_user(self, button):
		if len(self.usuarios) <= 3:
			return
		else:
			indice = self.usuarios.index(self.usuariosenmenu[-1])
			if indice == len(self.usuarios)-1:
				indice = 0
			else:
				indice += 1
			usuarios = [self.usuariosenmenu[1], self.usuariosenmenu[2], self.usuarios[indice]]
			self.remove(self.usuariosenmenu)
			self.usuariosenmenu = usuarios
			self.set_posiciones_usuarios()
			self.add(self.usuariosenmenu)

	def center(self, fondo_size):
		sep = 10

		a,b = self.label.get_tamanio()
		self.label.set_posicion( (fondo_size[0]/2-a/2, sep*2) )
		x,y, fondow, fondoh = self.fondo.rect
		ww,hh = fondo_size
		x,y = (ww/2-fondow/2,hh/2-fondoh/2)
		self.fondo.rect.x, self.fondo.rect.y = (x,y)

		w, h = self.upper.get_tamanio()
		posx, posy = (x+(fondow/2-w/2), y+sep)
		self.upper.set_posicion( (posx, posy) )

		w, h = self.down.get_tamanio()
		posx, posy = (x+(fondow/2-w/2), y+fondoh-h-sep)
		self.down.set_posicion( (posx, posy) )

		# usuarios
		x,y = self.upper.get_posicion()
		w,h = self.upper.get_tamanio()
		xx,yy = self.down.get_posicion()
		espacio = (yy-sep) - (y+h+sep)
		altura = espacio/3

		posy = y+h+sep
		self.posiciones_usuarios = (x, posy)
		for user in self.usuarios:
			user.set_tamanios(tamanio = (w, altura), grosorbor = 1, detalle = 1, espesor = 1)
			user.set_posicion( (x, posy) )
			posy += altura

		self.crear.set_tamanios(tamanio=(w,h), grosorbor=1, detalle=1, espesor=1)
		x,y,ww,h = self.fondo.rect
		self.crear.set_posicion( (fondo_size[0]/2-w/2, y+h+sep*2 ) )

	def emit_load_usuario(self, widget):
		self.main.emit_load_usuario(widget.usuario)

	def set_posiciones_usuarios(self):
		x, posy = self.posiciones_usuarios
		for user in self.usuariosenmenu:
			user.set_posicion( (x, posy) )
			posy += user.get_tamanio()[1]

class BotonScroll(JAMButton):
	def __init__(self):
		JAMButton.__init__(self, '', None)
	def set_imagen(self, origen):
		imagen = os.path.join(G.IMAGENES, "Login", "%s%s" % (origen, "1.png"))
		self.set_tamanios(tamanio = (376, 30), grosorbor=1, detalle=1, espesor=1)
		imagen = pygame.transform.scale(pygame.image.load(imagen), (376, 30))
		self.final_unselect = imagen

		imagen = os.path.join(G.IMAGENES, "Login", "%s%s" % (origen, "2.png"))
		self.final_select = pygame.transform.scale(pygame.image.load(imagen), (376, 30))
		self.image = self.final_unselect
		self.rect = self.image.get_rect()

class Usuario(JAMButton):
	def __init__(self, usuario):
		JAMButton.__init__(self, '', None)
		fuente, tamanio= JAMG.get_Font_fawn()
		self.usuario = usuario # diccionario cargado desde archivo shelve.
		imagen = self.usuario['personaje']
		self.set_imagen(origen = imagen)
		self.set_alineacion_label("izquierda")
		self.set_font_from_file(fuente, tamanio = 25)
		self.set_text(texto = self.usuario['nombre'], color = (255,255,255,255))
		self.set_colores(colorbas = (0,157,224,255),
			colorbor = (0,157,224,255), colorcara = (92,193,235,255))

