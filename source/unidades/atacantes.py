import engine
from unidades.defensores import Nenufar

class Atacante:
    def __init__(self, i, w, h):
        self.w = w
        self.h = h
        self.i = i
        self.j = 10
        self.intervalo_movimiento = 0.8
        self.intervalo_animacion = 0.1
        self.crono_i_m = 0
        self.crono_i_a = 0
        self.salud = 100
        self.danio = 30
        self.detenido = False
    def dibujar(self, superficie):
        pass
    def actualizar(self, tiempo):
        pass
    
class Zombie(Atacante):
    def __init__(self, i, w, h):
        Atacante.__init__(self, i, w, h)
        self.rect = engine.pygame.Rect(0, 0, 15, 167)
        self.rect_real = engine.pygame.Rect(0, 0, 100, 167)
        self.rect_real.centerx = self.w * (self.j + 1)
        self.rect_real.bottom = 120 + self.h * (i + 1)
        self.imagen = engine.cargar_imagen("zombies.png", True)
        cuadros1 = [(a, 0, 100, 167) for a in range(0, 700, 100)]
        cuadros2 = [(a, 0, 100, 167) for a in range(0, 700, 100)]
        cuadros2.reverse()
        self.cuadros_caminando = cuadros1 + cuadros2
        self.cuadros_comiendo = [(a, 167, 100, 167) for a in range(0, 400, 100)]
        self.cuadros = self.cuadros_caminando
        self.actual = 0
        self.intervalo_golpe = 2
        self.crono_i_g = 0
        self.danio = 30
        self.salud = 130
        self.detenido = False
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect_real, self.cuadros[self.actual])
    def actualizar(self, tiempo):
        self.rect.center = self.rect_real.center
        if self.detenido:
            self.intervalo_animacion = 0.5
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
        else:
            self.intervalo_animacion = 0.1
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
                                break
        if engine.pygame.time.get_ticks() - self.crono_i_a > self.intervalo_animacion * 1000:
            self.crono_i_a = engine.pygame.time.get_ticks()
            self.actual += 1
            if self.actual > len(self.cuadros) - 1:
                self.actual = 0
        if self.salud <= 0:
            engine.obtener_director().escena_actual.atacantes.remove(self)
