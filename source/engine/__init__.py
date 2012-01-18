import pygame
import os
from math import floor
inicializado = False
media_url = ""
os.environ['SDL_VIDEO_CENTERED'] = '1'
director = None
cursor = None
usuario = None


def redondear(n):
    r = n - floor(n)
    r = 1 if r >= 0.5 else 0
    return floor(n) + r

class Grilla(object):
    def __init__(self, url_img, nro_h, nro_v = 1):
        self.nro_cuadros_h = nro_h
        self.nro_cuadros_v = nro_v
        self.ancho = cargar_imagen(url_img).get_rect().width / self.nro_cuadros_h
        self.alto = cargar_imagen(url_img).get_rect().height / self.nro_cuadros_v
        self.cuadros = []
        for n in range(0, self.nro_cuadros_h * self.nro_cuadros_v):
            columna = n % self.nro_cuadros_h
            fila = n / self.nro_cuadros_h
            self.cuadros.append(pygame.Rect(columna * self.ancho, fila * self.alto , self.ancho, self.alto))
    def obtener_cuadro(self, nro):
        return self.cuadros[nro]

class Cursor:
    def __init__(self):
        self.normal = cargar_imagen("normal.png", True)
        self.arrastrando = cargar_imagen("arrastrando.png", True)
        self.imagen = self.normal
        self.rect = self.imagen.get_rect()
        self.mask = pygame.mask.from_surface(self.imagen, 127)
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)
    def actualizar(self, tiempo):
        self.rect.x, self.rect.y = pygame.mouse.get_pos()
    def cambiar_normal(self):
        self.imagen = self.normal
        self.mask = pygame.mask.from_surface(self.imagen, 127)
    def cambiar_arrastrando(self):
        self.imagen = self.arrastrando
        self.mask = pygame.mask.from_surface(self.imagen, 127)

def inicializar():
    global inicializado
    inicializado = True
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

def definir_dimension(w = 1000, h = 750):
    if inicializado:
        global cursor
        a = pygame.display.set_mode((w, h))
        cursor = Cursor()
        #pygame.mouse.set_visible(False)
        return a
    else:
        raise Exception("Aun no se ha inicializado el engine")

def definir_media(url):
    global media_url
    media_url = url + "/"
    
def definir_titulo(titulo):
    if inicializado:
        pygame.display.set_caption(titulo)
    else:
        raise Exception("Aun no se ha inicializado el engine")

def definir_icono(icono):
    if inicializado:
        pygame.display.set_icon(pygame.image.load(media_url + icono))
    else:
        raise Exception("Aun no se ha inicializado el engine")
    
def cargar_imagen(url_imagen, transparencia = False):
    if inicializado:
        if transparencia:
            return pygame.image.load(media_url + url_imagen).convert_alpha()
        else:
            return pygame.image.load(media_url + url_imagen).convert()
    else:
        raise Exception("Aun no se ha inicializado el engine")

def definir_director(direc):
    global director
    director = direc

def obtener_director():
    global director
    if director == None:
        raise Exception("Aun no se ha establecido un director al engine")
    return director

def definir_usuario(user):
    global usuario
    usuario = user

def obtener_usuario():
    global usuario
    return usuario
    
def cargar_sonido(url_sonido):
    pass

def cambiar_puntero():
    pass

def cambiar_mano():
    pass
