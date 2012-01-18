#!/usr/bin/python
'''
Created on 17/12/2011

@author: eysenck
'''
import engine
import os
from engine.control import Director
from complementos import Carta
from unidades.defensores import Girasol, LanzaGuisantes
from engine.intro import IntroEys
from escenas import MenuInicio

if __name__ == '__main__':
    url = os.path.join(os.path.dirname(__file__), 'recursos').replace('\\', '/')
    
    engine.inicializar()
    engine.definir_media(url)
    engine.definir_icono("icono.png")
    engine.definir_titulo("Plantas contra Zombies Clon")
    pantalla = engine.definir_dimension(1000, 750)
        
    d = Director(pantalla)
    engine.definir_director(d)
    
    intro = IntroEys(d)
    d.set_escena(intro)
    d.loop()
    
    inicio = MenuInicio()
    d.set_escena(inicio)
    d.loop()
