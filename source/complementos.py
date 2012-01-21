from pygame import locals
from engine import pytweener
import sqlite3
from datetime import datetime
from personal import Usuario
from unidades.defensores import *

class MenuPausa(object):
    def __init__(self):
        self.imagen = engine.cargar_imagen("pausa.png", True)
        self.boton_sal = Boton(260, 586, engine.cargar_imagen("boton3.png", True), comando = self.salir)
        self.tiempo_pausa = engine.pygame.time.get_ticks()
    def dibujar(self, superficie):
        superficie.blit(self.imagen, (0, 0))
        self.boton_sal.dibujar(superficie)
    def actualizar(self, tiempo):
        self.boton_sal.actualizar(tiempo)
    def verificar_eventos(self, evento):
        self.boton_sal.verificar_eventos(evento)
    def salir(self):
        t = engine.pygame.time.get_ticks() - self.tiempo_pausa
        engine.obtener_director().escena_actual.menu_pausa = None
        for fila in engine.obtener_director().escena_actual.tablero:
            for p in fila:
                if p: p.sincronizar_cronos_pausa(t)
        for s in engine.obtener_director().escena_actual.solsitos:
            s.sincronizar_cronos_pausa(t)

class Confirmar(object):
    def __init__(self, nombre):
        self.imagen = engine.cargar_imagen("areyousure.png", True)
        self.rect = engine.pygame.Rect(242, 183, 510, 380)
        self.boton_yes = Boton(self.rect.x + 37, self.rect.y + 284, engine.cargar_imagen("boton10.png", True), comando = self.yes, nombre = "YES")
        self.boton_no = Boton(self.rect.x + 258, self.rect.y + 284, engine.cargar_imagen("boton10.png", True), comando = self.no, nombre = "NO")
        self.nombre = self.imagen_nombre = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 34), "'" + nombre + "'", 1, (224, 187, 98))
        if self.nombre.get_rect().width + 339 > 416:
            self.msj_1 = self.imagen_nombre = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 34), "This will permanently remove ", 1, (224, 187, 98))
            self.msj_2 = self.imagen_nombre = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 34), "'" + nombre + "' from the player roster!", 1, (224, 187, 98))
        else:
            self.msj_1 = self.imagen_nombre = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 34), "This will permanently remove '" + nombre + "'", 1, (224, 187, 98))
            self.msj_2 = self.imagen_nombre = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 34), "from the player roster!", 1, (224, 187, 98))
        self.rect_1 = self.msj_1.get_rect()
        self.rect_2 = self.msj_2.get_rect()
        self.rect_1.center = 494, 365
        self.rect_2.center = 494, 394
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)
        self.boton_yes.dibujar(superficie)
        self.boton_no.dibujar(superficie)
        superficie.blit(self.msj_1, self.rect_1)
        superficie.blit(self.msj_2, self.rect_2)
    def verificar_eventos(self, evento):
        self.boton_yes.verificar_eventos(evento)
        self.boton_no.verificar_eventos(evento)
    def actualizar(self, tiempo):
        self.boton_yes.actualizar(tiempo)
        self.boton_no.actualizar(tiempo)
        self.boton_yes.rect.x = self.rect.x + 37
        self.boton_yes.rect.y = self.rect.y + 284
        self.boton_no.rect.x = self.rect.x + 258
        self.boton_no.rect.y = self.rect.y + 284
    def yes(self):
        engine.obtener_director().escena_actual.cuadro_quien.delete()
        engine.obtener_director().escena_actual.cuadro_quien.confirmar = None
    def no(self):
        engine.obtener_director().escena_actual.cuadro_quien.confirmar = None

class QuienEres(object):
    def __init__(self):
        self.imagen = engine.cargar_imagen("quieneres.png", True)
        self.rect = engine.pygame.Rect(126, 58, 745, 628)
        self.boton_rename = Boton(self.rect.x + 40, self.rect.y + 481, engine.cargar_imagen("boton9.png", True), comando = self.rename, nombre = "rename")
        self.boton_delete = Boton(self.rect.x + 378, self.rect.y + 481, engine.cargar_imagen("boton9.png", True), comando = self.areyousure, nombre = "delete")
        self.boton_ok = Boton(self.rect.x + 40, self.rect.y + 538, engine.cargar_imagen("boton9.png", True), comando = self.ok, nombre = "ok")
        self.boton_cancel = Boton(self.rect.x + 378, self.rect.y + 538, engine.cargar_imagen("boton9.png", True), comando = self.cancel, nombre = "cancel")
        self.imagen_seleccion = engine.pygame.Surface((568, 31))
        self.imagen_seleccion.fill((0, 174, 0))
        self.elementos = [Elemento(engine.pygame.Rect(self.rect.x + 84, self.rect.y + 175 + a, 568, 31), self.imagen_seleccion) for a in range(0, 248 , 31)]
        self.rect_clic = None
        self.imagen_crear = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 40), "(Create a New User)", 1, (246, 244, 177))
        self.rect_crear = self.imagen_crear.get_rect()
        self.confirmar = None
        self.renombrar = None
        self.cargar_usuarios()
        if self.elementos[0].usuario: self.elementos[0].seleccionado = True
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)
        self.boton_rename.dibujar(superficie)
        self.boton_delete.dibujar(superficie)
        self.boton_ok.dibujar(superficie)
        self.boton_cancel.dibujar(superficie)
        for e in self.elementos:
            e.dibujar(superficie)
        if self.rect_clic: superficie.blit(self.imagen_crear, self.rect_crear)
        if self.confirmar: self.confirmar.dibujar(superficie)
        if self.renombrar: self.renombrar.dibujar(superficie)
    def actualizar(self, tiempo):
        if self.confirmar: self.confirmar.actualizar(tiempo)
        elif self.renombrar: self.renombrar.actualizar(tiempo)
        else:
            for e in self.elementos:
                e.actualizar(tiempo)
            self.boton_ok.actualizar(tiempo)
            self.boton_cancel.actualizar(tiempo)
            self.boton_delete.actualizar(tiempo)
            self.boton_rename.actualizar(tiempo)
    def verificar_eventos(self, evento):
        if not self.confirmar and not self.renombrar:
            self.boton_rename.verificar_eventos(evento)
            self.boton_delete.verificar_eventos(evento)
            self.boton_ok.verificar_eventos(evento)
            self.boton_cancel.verificar_eventos(evento)
            for e in self.elementos:
                e.verificar_eventos(evento)
            if evento.type == locals.MOUSEBUTTONDOWN and evento.button == 1:
                if self.rect_clic and self.rect_clic.collidepoint(evento.pos[0], evento.pos[1]):
                    engine.obtener_director().escena_actual.cuadro_creacion = CuadroCreacion()
        elif self.confirmar: self.confirmar.verificar_eventos(evento)
        elif self.renombrar: self.renombrar.verificar_eventos(evento)
    def rename(self):
        s = None
        for e in self.elementos:
            if e.seleccionado == True: s = e.usuario
        self.renombrar = Renombre(s)
    def ok(self):
        s = None
        for e in self.elementos:
            if e.seleccionado == True: s = e.usuario
        if s != engine.obtener_usuario().nombre:
            conn = sqlite3.connect("recursos/data.db")
            cursor = conn.cursor()
            cursor.execute("select id from usuario where nombre = ?", (s,))
            id_user = cursor.fetchone()[0]
            cursor.execute("insert into sesion values (null,?,?)", (id_user, str(datetime.now())))
            conn.commit()
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
            engine.definir_usuario(Usuario(id_user, s, plantas, objetos))
            conn.close()
        engine.obtener_director().escena_actual.cuadro_quien = None
    def areyousure(self):
        s = None
        for e in self.elementos:
            if e.seleccionado == True: s = e.usuario
        self.confirmar = Confirmar(s)
    def delete(self):
        s = None
        i = 0
        for e in self.elementos:
            if e.seleccionado == True:
                s = e.usuario
                e.seleccionado = False
                break
            i += 1
        if i == 0:
            if self.elementos[1].usuario == None:
                engine.definir_usuario(None)
                engine.obtener_director().escena_actual.cuadro_creacion = CuadroCreacion()
            else:
                self.elementos[0].seleccionado = True
                conn = sqlite3.connect("recursos/data.db")
                cursor = conn.cursor()
                cursor.execute("select id from usuario where nombre = ?;", (self.elementos[1].usuario,))
                id_user = cursor.fetchone()[0]
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
                engine.definir_usuario(Usuario(id_user, self.elementos[1].usuario, plantas, objetos))
                conn.close()
        else:
            self.elementos[i - 1].seleccionado = True
        conn = sqlite3.connect("recursos/data.db")
        cursor = conn.cursor()
        cursor.execute("select id from usuario where nombre = ?", (s,))
        id_user = cursor.fetchone()[0]
        cursor.execute("delete from usuario where id = ?", (id_user,))
        cursor.execute("delete from sesion where id_usuario = ?", (id_user,))
        cursor.execute("delete from usuario_carta where id_usuario = ?", (id_user,))
        conn.commit()
        for e in self.elementos:
            e.usuario = None
        self.cargar_usuarios()
    def cancel(self):
        engine.obtener_director().escena_actual.cuadro_quien = None
    def cargar_usuarios(self):
        if engine.obtener_usuario():
            conn = sqlite3.connect("recursos/data.db")
            cursor = conn.cursor()
            cursor.execute("select nombre from usuario where nombre != ? order by nombre;", (engine.obtener_usuario().nombre,))
            self.elementos[0].usuario = engine.obtener_usuario().nombre
            i = 1
            for row in cursor:
                self.elementos[i].usuario = row[0]
                i += 1
            if i < 8:
                self.rect_clic = self.elementos[i].rect
                self.rect_crear.center = self.rect_clic.center
            else:
                self.rect_clic = None
        else:
            self.rect_clic = self.elementos[0].rect
            self.rect_crear.center = self.rect_clic.center
            self.elementos[0].seleccionado = True
        
class Elemento(object):
    def __init__(self, rect, seleccion = None):
        self.rect = rect
        self.seleccion = seleccion
        self.seleccionado = False
        self.imagen_nombre = None
        self.rect_nombre = None
        self.__nombre = None
    def dibujar(self, superficie):
        if self.seleccionado: superficie.blit(self.seleccion, self.rect)
        if self.imagen_nombre: superficie.blit(self.imagen_nombre, self.rect_nombre)
    def actualizar(self, tiempo):
        if self.imagen_nombre:
            self.rect_nombre.center = self.rect.center
    def verificar_eventos(self, evento):
        if evento.type == locals.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos[0], evento.pos[1]):
                for e in engine.obtener_director().escena_actual.cuadro_quien.elementos:
                    if e is not self and e.seleccionado:
                        if self.usuario: e.seleccionado = False
                if self.usuario:
                    self.seleccionado = True
    @property
    def usuario(self):
        return self.__nombre
    @usuario.setter
    def usuario(self, nombre):
        if nombre:
            self.__nombre = nombre
            self.imagen_nombre = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 40), self.__nombre, 1, (246, 244, 177))
            self.rect_nombre = self.imagen_nombre.get_rect()
            self.rect_nombre.center = self.rect.center
        else:
            self.__nombre = None
            self.imagen_nombre = None
            self.rect_nombre = None

class Bienvenida(object):
    def __init__(self):
        self.imagen = engine.cargar_imagen("bienvenida.png", True)
        self.x = 30
        self.y = -243
        self.rect_clic = engine.pygame.Rect(58, self.y + 186, 334, 38)
        self.__nombre = engine.obtener_usuario().nombre
        self.imagen_nombre = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 40), self.nombre, 1, (0, 176, 0))
        self.rect_nombre = self.imagen_nombre.get_rect()
        self.rect_nombre.center = 215, self.y + 120
    def dibujar(self, superficie):
        superficie.blit(self.imagen, (self.x, self.y))
        superficie.blit(self.imagen_nombre, self.rect_nombre)
    def actualizar(self, tiempo):
        self.rect_nombre.centery = self.y + 120
        self.rect_clic.centery = self.y + 186
        self.nombre = engine.obtener_usuario().nombre if engine.usuario else ""
    def verificar_eventos(self, evento):
        if evento.type == locals.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_clic.collidepoint(evento.pos[0], evento.pos[1]):
                engine.obtener_director().escena_actual.cuadro_quien = QuienEres()
    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, nombre):
        if nombre != self.__nombre:
            self.__nombre = nombre
            self.imagen_nombre = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 50), self.nombre, 1, (0, 176, 0))
            self.rect_nombre = self.imagen_nombre.get_rect()
            self.rect_nombre.center = 215, self.y + 120
        
class CuadroObligar(object):
    def __init__(self):
        self.imagen = engine.cargar_imagen("obligacion.png", True)
        self.rect = engine.pygame.Rect(184, 182, 636, 382)
        self.boton_ok = Boton(self.rect.x + 63, self.rect.y + 283, engine.cargar_imagen("boton11.png", True), comando = self.ok, nombre = "ok")
    def ok(self):
        engine.obtener_director().escena_actual.cuadro_creacion.cuadro_obligacion = None
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)
        self.boton_ok.dibujar(superficie)
    def verificar_eventos(self, evento):
        self.boton_ok.verificar_eventos(evento)
    def actualizar(self, tiempo):
        self.boton_ok.actualizar(tiempo)

class Renombre(object):
    def __init__(self, old):
        self.imagen = engine.cargar_imagen("rename.png", True)
        self.rect = engine.pygame.Rect(184, 184, 624, 380)
        self.boton_ok = Boton(223, 467, engine.cargar_imagen("boton8.png", True), comando = self.cambiar_usuario, nombre = "ok")
        self.boton_cancel = Boton(500, 467, engine.cargar_imagen("boton8.png", True), comando = self.cancelar, nombre = "cancel")
        self.entrada = Input(248, 376)
        self.old = old
        self.entrada.indice = len(self.old)
        self.entrada.text = self.old
        self.entrada.seleccionar()
    def cambiar_usuario(self):
        i = 0
        while i < len(self.entrada.text):
            if self.entrada.text[i] != " ":
                break
            i += 1
        self.entrada.text = self.entrada.text[i:len(self.entrada.text)]
        i = len(self.entrada.text) - 1
        while i > 0:
            if self.entrada.text[i] != " ":
                break
            i -= 1
        self.entrada.text = self.entrada.text[0:i + 1]
        if len(self.entrada.text.replace(" ", "")) != 0:
            conn = sqlite3.connect('recursos/data.db')
            cursor = conn.cursor()
            cursor.execute("update usuario set nombre = ? where nombre = ?", (self.entrada.text, self.old))
            conn.commit()
            conn.close()
            if self.old == engine.obtener_usuario().nombre: engine.obtener_usuario().nombre = self.entrada.text
            engine.obtener_director().escena_actual.cuadro_quien.cargar_usuarios()
            engine.obtener_director().escena_actual.cuadro_quien.renombrar = None
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)
        self.boton_ok.dibujar(superficie)
        self.boton_cancel.dibujar(superficie)
        self.entrada.dibujar(superficie)
    def actualizar(self, tiempo):
        self.entrada.actualizar(tiempo)
        self.boton_ok.actualizar(tiempo)
        self.boton_cancel.actualizar(tiempo)
    def verificar_eventos(self, evento):
        if evento.type == locals.KEYDOWN:
            self.seleccion = None
            if evento.key == 13:
                self.cambiar_usuario()
            elif evento.key == 275:
                self.entrada.text = self.old
        self.boton_ok.verificar_eventos(evento)
        self.boton_cancel.verificar_eventos(evento)
        self.entrada.verificar_eventos(evento)
    def cancelar(self):
        engine.obtener_director().escena_actual.cuadro_quien.renombrar = None
    
class CuadroCreacion(object):
    def __init__(self):
        self.imagen = engine.cargar_imagen("crearuser2.png", True)
        self.rect = engine.pygame.Rect(184, 184, 624, 380)
        self.boton_ok = Boton(223, 467, engine.cargar_imagen("boton8.png", True), comando = self.agregar_usuario, nombre = "ok")
        self.boton_cancel = Boton(500, 467, engine.cargar_imagen("boton8.png", True), comando = self.cancelar, nombre = "cancel")
        self.entrada = Input(248, 376)
        self.cuadro_obligacion = None
    def agregar_usuario(self):
        i = 0
        while i < len(self.entrada.text):
            if self.entrada.text[i] != " ":
                break
            i += 1
        self.entrada.text = self.entrada.text[i:len(self.entrada.text)]
        i = len(self.entrada.text) - 1
        while i > 0:
            if self.entrada.text[i] != " ":
                break
            i -= 1
        self.entrada.text = self.entrada.text[0:i + 1]
        if len(self.entrada.text.replace(" ", "")) != 0:
            conn = sqlite3.connect('recursos/data.db')
            cursor = conn.cursor()
            n = (self.entrada.text,)
            cursor.execute("select * from usuario where nombre = ?", (self.entrada.text,))
            if cursor.fetchall() != []:
                print "Ya existe un usuario con ese nombre,elija otro"
            else:
                cursor.execute("insert into usuario values (null,?,0)", n)
                cursor.execute("insert into sesion values (null,last_insert_rowid(),?)", (str(datetime.now()),))
                conn.commit()
                cursor.execute("select id from usuario where nombre = ?", (self.entrada.text,))
                engine.definir_usuario(Usuario(cursor.fetchone()[0], self.entrada.text, [], []))
                conn.close()
                engine.obtener_director().escena_actual.cuadro_creacion = None
                engine.obtener_director().escena_actual.cuadro_quien = None
                engine.obtener_director().escena_actual.saludar()
        else: self.cuadro_obligacion = CuadroObligar()
    def cancelar(self):
        if engine.usuario: 
            engine.obtener_director().escena_actual.cuadro_creacion = None
        else:
            self.cuadro_obligacion = CuadroObligar()
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)
        self.boton_ok.dibujar(superficie)
        self.boton_cancel.dibujar(superficie)
        self.entrada.dibujar(superficie)
        if self.cuadro_obligacion: self.cuadro_obligacion.dibujar(superficie)
    def actualizar(self, tiempo):
        self.entrada.actualizar(tiempo)
        self.boton_ok.actualizar(tiempo)
        self.boton_cancel.actualizar(tiempo)
        if self.cuadro_obligacion: self.cuadro_obligacion.actualizar(tiempo)
    def verificar_eventos(self, evento):
        if self.cuadro_obligacion: self.cuadro_obligacion.verificar_eventos(evento)
        else:
            if evento.type == locals.KEYDOWN and evento.key == 13:
                self.agregar_usuario()
            self.boton_ok.verificar_eventos(evento)
            self.boton_cancel.verificar_eventos(evento)
            self.entrada.verificar_eventos(evento)

class SlotCuadro(object):
    def __init__(self, rect):
        self.carta = None
        self.rect = rect
        self.usado = False
    def dibujar(self, superficie):
        if self.carta:
            superficie.blit(engine.obtener_director().escena_actual.imagen_cartas, self.rect, self.carta.rect_origen_carta)
            if self.usado:
                superficie.blit(engine.obtener_director().escena_actual.imagen_charge, self.rect)

class CuadroELeccion(object):
    def __init__(self):
        self.imagen = engine.cargar_imagen("choose.png", True)
        self.imagen_copia = engine.cargar_imagen("choose.png", True)
        f1 = [SlotCuadro(engine.pygame.Rect(a + 28, 51, 62, 87)) for a in range(0, 528, 66)]
        f2 = [SlotCuadro(engine.pygame.Rect(a + 28, 142, 62, 87)) for a in range(0, 528, 66)]
        f3 = [SlotCuadro(engine.pygame.Rect(a + 28, 233, 62, 87)) for a in range(0, 528, 66)]
        f4 = [SlotCuadro(engine.pygame.Rect(a + 28, 324, 62, 87)) for a in range(0, 528, 66)]
        f5 = [SlotCuadro(engine.pygame.Rect(a + 28, 415, 62, 87)) for a in range(0, 528, 66)]
        self.slots = f1 + f2 + f3 + f4 + f5
        self.rect = engine.pygame.Rect(0, 109, 581, 662)
        self.tweener = engine.pytweener.Tweener()
        self.altura = 750
        self.listo = Boton(194, 1325, engine.cargar_imagen("boton0.png", True), comando = self.bajar, nombre = "let's rock")
    def aparecer(self):
        self.tweener.addTween(self, altura = 109, tweenTime = 0.5, tweenType = engine.pytweener.Easing.Linear.easeIn)
    def agregar_carta(self, carta):
        for slot in self.slots:
            if slot.carta == None:
                slot.carta = carta
                slot.carta.x, slot.carta.y = slot.rect.x, slot.rect.y + 109
                slot.carta.slot_inicial = slot
                break
    def dibujar(self, superficie):
        self.imagen.blit(self.imagen_copia, (0, 0))
        for slot in self.slots:
            slot.dibujar(self.imagen)
        superficie.blit(self.imagen, (0, self.altura))
        self.listo.dibujar(superficie)
    def actualizar(self, tiempo):
        if not self.listo.presionado: self.listo.rect.y = self.altura + 575
        self.listo.actualizar(tiempo)
        if self.tweener.hasTweens():
            self.tweener.update(tiempo / 1000.0)
    def verificar_eventos(self, evento):
        self.listo.verificar_eventos(evento)
        if evento.type == locals.MOUSEBUTTONDOWN and evento.button == 1:
            for slot in self.slots:
                if slot.rect.collidepoint(evento.pos[0], evento.pos[1] - 109) and not slot.usado:
                    if slot.carta:
                        for s in engine.obtener_director().escena_actual.barra_control.slots:
                            if s.carta == None:
                                slot.usado = True
                                engine.obtener_director().escena_actual.cartas.append(slot.carta)
                                self.tweener.addTween(slot.carta, x = s.rect.x, y = s.rect.y, tweenTime = 0.2, tweenType = pytweener.Easing.Linear.easeIn, onCompleteFunction = slot.carta.empotrar)
                                break
    def bajar(self):
        engine.obtener_director().escena_actual.barra_control.eligiendo = 1
        self.tweener.addTween(self, altura = 750, tweenTime = 0.3, tweenType = engine.pytweener.Easing.Linear.easeIn, onCompleteFunction = self.acabar)
    def acabar(self):
        engine.obtener_director().escena_actual.cuadro_eleccion = None
        engine.obtener_director().escena_actual.tweener.addTween(engine.obtener_director().escena_actual, izquierda = 265, tweenTime = 1.5, tweenType = engine.pytweener.Easing.Linear.easeIn, onCompleteFunction = engine.obtener_director().escena_actual.modo_juego)

class CuadroLampa(object):
    def __init__(self):
        self.imagen = engine.cargar_imagen("slot_lampa.png", True)
        self.imagen_lampa = engine.cargar_imagen("lampa.png", True)
        self.rect_lampa = self.imagen_lampa.get_rect()
        self.rect = self.imagen.get_rect()
        self.rect.left = engine.obtener_director().escena_actual.barra_control.imagen.get_rect().width
        self.rect_lampa.center = self.rect.center
        self.usando = False
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)
    def dibujar_lampa(self, superficie):
        superficie.blit(self.imagen_lampa, self.rect_lampa)
    def actualizar(self, tiempo):
        if self.usando:
            self.rect_lampa.bottomleft = engine.pygame.mouse.get_pos()
        else:
            self.rect_lampa.center = self.rect.center
    def verificar_eventos(self, evento):
        if evento.type == locals.MOUSEBUTTONDOWN and evento.button == 1:
            if engine.obtener_director().escena_actual.barra_control.eligiendo == 2:
                if self.rect.collidepoint(evento.pos[0], evento.pos[1]) and not self.usando:
                    self.usando = True
                elif self.usando: 
                    i = (evento.pos[1] - 120) / 104
                    j = (evento.pos[0] - 50) / 100
                    if 0 <= i <= 5 and 0 <= j <= 8 and engine.obtener_director().escena_actual.tablero[i][j] != None:
                        if engine.obtener_director().escena_actual.tablero[i][j].__class__ == Nenufar and engine.obtener_director().escena_actual.tablero[i][j].contenido:
                            engine.obtener_director().escena_actual.tablero[i][j].contenido = None
                        else:
                            engine.obtener_director().escena_actual.tablero[i][j] = None
                    self.usando = False
        elif evento.type == locals.MOUSEBUTTONDOWN and evento.button == 3:
            if self.usando: self.usando = False

class BarraControl(object):
    def __init__(self):
        self.imagen = engine.cargar_imagen("barra.png", True)
        self.slots = [SlotBarra(engine.pygame.Rect(107 + a, 11, 62, 88)) for a in range(0, 438, 73)]
        self.soles = 5000
        self.nro_soles = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 30), str(self.soles), 1, (0, 0, 0))
        self.rect_soles = self.nro_soles.get_rect()
        self.rect_soles.center = 49, 91
        self.eligiendo = 0
        self.tweener = engine.pytweener.Tweener()
    def dibujar(self, superficie):
        superficie.blit(self.imagen, (0, 0))
        for slot in self.slots:
            slot.dibujar(superficie)
        superficie.blit(self.nro_soles, self.rect_soles)
    def actualizar(self, tiempo):
        for slot in self.slots:
            slot.actualizar(tiempo)
        self.nro_soles = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 30), str(self.soles), 1, (0, 0, 0))
        self.rect_soles = self.nro_soles.get_rect()
        self.rect_soles.center = 49, 91
        if self.tweener.hasTweens():
            self.tweener.update(tiempo / 1000.0)
    def verificar_eventos(self, evento):
        if evento.type == locals.MOUSEBUTTONDOWN and evento.button == 1:
            if self.eligiendo == 2:
                hubo_clic = False
                for slot in self.slots:
                    if slot.rect.collidepoint(evento.pos[0], evento.pos[1]):
                        hubo_clic = True
                        if slot.carta and engine.obtener_director().escena_actual.seleccion == None and slot.cargando == False:
                            if engine.obtener_director().escena_actual.barra_control.soles >= slot.carta.info['precio']:
                                engine.obtener_director().escena_actual.seleccion = PlantaSeleccionada(slot)
                                slot.oscurecer()
                        else:
                            if engine.obtener_director().escena_actual.seleccion: engine.obtener_director().escena_actual.seleccion.slot.aclarar()
                            engine.obtener_director().escena_actual.seleccion = None
                        break
                if not hubo_clic and self.imagen.get_rect().collidepoint(evento.pos[0], evento.pos[1]) and engine.obtener_director().escena_actual.seleccion:
                    engine.obtener_director().escena_actual.seleccion.slot.aclarar()
                    engine.obtener_director().escena_actual.seleccion = None
            elif self.eligiendo == 0:
                for slot in self.slots:
                    if slot.rect.collidepoint(evento.pos[0], evento.pos[1]):
                        if slot.carta:
                            engine.obtener_director().escena_actual.cartas.append(slot.carta)
                            self.tweener.addTween(slot.carta, x = slot.carta.slot_inicial.rect.x, y = slot.carta.slot_inicial.rect.y + 109, tweenTime = 0.2, tweenType = pytweener.Easing.Linear.easeIn, onCompleteFunction = slot.carta.reempotrar)
                            slot.carta = None
                            self.reacomodar(slot)
                            break
    def agregar_carta(self, carta):
        for slot in self.slots:
            if slot.carta == None:
                slot.carta = carta
                break
    def reacomodar(self, slot_movido):
        slot_ant = slot_movido
        for slot in self.slots:
            if slot.rect.centerx > slot_movido.rect.centerx and slot.carta:
                engine.obtener_director().escena_actual.cartas.append(slot.carta)
                self.tweener.addTween(slot.carta, x = slot_ant.rect.x, y = slot_ant.rect.y, tweenTime = 0.2, tweenType = pytweener.Easing.Linear.easeIn, onCompleteFunction = slot.carta.empotrar)
                slot.carta = None
                slot_ant = slot

class PlantaSeleccionada(object):
    def __init__(self, slot):
        self.slot = slot
        self.carta = slot.carta
        self.imagen = engine.cargar_imagen(self.carta.clase.url_imagen, True)
        self.grilla = Grilla(self.carta.clase.url_imagen, self.carta.clase.cantidad[0], self.carta.clase.cantidad[1])
        self.rect = engine.pygame.Rect(0, 0, self.grilla.ancho, self.grilla.alto)
        self.rect_origen = self.grilla.obtener_cuadro(self.carta.clase.cuadro_alpha)
        self.rect_fondo = engine.pygame.Rect(0, 0, self.grilla.ancho, self.grilla.alto)
        self.plantable = 2
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect, self.rect_origen)
    def verificar_eventos(self, evento):
        if evento.type == locals.MOUSEMOTION:
            x, y = evento.pos
            i = (y - 120) / 104
            j = (x - 50) / 100
            if i in range(0, 6) and j in range(0, 9):
                self.rect_fondo.right = 50 + engine.obtener_director().escena_actual.ancho_cuadro * (j + 1)
                self.rect_fondo.bottom = 120 + engine.obtener_director().escena_actual.alto_cuadro * (i + 1)
                if engine.obtener_director().escena_actual.lineas[i] == self.carta.info['campo']:
                    if ((engine.obtener_director().escena_actual.tablero[i][j] and engine.obtener_director().escena_actual.tablero[i][j].__class__ == self.carta.base) or (not engine.obtener_director().escena_actual.tablero[i][j] and self.carta.base == None)):
                        self.plantable = 0
                        if engine.obtener_director().escena_actual.tablero[i][j].__class__ == Nenufar and engine.obtener_director().escena_actual.tablero[i][j].contenido != None:
                            self.plantable = 2
                    else: self.plantable = 2
                else:
                    if engine.obtener_director().escena_actual.tablero[i][j] and engine.obtener_director().escena_actual.tablero[i][j].__class__ == Nenufar and engine.obtener_director().escena_actual.tablero[i][j].contenido == None:
                        self.plantable = 1
                    else:
                        self.plantable = 2
            else:
                self.plantable = 2
    def dibujar_posible(self, superficie):
        if self.plantable == 0 or self.plantable == 1:
            self.dibujar_alpha(superficie, self.imagen, self.rect_fondo, 130, self.rect_origen)
    def dibujar_alpha(self, fondo, imagen, rect_fondo, opacidad, rect_origen):
        temp = engine.pygame.Surface((rect_fondo.width, rect_fondo.height)).convert()
        temp.blit(fondo, (0, 0), rect_fondo)
        temp.blit(imagen, (0, 0), rect_origen)
        temp.set_alpha(opacidad)
        fondo.blit(temp, rect_fondo)
    def actualizar(self, tiempo):
        self.rect.centerx, self.rect.centery = engine.pygame.mouse.get_pos()
    def verificar_bases(self):
        for fila in engine.obtener_director().escena_actual.tablero:
            for p in fila:
                if p and p.__class__ == self.carta.clase.base:
                    print "encontre una base"

class Carta(object):
    def __init__(self, rect_origen, cls, nombre, descripcion, precio, campo, tipo, tiempo_charge = 3, base = None):
        self.rect_origen_carta = rect_origen
        self.rect = engine.pygame.Rect(0, 0, 85, 121)
        self.clase = cls
        self.x = 0
        self.y = 0
        self.slot_inicial = None
        self.info = {
                     'nombre':nombre,
                     'descripcion:':descripcion,
                     'precio':precio,
                     'campo':campo,
                     'tipo':tipo,
                     }
        self.tiempo_charge = tiempo_charge
        self.base = base
    def dibujar(self, superficie):
        superficie.blit(engine.obtener_director().escena_actual.imagen_cartas, self.rect, self.rect_origen_carta)
    def actualizar(self, superficie):
        self.rect.x, self.rect.y = self.x, self.y
    def empotrar(self):
        engine.obtener_director().escena_actual.barra_control.agregar_carta(self)
        engine.obtener_director().escena_actual.cartas.pop(0)
    def reempotrar(self):
        self.slot_inicial.usado = False
        engine.obtener_director().escena_actual.cartas.pop(0)

class SlotBarra(object):
    def __init__(self, rect):
        self.carta = None
        self.rect = rect
        self.cargando = False
        self.rect_charge = engine.pygame.Rect(0, 0, self.rect.width, 0)
        self.tweener = pytweener.Tweener()
        self.falta_cargar = 0
    def dibujar(self, superficie):
        if self.carta: 
            superficie.blit(engine.obtener_director().escena_actual.imagen_cartas, self.rect, self.carta.rect_origen_carta)
            if engine.obtener_director().escena_actual.barra_control.soles < self.carta.info['precio'] and engine.obtener_director().escena_actual.barra_control.eligiendo == 2: superficie.blit(engine.obtener_director().escena_actual.imagen_nosoles, self.rect)
        superficie.blit(engine.obtener_director().escena_actual.imagen_charge, self.rect, self.rect_charge)
    def actualizar(self, tiempo):
        self.rect_charge.height = self.falta_cargar
        if self.tweener.hasTweens():
            self.tweener.update(tiempo / 1000.0)
    def oscurecer(self):
        self.falta_cargar = self.rect.height
    def aclarar(self):
        self.falta_cargar = 0
    def cargar(self):
        if self.carta:
            self.tweener.addTween(self, falta_cargar = 0, tweenTime = self.carta.tiempo_charge, tweenType = pytweener.Easing.Linear.easeIn, onCompleteFunction = self.terminar_cargado)
            self.cargando = True
    def terminar_cargado(self):
        self.cargando = False
        self.falta_cargar = 0
            
class Input(object):
    def __init__(self, x, y):
        self.text = ""
        self.palabra = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 50), self.text, 1, (255, 255, 255))
        self.parpadeante = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 50), "|", 1, (255, 255, 255))
        self.x, self.y = x, y
        self.xp = self.x - 3
        self.visible = True
        self.indice = len(self.text)
        self.seleccionado = False
    def dibujar(self, superficie):
        if self.seleccionado: superficie.blit(self.seleccion, (self.x, self.y))
        if self.visible: superficie.blit(self.parpadeante, (self.xp, self.y))
        superficie.blit(self.palabra, (self.x, self.y))
    def actualizar(self, tiempo):
        if not self.seleccionado: self.palabra = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 50), self.text, 1, (255, 255, 255))
        else: self.palabra = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 50), self.text, 1, (0, 0, 0))
        if 0 <= engine.pygame.time.get_ticks() % 1000 <= 500:
            self.visible = False
        else: self.visible = True
        self.xp = self.x + engine.pygame.font.Font.render(engine.pygame.font.Font(None, 50), self.text[0:self.indice], 1, (255, 255, 255)).get_width() - 3
    def verificar_eventos(self, evento):
        if evento.type == locals.KEYDOWN:
            if evento.key == 275 and self.indice < len(self.text):
                self.indice += 1
            elif evento.key == 275 and self.indice == len(self.text):
                self.deseleccionar()
            elif evento.key == 276 and self.indice > 0:
                if not self.seleccionado: self.indice -= 1
                else:
                    self.deseleccionar()
                    self.indice = 0
            elif evento.key != 8 and evento.key != 13 and evento.key != 275 and evento.key != 276 and evento.key != 304 and len(self.text) < 15:
                if self.seleccionado:
                    self.deseleccionar()
                    self.text = ""
                    self.indice = 0
                self.text = self.text[0:self.indice] + evento.unicode + self.text[self.indice:len(self.text)]
                self.indice += 1
            elif evento.key == 8 and self.indice > 0:
                if self.seleccionado:
                    self.deseleccionar()
                    self.text = ""
                    self.indice = 0
                else:
                    self.text = self.text[0:self.indice - 1] + self.text[self.indice:len(self.text)]
                    self.indice -= 1
    def seleccionar(self):
        if len(self.text) > 0:
            self.seleccionado = True
            self.palabra = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 50), self.text, 1, (0, 0, 0))
            self.seleccion = engine.pygame.Surface((self.palabra.get_width(), self.palabra.get_height()))
            self.seleccion.fill((255, 255, 255))
            self.indice = len(self.text)
    def deseleccionar(self):
        self.seleccionado = False
        self.seleccion = None

class Boton(object):
    def __init__(self, x, y, imagen, comando = None, nombre = None):
        self.imagen = imagen
        self.rect = self.imagen.get_rect()
        self.mask = engine.pygame.mask.from_surface(self.imagen, 127)
        self.rect.x = x
        self.rect.y = y
        self.comando = comando
        self.presionado = False
        self.nombre = engine.pygame.font.Font.render(engine.pygame.font.Font(None, 32), nombre.upper(), 1, (0, 174, 0)) if nombre else None
        self.rect_nombre = self.nombre.get_rect() if self.nombre else None
        if self.rect_nombre: self.rect_nombre.center = self.rect.center
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)
        if self.nombre: superficie.blit(self.nombre, self.rect_nombre)
    def verificar_eventos(self, evento):
        if evento.type == locals.MOUSEBUTTONDOWN and evento.button == 1:
            if engine.pygame.sprite.spritecollideany(self, [engine.cursor], engine.pygame.sprite.collide_mask):
                if not self.presionado:
                    self.presionado = True
                    self.rect.x = self.rect.x + 3
                    self.rect.y = self.rect.y + 3
        elif evento.type == locals.MOUSEBUTTONUP and evento.button == 1 and self.presionado:
            self.presionado = False
            self.rect.x = self.rect.x - 3
            self.rect.y = self.rect.y - 3
            if self.rect_nombre: self.rect_nombre.center = self.rect.center
            if engine.pygame.sprite.spritecollideany(self, [engine.cursor], engine.pygame.sprite.collide_mask):
                if self.comando: self.comando()
    def actualizar(self, tiempo):
        if self.rect_nombre: self.rect_nombre.center = self.rect.center
    
