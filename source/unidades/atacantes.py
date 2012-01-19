import engine
from unidades.defensores import Nenufar
import re
from engine import Grilla

class Atacante(object):
    url_imagen_1 = None
    url_imagen_2 = None
    imagen1 = None
    imagen2 = None
    cantidad = (1, 1)
    def __new__(cls, *args, **kargs):
        if not cls.imagen1:
            cls.imagen1 = engine.cargar_imagen(cls.url_imagen_1, True)
            cls.imagen2 = engine.cargar_imagen(cls.url_imagen_2, True)
        return object.__new__(cls, *args, **kargs)
    def __init__(self, i, w, h):
        self.w = w
        self.h = h
        self.i = i
        self.j = 10
        self.grilla = Grilla(self.url_imagen_1, self.cantidad[0], self.cantidad[1])
        self.rect_real = engine.pygame.Rect(0, 0, self.grilla.ancho, self.grilla.alto)
        self.rect_real.centerx = self.w * (self.j + 1)
        self.rect_real.bottom = 120 + self.h * (i + 1)
        self.rect = engine.pygame.Rect(0, 0, 15, self.grilla.alto)
        self.intervalo_movimiento = 0.8
        self.intervalo_animacion = 0.1
        self.crono_i_m = 0
        self.crono_i_a = 0
        self.salud = 100
        self.danio = 30
        self.detenido = False
        self.congelado = False
        self.duracion_congelado = 2
        self.crono_i_c = 0
        self.imagen = self.imagen1
    @property
    def cuadro_actual(self):
        return self.grilla.obtener_cuadro(self.cuadros[self.actual])
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect_real, self.cuadro_actual)
    def actualizar(self, tiempo):
        if self.congelado and engine.pygame.time.get_ticks() - self.crono_i_c > self.duracion_congelado * 1000:
            self.descongelar()
    def congelar(self):
        self.crono_i_c = engine.pygame.time.get_ticks()
        if not self.congelado:
            for i in self.__dict__:
                self.congelado = True
                if re.match("\Aintervalo_.*", i):
                    exec("self.{}=self.{}*4".format(i, i))
            self.imagen = self.imagen2
    def descongelar(self):
        if self.congelado:
            self.congelado = False
            self.imagen = self.imagen1
            for i in self.__dict__:
                if re.match("\Aintervalo_.*", i):
                    exec("self.{}=self.{}/4.0".format(i, i))
                
class Zombie(Atacante):
    url_imagen_1 = "zombies.png"
    url_imagen_2 = "zombiescongelados.png"
    cantidad = (7, 2)
    def __init__(self, i, w, h):
        Atacante.__init__(self, i, w, h)
        self.cuadros_caminando = [0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 0]
        self.cuadros_comiendo = [7, 8, 9, 10, 8]
        self.cuadros = self.cuadros_caminando
        self.actual = 0
        self.intervalo_golpe = 2
        self.crono_i_g = 0
        self.danio = 30
        self.salud = 150
        self.detenido = False
    def actualizar(self, tiempo):
        Atacante.actualizar(self, tiempo)
        self.rect.center = self.rect_real.center
        if self.detenido:
            self.detenido = False
            for fila in engine.obtener_director().escena_actual.tablero:
                if not self.detenido:
                    for d in fila:
                        if d:
                            if d.i == self.i and d.j == self.j:
                                if engine.pygame.time.get_ticks() - self.crono_i_g > self.intervalo_golpe * 1000:
                                    self.crono_i_g = engine.pygame.time.get_ticks()
                                    if d.__class__ == Nenufar and d.contenido:
                                        d.contenido.salud -= self.danio
                                    else:
                                        d.salud -= self.danio
                                self.detenido = True
                                break
            if not self.detenido:
                self.cuadros = self.cuadros_caminando
                self.actual = 0
                self.intervalo_animacion = self.intervalo_animacion / 5.0
        else:
            if engine.pygame.time.get_ticks() - self.crono_i_m > self.intervalo_movimiento * 1000:
                self.crono_i_m = engine.pygame.time.get_ticks()
                avance = 10 if self.actual != 0 else 20
                self.rect_real.x -= avance 
                self.j = (self.rect_real.x - 50) / 100
            for fila in engine.obtener_director().escena_actual.tablero:
                if not self.detenido:
                    for d in fila:
                        if d:
                            if d.i == self.i and d.j == self.j:
                                self.detenido = True
                                self.cuadros = self.cuadros_comiendo
                                self.actual = 0
                                self.intervalo_animacion = self.intervalo_animacion * 5
                                break
        if engine.pygame.time.get_ticks() - self.crono_i_a > self.intervalo_animacion * 1000:
            self.crono_i_a = engine.pygame.time.get_ticks()
            self.actual += 1
            if self.actual > len(self.cuadros) - 1:
                self.actual = 0
        if self.salud <= 0:
            engine.obtener_director().escena_actual.atacantes.remove(self)
