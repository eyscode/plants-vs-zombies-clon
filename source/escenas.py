from pygame import locals
from unidades.atacantes import Zombie
from unidades.neutrales import Sol
import random
from complementos import BarraControl, Boton, CuadroELeccion, Carta, CuadroCreacion, Bienvenida, MenuPausa, \
    CuadroLampa
import engine
import sqlite3
from personal import Usuario
from unidades.defensores import LanzaGuisantes, Girasol, ColaDeGato, Nenufar, Nuez, PetaCereza

class Escena:
    def __init__(self):
        self.fondo = None
    def dibujar(self, superficie):
        pass
    def actualizar(self, tiempo):
        pass
    def verificar_eventos(self, evento):
        pass

class MenuInicio(Escena):
    def __init__(self):
        Escena.__init__(self)
        self.fondo = engine.cargar_imagen("inicial.jpg")
        self.boton_ad = Boton(508, 83, engine.cargar_imagen("boton7.png", True), comando = self.adventure)
        self.bienvenida = None
        self.cuadro_creacion = None
        self.cuadro_quien = None
        self.tweener = engine.pytweener.Tweener()
        self.cargar_ultimo_usuario()
        self.rect_clic = engine.pygame.Rect(900, 645, 64, 34)
    def cargar_ultimo_usuario(self):
        id_user = None
        conn = sqlite3.connect('recursos/data.db')
        cursor = conn.cursor()
        cursor.execute("select id_usuario from sesion where acceso = (select MAX(acceso) from sesion);")
        obtenido = cursor.fetchone()
        if obtenido: id_user = obtenido[0]
        if id_user:
            cursor.execute("select nombre from usuario where id=?;", (id_user,))
            nombre = cursor.fetchone()[0]
            plantas = []
            objetos = []
            cursor.execute("select * from carta where id in (select id_carta from usuario_carta where id_usuario = ?);", (id_user,))
            for row in cursor:
                clase = None
                clasebase = None
                exec("clase = {}".format(row[3]))
                exec("clasebase = {}".format(row[10]))
                plantas.append(Carta(engine.pygame.Rect(row[1], row[2], 62, 87), clase, row[4], row[5], row[6], row[7], row[8], row[9], clasebase))
            cursor.execute("select * from objeto where id in (select id_objeto from usuario_objeto where id_usuario = ?);", (id_user,))
            for row in cursor:
                objetos.append(row[1])
            engine.definir_usuario(Usuario(id_user, nombre, plantas, objetos))
            self.saludar()
        else:
            self.cuadro_creacion = CuadroCreacion()
        conn.close()
    def saludar(self):
        if not self.bienvenida:
            self.bienvenida = Bienvenida()
            self.tweener.addTween(self.bienvenida, y = 0, tweenTime = 0.2, tweenType = engine.pytweener.Easing.Linear.easeIn)
        else:
            self.bienvenida.nombre = engine.obtener_usuario().nombre
    def dibujar(self, superficie):
        superficie.blit(self.fondo, (0, 0))
        self.boton_ad.dibujar(superficie)
        if self.bienvenida: self.bienvenida.dibujar(superficie)
        if self.cuadro_quien: self.cuadro_quien.dibujar(superficie)
        if self.cuadro_creacion: self.cuadro_creacion.dibujar(superficie)
    def actualizar(self, tiempo):
        if self.tweener.hasTweens():
            self.tweener.update(tiempo / 1000.0)
        if self.cuadro_creacion: self.cuadro_creacion.actualizar(tiempo)
        if self.bienvenida: self.bienvenida.actualizar(tiempo)
        if self.cuadro_quien: self.cuadro_quien.actualizar(tiempo)
    def verificar_eventos(self, evento):
        if self.cuadro_creacion: 
            self.cuadro_creacion.verificar_eventos(evento)
        elif self.cuadro_quien: 
            self.cuadro_quien.verificar_eventos(evento)
        else:
            self.boton_ad.verificar_eventos(evento)
            self.bienvenida.verificar_eventos(evento)
        if evento.type == locals.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_clic.collidepoint(evento.pos[0], evento.pos[1]):
                engine.obtener_director().salir()
    def adventure(self):
        #belsprout = Carta((0, 0, 62, 87), LanzaGuisantes, 100, "tierra", 8)
        #gira = Carta((65, 0, 62, 87), Girasol, 50, "tierra", 5)
        #gato = Carta((195, 488, 62, 87), ColaDeGato, 225, "agua", 12)
        #nenufar = Carta((0, 195, 62, 87), Nenufar, 25, "agua", 6)
        e = Supervivencia()
        for c in engine.obtener_usuario().plantas:
            e.cuadro_eleccion.agregar_carta(c)
        engine.obtener_director().set_escena(e)
        engine.obtener_director().escena_actual.imagen_cartas = engine.cargar_imagen("cartas.jpg")
        engine.obtener_director().escena_actual.imagen_charge = engine.cargar_imagen("charge.png", True)
        engine.obtener_director().escena_actual.imagen_nosoles = engine.cargar_imagen("nosoles.png", True)
    def survival(self):
        pass
    def creditos(self):
        pass
    def salir(self):
        pass

class Supervivencia(Escena):
    def __init__(self, lineas = {0:"tierra", 1:"tierra", 2:"agua", 3:"agua", 4:"tierra", 5:"tierra"}):
        Escena.__init__(self)
        self.hora = "dia"
        self.lineas = lineas
        self.atacantes = []
        self.balas = []
        self.solsitos = []
        self.cartas = []
        self.explosiones = []
        self.tablero = [[None for col in range(9)] for row in range(6)]
        self.banderas = 0
        self.establecer_enemigos()
        self.barra_control = None
        self.cuadro_eleccion = CuadroELeccion()
        self.boton_menu = None
        self.seleccion = None
        self.carta_seleccionada = None
        self.intervalo_zombie = random.randint(18, 20)
        self.crono_i_z = engine.pygame.time.get_ticks()
        self.imagen_cartas = None
        self.imagen_charge = None
        self.imagen_nosoles = None
        self.tweener = engine.pytweener.Tweener()
        self.intervalo_comienzo = 0
        self.crono_i_c = engine.pygame.time.get_ticks()
        self.intervalo_produccion = 14
        self.crono_i_p = engine.pygame.time.get_ticks()
        self.jugando = False
        self.izquierda = 0
        self.rect_origen = engine.pygame.Rect(0, 0, 1000, 750)
        self.final_comienzo = False
        self.fondo = engine.cargar_imagen("piscina.jpg")
        self.menu_pausa = None
        self.ancho_cuadro = 100
        self.alto_cuadro = 104
        self.cuadro_lampa = None
    def establecer_enemigos(self):
        self.por_venir = {Zombie:6 * (self.banderas + 1)}
    def verificar_completado(self):
        if self.por_venir[Zombie] == 0 and len(self.atacantes) == 0:
            self.banderas += 1
            print "se acabo una oleada"
            self.establecer_enemigos()
            self.intervalo_zombie = random.randint(18, 20)
            self.crono_i_z = engine.pygame.time.get_ticks()
            #engine.obtener_director().salir()
    def modo_eleccion(self):
        self.barra_control = BarraControl()
        self.cuadro_eleccion.aparecer()
    def modo_juego(self):
        self.jugando = True
        self.boton_menu = Boton(862, 4, engine.cargar_imagen("boton1.png", True), comando = self.pausar, nombre = "MENU")
        self.barra_control.eligiendo = 2
        self.cuadro_lampa = CuadroLampa() if 'Lampa' in engine.obtener_usuario().objetos else None
        self.crono_i_p = engine.pygame.time.get_ticks()
        self.crono_i_z = engine.pygame.time.get_ticks()
    def pausar(self):
        self.menu_pausa = MenuPausa()
    def dibujar(self, superficie):
        superficie.blit(self.fondo, (0, 0), self.rect_origen)
        if self.barra_control: self.barra_control.dibujar(superficie)
        if self.cuadro_lampa: self.cuadro_lampa.dibujar(superficie)
        if self.cuadro_eleccion: self.cuadro_eleccion.dibujar(superficie)
        if self.jugando:
            self.boton_menu.dibujar(superficie)
            for b in self.balas:
                b.dibujar_sombra(superficie)
            for fila in self.tablero:
                for defensor in fila:
                    if defensor: defensor.dibujar(superficie)
            if self.seleccion: self.seleccion.dibujar_posible(superficie)
            for a in self.atacantes:
                a.dibujar(superficie)
            for e in self.explosiones:
                e.dibujar(superficie)
            for b in self.balas:
                b.dibujar(superficie)
            for s in self.solsitos:
                s.dibujar(superficie)
            if self.cuadro_lampa: self.cuadro_lampa.dibujar_lampa(superficie)
            if self.seleccion: self.seleccion.dibujar(superficie)
        else:
            for c in self.cartas:
                c.dibujar(superficie)
        if self.menu_pausa:
            self.menu_pausa.dibujar(superficie)
    def actualizar(self, tiempo):
        self.verificar_completado()
        if self.boton_menu: self.boton_menu.actualizar(tiempo)
        if not self.menu_pausa:
            self.rect_origen.left = self.izquierda
            if self.barra_control: self.barra_control.actualizar(tiempo)
            if self.cuadro_lampa: self.cuadro_lampa.actualizar(tiempo)
            if self.cuadro_eleccion: self.cuadro_eleccion.actualizar(tiempo)
            if self.tweener.hasTweens():
                self.tweener.update(tiempo / 1000.0)
            if self.jugando:
                for fila in self.tablero:
                    for defensor in fila:
                        if defensor: defensor.actualizar(tiempo)
                for e in self.explosiones:
                    e.actualizar(tiempo)
                for b in self.balas:
                    b.actualizar(tiempo)
                for a in self.atacantes:
                    a.actualizar(tiempo)
                for s in self.solsitos:
                    s.actualizar(tiempo)
                if self.seleccion: self.seleccion.actualizar(tiempo)
                if engine.pygame.time.get_ticks() - self.crono_i_p > self.intervalo_produccion * 1000:
                    self.crono_i_p = engine.pygame.time.get_ticks()
                    self.aparece_solsito()
                if engine.pygame.time.get_ticks() - self.crono_i_z > self.intervalo_zombie * 1000:
                    self.crono_i_z = engine.pygame.time.get_ticks()
                    self.intervalo_zombie = random.randint(5, 7)
                    self.poner_zombie()
                self.atacantes.sort(key = lambda atacante: atacante.i)
            else:
                for c in self.cartas:
                    c.actualizar(tiempo)
                if engine.pygame.time.get_ticks() - self.crono_i_c > self.intervalo_comienzo * 1000 and self.final_comienzo == False:
                    self.tweener.addTween(self, izquierda = 727, tweenTime = 2, tweenType = engine.pytweener.Easing.Linear.easeIn, onCompleteFunction = self.modo_eleccion)
                    self.final_comienzo = True
            
        else:
            self.menu_pausa.actualizar(tiempo)
    def verificar_eventos(self, evento):
        if self.cuadro_eleccion: self.cuadro_eleccion.verificar_eventos(evento)
        if not self.menu_pausa:
            if self.boton_menu: self.boton_menu.verificar_eventos(evento)
            if self.seleccion: self.seleccion.verificar_eventos(evento)
            if evento.type == locals.QUIT:
                engine.obtener_director().salir()
            elif evento.type == locals.MOUSEBUTTONDOWN and evento.button == 1 and self.jugando:
                if self.seleccion and not self.barra_control.imagen.get_rect().collidepoint(evento.pos[0], evento.pos[1]):
                    self.plantar(evento.pos)
                    self.seleccion = None
                else:
                    for sol in self.solsitos:
                        if sol.rect.collidepoint(evento.pos[0], evento.pos[1]):
                            sol.recolectar()
            elif evento.type == locals.MOUSEBUTTONDOWN and evento.button == 3 and self.jugando:
                if self.seleccion:
                    self.seleccion.slot.aclarar()
                    self.seleccion = None
            if self.barra_control: self.barra_control.verificar_eventos(evento)
            if self.cuadro_lampa: self.cuadro_lampa.verificar_eventos(evento)
        else:
            self.menu_pausa.verificar_eventos(evento)
    def plantar(self, (x , y)):
        i = (y - 120) / 104
        j = (x - 50) / 100
        if 0 <= i <= 5 and 0 <= j <= 8:
            if self.seleccion.plantable == 0:
                d = self.seleccion.carta.clase(i, j)
                self.tablero[i][j] = d
                self.seleccion.slot.cargar()
                self.barra_control.soles -= self.seleccion.carta.info['precio']
            elif self.seleccion.plantable == 1:
                d = self.seleccion.carta.clase(i, j)
                self.tablero[i][j].contenido = d
                self.seleccion.slot.cargar()
                self.barra_control.soles -= self.seleccion.carta.info['precio']
            else:
                self.seleccion.slot.aclarar()
        else:
            self.seleccion.slot.aclarar()
    def aparece_solsito(self):
        x, y = random.randint(100, 950), random.randint(210, 690)
        self.solsitos.append(Sol(x, y))
    def poner_zombie(self):
        index = random.randint(0, len(self.por_venir) - 1)
        clase = self.por_venir.keys()[index]
        i = random.randint(0, 5)
        if self.por_venir[clase] > 0:
            z = clase(i, 100, 104)
            z.salud = z.salud * (self.banderas + 1)
            self.atacantes.append(z)
            self.por_venir[clase] -= 1

class EnJuego(Escena):
    def __init__(self, filas_validas = (0, 1, 2, 3, 4), atacantes = {Zombie:10}):
        Escena.__init__(self)
        self.filas_validas = filas_validas
        self.defensas = []
        self.atacantes = []
        self.balas = []
        self.solsitos = []
        self.cartas = []
        self.tablero = [[None for col in range(9)] for row in range(5)]
        self.barra_control = None
        self.cuadro_eleccion = CuadroELeccion()
        self.boton_menu = Boton(862, 4, engine.cargar_imagen("boton1.png", True), comando = self.pausar, nombre = "MENU")
        self.seleccion = None
        self.por_venir = atacantes
        self.intervalo_zombie = random.randint(18, 20)
        self.crono_i_z = engine.pygame.time.get_ticks()
        self.imagen_cartas = None
        self.imagen_charge = None
        self.imagen_nosoles = None
        self.tweener = engine.pytweener.Tweener()
        self.intervalo_comienzo = 0
        self.crono_i_c = engine.pygame.time.get_ticks()
        self.intervalo_produccion = 13
        self.crono_i_p = engine.pygame.time.get_ticks()
        self.jugando = False
        self.izquierda = 0
        self.rect_origen = engine.pygame.Rect(0, 0, 1000, 750)
        self.final_comienzo = False
        self.fondo = engine.cargar_imagen("fondoreal.jpg")
        self.menu_pausa = None
    def modo_eleccion(self):
        self.barra_control = BarraControl()
        self.cuadro_eleccion.aparecer()
    def modo_juego(self):
        self.barra_control.eligiendo = 2
        self.jugando = True
        self.crono_i_p = engine.pygame.time.get_ticks()
        self.crono_i_z = engine.pygame.time.get_ticks()
    def pausar(self):
        self.menu_pausa = MenuPausa()
    def dibujar(self, superficie):
        superficie.blit(self.fondo, (0, 0), self.rect_origen)
        if self.barra_control: self.barra_control.dibujar(superficie)
        if self.cuadro_eleccion: self.cuadro_eleccion.dibujar(superficie)
        if self.jugando:
            self.boton_menu.dibujar(superficie)
            for b in self.balas:
                b.dibujar_sombra(superficie)
            for d in self.defensas:
                d.dibujar(superficie)
            for a in self.atacantes:
                a.dibujar(superficie)
            for b in self.balas:
                b.dibujar(superficie)
            for s in self.solsitos:
                s.dibujar(superficie)
            if self.seleccion: self.seleccion.dibujar(superficie)
        else:
            for c in self.cartas:
                c.dibujar(superficie)
        if self.menu_pausa: self.menu_pausa.dibujar(superficie)
    def actualizar(self, tiempo):
        if not self.menu_pausa:
            self.boton_menu.actualizar(tiempo)
            self.rect_origen.left = self.izquierda
            if self.barra_control: self.barra_control.actualizar(tiempo)
            if self.cuadro_eleccion: self.cuadro_eleccion.actualizar(tiempo)
            if self.tweener.hasTweens():
                self.tweener.update(tiempo / 1000.0)
            if self.jugando:
                for d in self.defensas:
                    d.actualizar(tiempo)
                for b in self.balas:
                    b.actualizar(tiempo)
                    atc = engine.pygame.sprite.spritecollideany(b, self.atacantes)
                    if atc:
                        atc.salud -= b.danio
                        self.balas.remove(b)
                for a in self.atacantes:
                    a.actualizar(tiempo)
                for s in self.solsitos:
                    s.actualizar(tiempo)
                if self.seleccion: self.seleccion.actualizar(tiempo)
                if engine.pygame.time.get_ticks() - self.crono_i_p > self.intervalo_produccion * 1000:
                    self.crono_i_p = engine.pygame.time.get_ticks()
                    self.aparece_solsito()
                if engine.pygame.time.get_ticks() - self.crono_i_z > self.intervalo_zombie * 1000:
                    self.crono_i_z = engine.pygame.time.get_ticks()
                    self.intervalo_zombie = random.randint(5, 7)
                    self.poner_zombie()
                self.atacantes.sort(key = lambda atacante: atacante.i)
            else:
                for c in self.cartas:
                    c.actualizar(tiempo)
                if engine.pygame.time.get_ticks() - self.crono_i_c > self.intervalo_comienzo * 1000 and self.final_comienzo == False:
                    self.tweener.addTween(self, izquierda = 727, tweenTime = 2, tweenType = engine.pytweener.Easing.Linear.easeIn, onCompleteFunction = self.modo_eleccion)
                    self.final_comienzo = True
        else:
            self.menu_pausa.actualizar(tiempo)
    def verificar_eventos(self, evento):
        if not self.menu_pausa:
            if self.cuadro_eleccion: self.cuadro_eleccion.verificar_eventos(evento)
            if self.jugando: self.boton_menu.verificar_eventos(evento)
            if evento.type == locals.QUIT:
                engine.obtener_director().salir()
            elif evento.type == locals.MOUSEBUTTONDOWN and evento.button == 1:
                if self.seleccion:
                    if self.jugando:
                        self.plantar(self.seleccion.clase, engine.pygame.mouse.get_pos())
                        self.seleccion = None
                else:
                    if self.barra_control: self.barra_control.verificar_eventos(evento)
                if self.jugando:
                    for sol in self.solsitos:
                        if sol.rect.collidepoint(engine.pygame.mouse.get_pos()[0], engine.pygame.mouse.get_pos()[1]):
                            sol.recolectar()
        else:
            self.menu_pausa.verificar_eventos(evento)
    def plantar(self, defensor, (x , y)):
        i = (y - 150) / 120
        j = (x - 50) / 100
        if i in self.filas_validas and 0 <= j <= 8:
            if self.tablero[i][j] == 0:
                self.tablero[i][j] = 1
                self.defensas.append(defensor(i, j, 100, 120))
                self.barra_control.soles -= self.seleccion.carta.precio
                self.seleccion.slot.cargar()
            else:
                self.seleccion.slot.aclarar()
        else:
            self.seleccion.slot.aclarar()
    def aparece_solsito(self):
        x, y = random.randint(100, 950), random.randint(210, 690)
        self.solsitos.append(Sol(x, y))
    def poner_zombie(self):
        index = random.randint(0, len(self.por_venir) - 1)
        clase = self.por_venir.keys()[index]
        i = random.randint(0, 4)
        if self.por_venir[clase] > 0:
            self.atacantes.append(clase(i))
            self.por_venir[clase] -= 1
