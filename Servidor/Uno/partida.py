from Uno.jugador import Jugador
from Uno.color_carta import CartaColor
from Uno.tablero import Tablero
from Uno.mazo import Mazo
from Uno.juego_acciones import JuegoAccion
from random import randint


class UNO():

    """
    Maneja las caracteristicas usadas por baraja, tablero y cuando el jugador pone carta
    Se encarga de ver si algun jugador gano, esta en uno o esta normal todo
    Tambien se encarga de dependiendo la jugada realizar la accion
    (Si sale un +4 del tablero, dar 4 cartas al siguiente jugador, etc..)
    """
    # ESTADOS DEL JUEGO
    SIN_INICIAR = 0
    EN_CURSO = 1
    TERMINO = 2
    ESPERANDO_COLOR = 3
    ESPERANDO_COLOR_MAS_4 = 4

    max_jugadores = 4
    min_jugadores = 2

    # CONSTRUCTOR
    def __init__(self):

        # ID Partida
        self.id = 1

        # Componentes del juego
        self.tablero = Tablero()
        self.mazo = Mazo()
        self.jugadores = []

        # Atributos
        self.ganador = None
        self.jugadores_en_uno = []
        self.jugador_en_curso = None
        self.reversa = False
        self.estado = UNO.SIN_INICIAR

        self.jugador_host = None

    # INICIA EL JUEGO
    def iniciar(self):

        # Verifica que existan los jugadores minimos para iniciar la partida
        if(len(self.jugadores) >= UNO.min_jugadores and self.estado == UNO.SIN_INICIAR):

            # Entrega a cada jugador las cartas
            for jugador in self.jugadores:
                for i in range(7):
                    jugador.dar_carta(self.mazo.toma_carta())

            # Pone la carta inicial
            self.tablero.poner_carta(self.mazo.tomar_carta_numero())

            # Elige el jugador que iniciara
            idx = randint(0, len(self.jugadores)-1)
            self.jugador_en_curso = self.jugadores[idx]

            # Actualiza el estado del juego
            self.estado = UNO.EN_CURSO
            return True
        else:
            return False

    # REGISTRA UN JUGADOR EN EL JUEGO
    def registrar_jugador(self, jugador):

        # Si no se ha llenado el juego, agrega el jugador
        if(len(self.jugadores) < UNO.max_jugadores and self.estado == UNO.SIN_INICIAR):

            # Agrega el jugador y actualiza su index
            self.jugadores.append(jugador)
            #jugador.index = self.jugadores.index(jugador)
            self.__organiza_index()
            return True
        return False

    # SACA EL JUGADOR DEL JUEGO
    def sale_jugador(self, jug):

        # Verifica que el jugador si este en el juego
        if(jug in self.jugadores):

            #Si estaba en espera de color el jugador
            if((self.estado == UNO.ESPERANDO_COLOR or self.estado == UNO.ESPERANDO_COLOR_MAS_4) and self.jugador_en_curso == jug):
                self.tablero.actualizar_color(CartaColor(randint(0,4)))
                self.estado = UNO.EN_CURSO

            # Verifica si es el jugador en curso para saltar al proximo
            if(self.jugador_en_curso == jug and self.estado != UNO.SIN_INICIAR):
                self.proximo_jugador()

            # Quita el jugador y su index
            self.jugadores.remove(jug)
            self.__organiza_index()
            jug.index = -1

            if(self.estado != UNO.SIN_INICIAR):

                #Verifica si solo queda un jugador en partida para terminar, si no actualiza el host
                if(len(self.jugadores) == 1):
                    self.ganador = self.jugadores[0]
                    self.estado = UNO.TERMINO
            #Verifica si el jugador anterior era host para actualizar
            if(len(self.jugadores) >= 1):
                if(jug == self.jugador_host):
                    self.jugador_host = self.jugadores[0]
            #Termina el juego si no hay jugadores
            else:
                self.estado = UNO.TERMINO
            return True
            
        return False
    
    # ASIGNA EL HOST DE LA PARTIDA A UN JUGADOR
    def asignar_host(self, jugador):
        if(self.jugador_host == None):
            self.jugador_host = jugador
            return True

        return False

    # PONE UNA CARTA EN EL TABLERO SI ES POSIBLE
    def poner_carta(self, jugador, carta):

        # Verifica que sea el jugador actual y pueda poner la carta que desea, luego pone y dependiendo la carta realiza la accion
        if(jugador == self.jugador_en_curso and self.tablero.puede_poner_carta(carta)):

            accion = self.tablero.poner_carta(carta)
            self.__analiza_jugada(accion)
            jugador.tirar_carta(carta)

            #Verifica las cartas del jugador para saber si el juego acaba
            if(len(jugador.cartas) == 0):
                self.ganador = jugador
                self.estado = UNO.TERMINO

            return accion

        return JuegoAccion.MOV_INVALIDO

    # ACUALIZA EL PROXIMO JUGADOR DEPENDIENDO DEL ESTADO
    def proximo_jugador(self, saltar=1):

        if(self.estado != UNO.TERMINO):
            idx_jugador = self.jugadores.index(self.jugador_en_curso)
            tam_jugadores = len(self.jugadores)

            # Dependiendo de si esta en reversa o no suma o resta al nuevo index
            if(self.reversa):

                # Salta dependiendo la cantidad recibida
                for i in range(saltar):
                    # Si se baja de 0 asigna la ultima posicion del arreglo
                    idx_jugador -= 1
                    if(idx_jugador < 0):
                        idx_jugador = tam_jugadores-1
            else:
                # Salta dependiendo la cantidad recibida
                for i in range(saltar):
                    # Si excede la ultima posicion del arreglo asigna la 0
                    idx_jugador += 1
                    if(idx_jugador >= tam_jugadores):
                        idx_jugador = 0

            # Actualiza el jugador
            self.jugador_en_curso = self.jugadores[idx_jugador]
            self.jugador_en_curso.saltar_turno = False
    
    # ACTUALIZA EL COLOR EN CASO DE QUE EL JUEGO ESTUVIERA ESPERANDO POR LA ELECCION DEL JUGADOR
    def actualizar_color(self, color):

        if(self.estado == UNO.ESPERANDO_COLOR or self.estado == UNO.ESPERANDO_COLOR_MAS_4):

            if(color > 0 and color <= 4):
                if(color == 1):
                    self.tablero.actualizar_color(CartaColor.AMARILLO)
                elif(color == 2):
                    self.tablero.actualizar_color(CartaColor.VERDE)
                elif(color == 3):
                    self.tablero.actualizar_color(CartaColor.AZUL)
                elif(color == 4):
                    self.tablero.actualizar_color(CartaColor.ROJO)

                self.proximo_jugador() #Cambia el jugador

                #Si estaba en +4 agrega las cartas al otro jugador
                if(self.estado == UNO.ESPERANDO_COLOR_MAS_4):
                    for i in range(4):
                        self.jugador_en_curso.dar_carta(self.mazo.toma_carta())

                self.estado = UNO.EN_CURSO #Actualiza el estado
        

    # TOMA UNA CARTA DE LA BARAJA Y QUEDA EN SALTO DE TURNO
    def tomar_carta_mazo(self, jugador):
        if(jugador == self.jugador_en_curso and jugador.saltar_turno == False):
            jugador.saltar_turno = True
            carta = self.mazo.toma_carta()
            jugador.dar_carta(carta)
            return carta
        return False

    # SALTA EL TURNO DEL JUGADOR ACTUAL
    def saltar_turno(self, jugador):
        if(jugador == self.jugador_en_curso and jugador.saltar_turno):
            jugador.saltar_turno = False
            self.proximo_jugador()
            return True
        return False

    # VERIFICA SI UN JUGADOR TIENE EL TURNO PARA PONER CARTAS
    def puede_jugar(self, jugador):
        return jugador == self.jugador_en_curso

    # DEPENDIENDO DE UNA ACCION DE COMODIN ACTUALIZA EL JUEGO
    def __analiza_jugada(self, accion):

        # Cambia de jugador y le da 4 cartas
        if(accion == JuegoAccion.TOMA_CUATRO):
            self.estado = UNO.ESPERANDO_COLOR_MAS_4

        # Pone el juego en estado de espera por color
        elif(accion == JuegoAccion.CAMBIO_COLOR):
            self.estado = UNO.ESPERANDO_COLOR


        # Cambia el jugador y le da 2 cartas
        elif(accion == JuegoAccion.TOMA_DOS):
            self.proximo_jugador()
            for i in range(2):
                self.jugador_en_curso.dar_carta(self.mazo.toma_carta())

        # Salta dos jugadores, el que se quita el turno, y deja el siguiente como jugador actual
        elif(accion == JuegoAccion.BLOQUEAR_PROXIMO):
            self.proximo_jugador(2)

        # Cambia el sentido del juego y luego los jugadores
        elif(accion == JuegoAccion.REVERSA):
            self.reversa = (not self.reversa)
            self.proximo_jugador()

        # Continua normalmente, unicamente cambia jugador
        elif(accion == JuegoAccion.CONTINUAR):
            self.proximo_jugador()

    # ASIGNA LOS INDEX DE LOS JUGADORES CON LOS DE SU POSICION EN EL ARREGLO
    def __organiza_index(self):
        for jug in self.jugadores:
            jug.index = self.jugadores.index(jug)

    # IMPRIME EL JUEGO
    def __str__(self):

        nombre_host = None
        nombre_jug_curso = None

        if(self.jugador_host != None):
            nombre_host = self.jugador_host.nombre
        
        if(self.jugador_en_curso != None):
            nombre_jug_curso = self.jugador_en_curso.nombre 

        par = "[================PARTIDA UNO================]\n"
        par += "* JUGADORES ("+str(len(self.jugadores))+"): \n"
        for jug in self.jugadores:
            par += "    - " + str(jug.nombre) + "\n"
        par += "\n* INFORMACION DE LA PARTIDA: \n"
        par += "    + Host: " + str(nombre_host) + "\n"
        par += "    + Estado: " + str(self.estado) + "\n"
        par += "    + Reversa: " + str(self.reversa) + "\n"
        par += "    + Prox. Jugador: " + str(nombre_jug_curso) + "\n"
        par += "\n" + str(self.tablero) + "\n"
        par += "[===========================================]\n"
        return par
