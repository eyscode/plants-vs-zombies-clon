import engine
from engine import redondear, Grilla
import math

class Disparo(object):
    imagen = None
    sombra = None
    url_imagen = None
    url_sombra = "sombra.png"
    cantidad = (1, 1)
    def __new__(cls, *args, **kwargs):
        if not cls.imagen: 
            cls.imagen = engine.cargar_imagen(cls.url_imagen, True)
            cls.sombra = engine.cargar_imagen(cls.url_sombra, True)
        return object.__new__(cls, *args, **kwargs)
    def __init__(self, x, y):
        self.grilla = Grilla(self.url_imagen, self.cantidad[0], self.cantidad[1])
        self.rect = engine.pygame.Rect(0, 0, self.grilla.ancho, self.grilla.alto)
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 3
        self.crono_i_m = 0
        self.crono_i_a = 0
        self.intervalo_movimiento = 0.001
        self.intervalo_animacion = 0.1
        self.actual = 0
        self.cuadros = [0]
    @property
    def cuadro_actual(self):
        return self.grilla.obtener_cuadro(self.cuadros[self.actual])
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect, self.cuadro_actual)
    def dibujar_sombra(self, superficie):
        superficie.blit(self.sombra, (self.rect.right - self.sombra.get_width(), self.rect.y + 78))
    def actualizar(self, tiempo):
        if engine.pygame.time.get_ticks() - self.crono_i_m > self.intervalo_movimiento * 1000:
            self.crono_i_m = engine.pygame.time.get_ticks()
            self.mover()
        if engine.pygame.time.get_ticks() - self.crono_i_a > self.intervalo_animacion * 1000:
            self.crono_i_a = engine.pygame.time.get_ticks()
            self.actual += 1
            if self.actual > len(self.cuadros) - 1:
                self.actual = 0
        if self.rect.left >= 1200:
            engine.obtener_director().escena_actual.balas.remove(self)
        self.hacer_danio()
    def mover(self):
        pass
    def hacer_danio(self):
        atc = engine.pygame.sprite.spritecollideany(self, engine.obtener_director().escena_actual.atacantes)
        if atc:
            atc.salud -= self.danio
            engine.obtener_director().escena_actual.balas.remove(self)
    
class Estallido(object):
    imagen = None
    url_imagen = None
    def __new__(cls, *args, **kwargs):
        if not cls.imagen: 
            cls.imagen = engine.cargar_imagen(cls.url_imagen, True)
        return object.__new__(cls, *args, **kwargs)
    def __init__(self, centerx, centery):
        self.rect = self.imagen.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.intervalo_vida = 0.8
        self.crono_i_v = engine.pygame.time.get_ticks()
        self.termino = False
        self.danio = 0
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)
    def actualizar(self, tiempo):
        self.hacer_danio()
        if engine.pygame.time.get_ticks() - self.crono_i_v > self.intervalo_vida * 1000:
            engine.obtener_director().escena_actual.explosiones.remove(self)
    def hacer_danio(self):
        pass

class Pumba(Estallido):
    url_imagen = "pumba.png"
    def __init__(self, centerx, centery, padre):
        Estallido.__init__(self, centerx, centery)
        self.danio = 150
        self.padre = padre
    def hacer_danio(self):
        if not self.termino:
            i = self.padre.i + 1
            while i >= self.padre.i - 1:
                j = self.padre.j + 1
                while j >= self.padre.j - 1:
                    for z in engine.obtener_director().escena_actual.atacantes:
                        if z.i == i and z.j == j:
                            #deberia ir anmacion de zombies en cenizas
                            #engine.obtener_director().escena_actual.atacantes.remove(z)
                            z.salud -= self.danio
                    j -= 1
                i -= 1
            self.termino = True

class Placa(Estallido):
    url_imagen = "placa.png"
    def __init__(self, centerx, centery, padre):
        Estallido.__init__(self, centerx, centery)
        self.danio = 150
        self.padre = padre
        self.rect.bottom = self.rect.centery + 52
    def hacer_danio(self):
        if not self.termino:
            for a in engine.obtener_director().escena_actual.atacantes:
                if a.j == self.padre.j and a.i == self.padre.i:
                    a.salud -= self.danio

class Pua(Disparo):
    url_imagen = "pua.png"
    def __init__(self, x, y, objetivo, modo, padre):
        Disparo.__init__(self, x, y)
        self.x_inicial = self.rect.centerx
        self.y_inicial = self.rect.centery
        self.imagen_base = engine.cargar_imagen(self.url_imagen, True)
        self.danio = 20
        self.tiempo = 0
        self.velocidad_angular = 0
        self.velocidad = 3
        self.velocidad_x = self.velocidad
        self.velocidad_y = 0
        self.objetivo = objetivo
        self.modo = modo
        self.padre = padre
        self.finalx = 0
        self.finaly = 0
        self.var = False
    def mover(self):
        self.tiempo += 1
        self.finalx = self.objetivo.rect.centerx
        self.finaly = self.objetivo.rect.centery
        if self.padre.j > self.objetivo.j and self.padre.i != self.objetivo.i:
            self.finalx = self.padre.rect.centerx
        if self.objetivo.salud > 0:
            if (self.modo == 1 or self.modo == 2) and self.rect.centerx > self.padre.rect.centerx:
                radio = abs((((self.finalx - self.x_inicial) ** 2 + self.finaly ** 2 - self.y_inicial ** 2) / (2.0 * (self.finaly - self.y_inicial))) - self.y_inicial)
                self.velocidad_angular = self.velocidad / radio
                self.velocidad_x, self.velocidad_y = redondear(self.velocidad_angular * radio * math.cos(self.velocidad_angular * self.tiempo)), redondear(self.velocidad_angular * radio * math.sin(self.velocidad_angular * self.tiempo))
                if self.modo == 1:
                    self.rect.center = self.x_inicial + redondear(radio * math.sin(self.velocidad_angular * self.tiempo)), self.y_inicial - (radio - redondear(radio * math.cos(self.velocidad_angular * self.tiempo)))
                    self.imagen = engine.pygame.transform.rotate(self.imagen_base, self.velocidad_angular * 180 / math.pi * self.tiempo)
                elif self.modo == 2:
                    self.rect.center = self.x_inicial + redondear(radio * math.sin(self.velocidad_angular * self.tiempo)), self.y_inicial + (radio - redondear(radio * math.cos(self.velocidad_angular * self.tiempo)))
                    self.imagen = engine.pygame.transform.rotate(self.imagen_base, -self.velocidad_angular * 180 / math.pi * self.tiempo)
            elif self.modo == 0 or self.rect.centerx <= self.padre.rect.centerx:
                self.rect.centerx = self.rect.centerx + self.velocidad_x
        elif self.objetivo.salud <= 0:
            if self.modo == 1 and self.velocidad_y > 0: self.velocidad_y = -1 * self.velocidad_y
            self.rect.center = self.rect.centerx + self.velocidad_x, self.rect.centery + self.velocidad_y
    def hacer_danio(self):
        if self.rect.colliderect(self.objetivo.rect):
            self.objetivo.salud -= self.danio
            engine.obtener_director().escena_actual.balas.remove(self)

class Bala(Disparo):
    url_imagen = "bala.png"
    def __init__(self, x, y):
        Disparo.__init__(self, x, y)
        self.danio = 15
        self.velocidad = 4
    def mover(self):
        self.rect.centerx += self.velocidad
        
class Hielo(Disparo):
    url_imagen = "balahielo.png"
    cantidad = (3, 1)
    def __init__(self, x, y, padre):
        Disparo.__init__(self, x, y)
        self.danio = 20
        self.velocidad = 4
        self.padre = padre
        self.cuadros = [2, 0, 2, 1]
    def mover(self):
        self.rect.centerx += self.velocidad
    def hacer_danio(self):
        if len(engine.obtener_director().escena_actual.atacantes) > 0:
            obj = None
            for a in engine.obtener_director().escena_actual.atacantes:
                if self.padre.i == a.i:
                    obj = a
                    break
            for a in engine.obtener_director().escena_actual.atacantes:
                if self.padre.i == a.i and a.rect.centerx - self.rect.centerx < obj.rect.centerx - self.rect.centerx:
                    obj = a
            if obj and self.rect.colliderect(obj.rect):
                obj.salud -= self.danio
                obj.congelar()
                engine.obtener_director().escena_actual.balas.remove(self)
