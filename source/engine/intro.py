from engine import pytweener
import pygame
from pygame.locals import *
from escenas import Escena


class IntroEys(Escena):
    def __init__(self, director):
        Escena.__init__(self)
        self.director = director
        self.__background = pygame.Surface((1000, 750))
        self.__layer1 = self.Sprite(pygame.image.load("recursos/imgs/capa.png").convert(), 0, 0)
        self.__layer2 = pygame.image.load("recursos/imgs/eys.png").convert_alpha()
        self.__layer3 = self.Sprite(pygame.image.load("recursos/imgs/bola2.png").convert_alpha(), 0, 0)
        self.__t = pytweener.Tweener()
        self.__t.addTween(self.__layer3, width = 300, height = 105, tweenTime = 1, tweenType = pytweener.Easing.Linear.easeOut)
        self.__t.addTween(self.__layer1, alpha = 150, tweenTime = 1.4, tweenType = pytweener.Easing.Elastic.easeOut, onCompleteFunction = self.__action2)
        #pygame.mixer.Sound("snds/esto.wav").play()
    def actualizar(self, time):
        self.__t.update(time / 1000.0)
        self.__layer3.update()
        self.__layer1.appear()
    def dibujar(self, screen):
        screen.blit(self.__background, (0, 0))
        self.__layer3.draw(screen)
        screen.blit(self.__layer2, (320, 310))
        self.__layer1.draw(screen)
    def verificar_eventos(self, event):
        if event.type == KEYDOWN and event.key == 27:
            self.director.salir()
    def __action1(self):
        self.__t.addTween(self.__layer1, alpha = 255, tweenTime = 1.5, tweenType = pytweener.Easing.Cubic.easeOut, onCompleteFunction = self.director.salir)
    def __action2(self):
        self.__t.addTween(self.__layer3, width = 800, height = 280, tweenTime = 0.5, tweenType = pytweener.Easing.Back.easeOut)
        self.__t.addTween(self.__layer1, alpha = 0, tweenTime = 2, tweenType = pytweener.Easing.Cubic.easeOut, onCompleteFunction = self.__action1)
    class Sprite:
        def __init__(self, image, x, y):
            self.x = x
            self.y = y
            self.width = image.get_width()
            self.height = image.get_height()
            self.image = image
            self.original_image = image
            self.alpha = 255
        def update(self):
            size = (int(self.width), int(self.height))
            self.image = pygame.transform.smoothscale(self.original_image, size)
        def appear(self):
            self.image.set_alpha(self.alpha)
        def draw(self, screen):
            screen.blit(self.image, (500 - self.width / 2, 375 - self.height / 2)) 
