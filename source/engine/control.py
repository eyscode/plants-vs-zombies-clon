'''
Created on 17/12/2011

@author: eysenck
'''
import engine
import time

class Director(object):
    __singleton = None
    def __new__(cls, *args, **kargs):
        if cls.__singleton is None:
            cls.__singleton = object.__new__(cls, *args, **kargs)
        return cls.__singleton
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.__escenas = []
        self.__corriendo = True
        self.clock = engine.pygame.time.Clock()
    def add_escena(self, escena):
        self.__escenas.append(escena)
        self.__corriendo = True
    def set_escena(self, escena):
        self.__corriendo = True
        del self.__escenas
        self.__escenas = [escena]
    def loop(self):
        while self.__corriendo:
            time = self.clock.tick(80)
            #print "fps del juego:", self.clock.get_fps()
            engine.cursor.actualizar(time)
            self.__escenas[-1].actualizar(time)
            self.__escenas[-1].dibujar(self.pantalla)
            #engine.cursor.dibujar(self.pantalla)
            for evento in engine.pygame.event.get():
                self.__escenas[-1].verificar_eventos(evento)
            engine.pygame.display.update()
    def mostrar_mensaje(self):
        pass
    def salir(self):
        self.__corriendo = False
    @property
    def escena_actual(self):
        return self.__escenas[-1]
    def remove_escena(self):
        self.__escenas.pop()
