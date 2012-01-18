import engine
import re

class Sol:
    def __init__(self, xinicial, y, yinicial = 150):
        self.imagen = engine.pygame.image.load("recursos/soles.png").convert_alpha()
        self.cuadros = [(0, 0, 115, 115), (115, 0, 115, 115), (230, 0, 115, 115), (115, 0, 115, 115)]
        self.actual = 0
        self.intervalo_caida = 0.001
        self.invervalo_animacion = 0.1
        self.intervalo_vida = 10
        self.crono_i_c = engine.pygame.time.get_ticks()
        self.crono_i_a = engine.pygame.time.get_ticks()
        self.crono_i_v = engine.pygame.time.get_ticks()
        self.rect = engine.pygame.Rect(0, 0, 115, 115)
        self.rect.centerx = xinicial
        self.rect.centery = yinicial
        self.finy = y
        self.x, self.y = self.rect.centerx, self.rect.centery
        self.tweener = engine.pytweener.Tweener()
        self.se_cogio = False
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect, self.cuadros[self.actual])
        self.rect.centerx, self.rect.centery = self.x, self.y
    def actualizar(self, tiempo):
        if engine.pygame.time.get_ticks() - self.crono_i_a > self.invervalo_animacion * 1000:
                self.crono_i_a = engine.pygame.time.get_ticks()
                self.actual += 1
                if self.actual > 3: self.actual = 0
        if self.y <= self.finy:
            if engine.pygame.time.get_ticks() - self.crono_i_c > self.intervalo_caida * 1000:
                self.crono_i_c = engine.pygame.time.get_ticks()
                self.y += 5
            self.crono_i_v = engine.pygame.time.get_ticks()
        else:
            if engine.pygame.time.get_ticks() - self.crono_i_v > self.intervalo_vida * 1000 and self.se_cogio == False:
                self.se_cogio = True
                engine.obtener_director().escena_actual.solsitos.remove(self)
        if self.tweener.hasTweens():
            self.tweener.update(tiempo / 1000.0)
    def recolectar(self):
        self.tweener.addTween(self, x = 65, y = 55, tweenTime = 0.8, tweenType = engine.pytweener.Easing.Linear.easeIn, onCompleteFunction = self.desaparecer)
    def desaparecer(self):
        engine.obtener_director().escena_actual.barra_control.soles += 25
        engine.obtener_director().escena_actual.solsitos.remove(self)
    def sincronizar_cronos_pausa(self, t):
        for i in self.__dict__:
            if re.match("\Acrono_i_.*", i):
                exec("self.{}=self.{}+t".format(i, i))
