import engine
from neutrales import Sol
from balas import Bala, Pua, Pumba
import random

class Habilidad(object):
    def __init__(self, objetivo):
        self.objetivo = objetivo
    def actualizar(self, tiempo):
        pass

class DispararNormal(Habilidad):
    def __init__(self, objetivo):
        Habilidad.__init__(self, objetivo)
        self.intervalo_disparo = 3
        self.crono_i_d = engine.pygame.time.get_ticks()
    def actualizar(self, tiempo):
        if len(engine.obtener_director().escena_actual.atacantes) > 0:
            if engine.pygame.time.get_ticks() - self.crono_i_d > self.intervalo_disparo * 1000:
                self.crono_i_d = engine.pygame.time.get_ticks()
                for a in engine.obtener_director().escena_actual.atacantes:
                    if a.i == self.objetivo.i and a.j >= self.objetivo.j:
                        engine.obtener_director().escena_actual.balas.append(Bala(self.objetivo.rect.centerx + 30, self.objetivo.rect.centery - 50))
                        break

class DispararTodoSentido(Habilidad):
    def __init__(self, objetivo):
        Habilidad.__init__(self, objetivo)
        self.intervalo_disparo = 2
        self.crono_i_d = 0
        self.contador = 2
        self.inicio = True
    def actualizar(self, tiempo):
        if self.contador == 2:
            self.intervalo_disparo = 2
            self.objetivo.cuadros = self.objetivo.cuadros_normal
        else:
            self.intervalo_disparo = 1
        if len(engine.obtener_director().escena_actual.atacantes) > 0 and self.inicio:
            self.crono_i_d = engine.pygame.time.get_ticks()
            self.inicio = False
        elif len(engine.obtener_director().escena_actual.atacantes) > 0 and not self.inicio:
            if engine.pygame.time.get_ticks() - self.crono_i_d > self.intervalo_disparo * 1000:
                self.crono_i_d = engine.pygame.time.get_ticks()
                self.contador += 1
                if self.contador > 2: self.contador = 0
                obj = engine.obtener_director().escena_actual.atacantes[0]
                for o in engine.obtener_director().escena_actual.atacantes:
                    if pow((((self.objetivo.rect.centerx - o.rect.centerx) ** 2) + ((self.objetivo.rect.centery - o.rect.centery) ** 2)), 0.5) < pow((((self.objetivo.rect.centerx - obj.rect.centerx) ** 2) + ((self.objetivo.rect.y - obj.rect.centery) ** 2)), 0.5):
                        obj = o
                if obj.i > self.objetivo.i: modo = 2
                elif obj.i < self.objetivo.i: modo = 1
                elif obj.i == self.objetivo.i and obj.j >= self.objetivo.j: modo = 0
                else: modo = -1
                if self.contador > 0:
                    engine.obtener_director().escena_actual.balas.append(Pua(self.objetivo.rect.centerx - 15, self.objetivo.rect.top, obj, modo, self.objetivo))
                self.objetivo.cuadros = self.objetivo.cuadros_ataque
                self.objetivo.actual = 0
        else:
            self.inicio = True
            self.objetivo.cuadros = self.objetivo.cuadros_normal

class ProducirSol(Habilidad):
    def __init__(self, objetivo):
        Habilidad.__init__(self, objetivo)
        self.intervalo_produccion = 12
        self.crono_i_p = engine.pygame.time.get_ticks()
    def actualizar(self, tiempo):
        if engine.pygame.time.get_ticks() - self.crono_i_p > self.intervalo_produccion * 1000:
            self.crono_i_p = engine.pygame.time.get_ticks()
            xfinal = random.randint(self.objetivo.rect.left, self.objetivo.rect.right)
            yfinal = self.objetivo.rect.top - (self.objetivo.rect.height / 4)
            x, y = self.objetivo.rect.center
            sol_producido = Sol(x, y, y)
            engine.obtener_director().escena_actual.solsitos.append(sol_producido)
            engine.obtener_director().escena_actual.tweener.addTween(sol_producido, x = xfinal, y = yfinal, tweenTime = 0.3, tweenType = engine.pytweener.Easing.Linear.easeIn)

class Explotar(Habilidad):
    def __init__(self, objetivo):
        Habilidad.__init__(self, objetivo)
        self.w = self.objetivo.imagen.get_width()
        self.h = self.objetivo.imagen.get_height()
        self.imagen_original = self.objetivo.imagen
        engine.obtener_director().escena_actual.tweener.addTween(self, w = 135, h = 135, tweenTime = 2.0, tweenType = engine.pytweener.Easing.Linear.easeIn, onCompleteFunction = self.matar)
    def matar(self):
        engine.obtener_director().escena_actual.explosiones.append(Pumba(self.objetivo.rect.centerx, self.objetivo.rect.centery, self.objetivo))
        self.objetivo.salud = -1
    def actualizar(self, tiempo):
        self.objetivo.imagen = engine.pygame.transform.scale(self.imagen_original, (int(self.w), int(self.h)))
        self.objetivo.rect.width = int(self.w)
        self.objetivo.rect.height = int(self.h)
        self.objetivo.rect.centerx = 50 + engine.obtener_director().escena_actual.ancho_cuadro * (self.objetivo.j + 1) - engine.obtener_director().escena_actual.ancho_cuadro / 2
        self.objetivo.rect.bottom = 120 + engine.obtener_director().escena_actual.alto_cuadro * (self.objetivo.i + 1)
        self.objetivo.grilla.cuadros[0].width = int(self.w)
        self.objetivo.grilla.cuadros[0].height = int(self.h)
