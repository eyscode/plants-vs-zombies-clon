import engine
from habilidades import DispararNormal, DispararTodoSentido, ProducirSol
from engine import Grilla
from unidades.habilidades import Explotar
import re

class Defensor(object):
    url_imagen = None
    imagen = None
    cuadro_alpha = 0
    cantidad = (1, 1)
    def __new__(cls, *args, **kargs):
        if not cls.imagen: cls.imagen = engine.cargar_imagen(cls.url_imagen, True)
        return object.__new__(cls, *args, **kargs)
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.grilla = Grilla(self.url_imagen, self.cantidad[0], self.cantidad[1])
        self.rect = engine.pygame.Rect(0, 0, self.grilla.ancho, self.grilla.alto)
        self.rect.right = 50 + engine.obtener_director().escena_actual.ancho_cuadro * (j + 1)
        self.rect.bottom = 120 + engine.obtener_director().escena_actual.alto_cuadro * (i + 1)
        self.intervalo_animacion = 0.15
        self.crono_i_a = engine.pygame.time.get_ticks()
        self.salud = 100
        self.actual = 0
        self.habilidades = []
    @property
    def cuadro_actual(self):
        return self.grilla.obtener_cuadro(self.cuadros[self.actual])
    def aprender_habilidad(self, classname, *args):
        habilidades_actuales = [habilidad.__class__ for habilidad in self.habilidades]
        if classname not in habilidades_actuales:
            self.habilidades.append(classname(self, args))
    def olvidar_habilidad(self, classname):
        for h in self.habilidades:
            if h.__class__ == classname:
                self.habilidades.remove(h)
                break
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect, self.cuadro_actual)
    def actualizar(self, tiempo):
        if self.salud <= 0:
            if engine.obtener_director().escena_actual.tablero[self.i][self.j].__class__ == Nenufar and engine.obtener_director().escena_actual.tablero[self.i][self.j].contenido:
                engine.obtener_director().escena_actual.tablero[self.i][self.j].contenido = None
            else:
                engine.obtener_director().escena_actual.tablero[self.i][self.j] = 0
        if engine.pygame.time.get_ticks() - self.crono_i_a > self.intervalo_animacion * 1000:
            self.crono_i_a = engine.pygame.time.get_ticks()
            self.actual += 1
            if self.actual > len(self.cuadros) - 1:
                self.actual = 0
        self.actualizar_habilidades(tiempo)
    def actualizar_habilidades(self, tiempo):
        for h in self.habilidades:
            h.actualizar(tiempo)
    def sincronizar_cronos_pausa(self, t):
        nroh = 0
        for h in self.habilidades:
            for i in h.__dict__:
                if re.match("\Acrono_i_.*", i):
                    exec("self.habilidades[nroh].{}=self.habilidades[nroh].{}+t".format(i, i))
            nroh += 1

class Girasol(Defensor):
    url_imagen = "girasol.png"
    cantidad = (3, 1)
    def __init__(self, i, j):
        Defensor.__init__(self, i, j)
        self.cuadros = [0, 1, 0, 2]
        self.salud = 120
        self.aprender_habilidad(ProducirSol)

class LanzaGuisantes(Defensor):
    url_imagen = "planta.png"
    cantidad = (3, 1)
    def __init__(self, i, j):
        Defensor.__init__(self, i, j)
        self.cuadros = [0, 1, 0, 2]
        self.salud = 170
        self.aprender_habilidad(DispararNormal)

class HielaGuisantes(Defensor):
    url_imagen = "hielo.png"
    cantidad = (3, 1)
    def __init__(self, i, j):
        Defensor.__init__(self, i, j)
        self.cuadros = [0, 1, 0, 2]
        self.salud = 175
        self.aprender_habilidad(DispararNormal, True)
        
class Nenufar(Defensor):
    url_imagen = "nenufar.png"
    cantidad = (1, 1)
    def __init__(self, i, j):
        Defensor.__init__(self, i, j)
        self.cuadros = [0]
        self.salud = 80
        self.contenido = None
    def dibujar(self, superficie):
        Defensor.dibujar(self, superficie)
        if self.contenido: self.contenido.dibujar(superficie)
    def actualizar(self, tiempo):
        Defensor.actualizar(self, tiempo)
        if self.contenido: self.contenido.actualizar(tiempo)
        
class ColaDeGato(Defensor):
    url_imagen = "gato.png"
    cantidad = (5, 1)
    def __init__(self, i, j):
        super(ColaDeGato, self).__init__(i, j)
        self.cuadros_ataque = [1, 0, 3, 4, 3, 0, 1, 2]
        self.cuadros_normal = [1, 1, 1, 1, 0, 0, 0, 0]
        self.cuadros = self.cuadros_normal
        self.salud = 200
        self.intervalo_animacion = 0.125
        self.aprender_habilidad(DispararTodoSentido)
    def cambiar_animacion(self):
        if len(engine.obtener_director().escena_actual.atacantes) > 0 and self.cuadros != self.cuadros_ataque:
            self.cuadros = self.cuadros_ataque
            self.actual = 0
        elif len(engine.obtener_director().escena_actual.atacantes) == 0 and self.cuadros != self.cuadros_normal:
            self.cuadros = self.cuadros_normal
            self.actual = 0
    def actualizar(self, tiempo):
        Defensor.actualizar(self, tiempo)

class Nuez(Defensor):
    url_imagen = "nuez.png"
    cantidad = (5, 2)
    cuadro_alpha = 2
    def __init__(self, i, j):
        super(Nuez, self).__init__(i, j)
        self.cuadros_normal = [2, 1, 0, 1, 2, 3, 4, 3]
        self.cuadros_golpeado = [7, 6, 5, 6, 7, 8, 9, 8]
        self.cuadros = self.cuadros_normal
        self.salud = 800
        self.intervalo_animacion = 0.2
    def actualizar(self, tiempo):
        Defensor.actualizar(self, tiempo)
        if self.salud <= 350:
            self.cuadros = self.cuadros_golpeado
            
class PetaCereza(Defensor):
    url_imagen = "cereza.png"
    def __init__(self, i, j):
        Defensor.__init__(self, i, j)
        self.cuadros = [0]
        self.salud = 100
        self.aprender_habilidad(Explotar)
