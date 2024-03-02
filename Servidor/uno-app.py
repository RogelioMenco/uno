from Uno.juego_acciones import JuegoAccion
from Uno.partida import UNO
from Uno.jugador import Jugador
from flask import Flask, request
from flask_socketio import SocketIO, emit

# Configuracion
app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins="*")

# Juego y jugadores
uno = UNO()
jugadores = []

# El jugador entra en la partida
@socket.on("connect")
def conectado():  # OK

    # Variables
    global uno
    jugador = Jugador("Jugador " + str(len(uno.jugadores) + 1))

    if(uno.estado == UNO.SIN_INICIAR):

        if(uno.registrar_jugador(jugador)):

            # Guarda el jugador relacionado en el socket y envia la informacion del jugador al cliente
            jugador.sid = request.sid
            jugadores.append(jugador)

            # Verifica si el jugador es host del juego para notificar al cliente
            es_host = False
            if(len(uno.jugadores) == 1 and uno.asignar_host(jugador)):
                es_host = True

            #Actualiza el jugador y el juego
            actualizar_jugador(jugador, es_host)
            actualizar_juego()
        else:
            emit("sala_llena", None)
    else:
        emit("juego_iniciado")

# El jugador se desconecta


@socket.on("disconnect") #OK
def desconectar():

    #Obtiene el jugador si existe en el juego
    jugador = None
    for j in uno.jugadores:
        if(j.sid == request.sid):
            jugador = j
            break
    
    #Existe el juego aun y el jugador esta en el
    if(jugador != None and uno.sale_jugador(jugador)):
        socket.emit("salio_jugador", {"nombre": jugador.nombre})
        for j in uno.jugadores:
            if(j == uno.jugador_host):
                actualizar_jugador(j, True)
            else:
                actualizar_jugador(j)
        actualizar_juego()

        if(uno.jugador_en_curso != None):
            socket.emit("en_turno", room=uno.jugador_en_curso.sid)

# El juego se va a iniciar

@socket.on("iniciar_uno")  # OK
def iniciar_uno():

    if(uno.estado == UNO.SIN_INICIAR):
        # Obtiene el jugador de la lista
        jugador = None
        for jug in uno.jugadores:
            if(jug.sid == request.sid):
                jugador = jug
                break

        # Verifica que el jugador sea el host
        if(jugador != None and uno.jugador_host == jug):
            if(uno.iniciar()):
                actualizar_juego()  # Actualiza para todos los jugadores

                # Actualiza las cartas de todos los jugadores
                for j in uno.jugadores:
                    actualizar_cartas(j)

                # Notifica al usuario en turno
                socket.emit("en_turno", room=uno.jugador_en_curso.sid)

            else:
                emit("error_uno", {"msg": "No hay suficientes jugadores para inciar la partida!"})


@socket.on("jugar_carta")
def jugar_carta(id): #OK

    # Verifica que el jugador tenga el turno y que el juego este en curso
    if(uno.jugador_en_curso.sid == request.sid and uno.estado == UNO.EN_CURSO):

        jug = uno.jugador_en_curso

        # Verifica que el jugador tenga la carta y en caso tal la toma
        carta_jug = None
        try:
            if(id >= 0):
                carta_jug = uno.jugador_en_curso.cartas[id]
        except:
            carta_jug = None

        # Si hay una carta verifica que se pueda colocar
        if(carta_jug != None):
            accion = uno.poner_carta(uno.jugador_en_curso, carta_jug)

            # Verifica que la accion sea valida (El jugador coloco y se cambia al proximo si es posible)
            if(accion != JuegoAccion.MOV_INVALIDO):

                # Actualiza las cartas del jugador que coloco, el juego para todos y la accion
                actualizar_cartas(jug)
                actualizar_juego()
                socket.emit("accion_carta", {"estado": accion.name})

                #Si es comodin negro se notifica al jugador que debe elegir color, si no, cambia turno
                if(accion == JuegoAccion.TOMA_CUATRO or accion == JuegoAccion.CAMBIO_COLOR and len(jug.cartas) > 0):
                    emit("pedir_color")
                else:
                    # La ultima carta fue un +2, el jugador ya cambio, por lo que debe actualizar sus cartas
                    if(accion == JuegoAccion.TOMA_DOS):
                        actualizar_cartas(uno.jugador_en_curso)

                    #Verifica que no haya terminado el juego
                    if(uno.jugador_en_curso != None):
                        socket.emit("en_turno", room=uno.jugador_en_curso.sid)
                
                return

            emit("error_uno", {"msg": "No puedes jugar con esta carta!"})


# El jugador que estaba en curso eligio un color
@socket.on("nuevo_color")
def nuevo_color(color):

    #Verifica que el juego este en estado de espera
    if(uno.estado == UNO.ESPERANDO_COLOR_MAS_4 or uno.estado == UNO.ESPERANDO_COLOR):

        #Verifica que el jugador sea el mismo que debe colocar el colo
        if(uno.jugador_en_curso.sid == request.sid):

            color = int(color)

            #Verifica que el color este en el rango
            if(color > 0 and color <= 4):
                uno.actualizar_color(color)
                actualizar_juego() #Actualiza para todos los jugadores
                actualizar_cartas(uno.jugador_en_curso) #Actualiza las cartas del siguiente jugador por si hubo +4
                socket.emit("en_turno", room=uno.jugador_en_curso.sid) #Le notifica del turno
            else:
                emit("error_uno", {"msg":"El color seleccionado no es valido!"})


@socket.on("actualizar")  # OK
def actualizar_juego():

    arr_jugadores = []
    carta_tablero = None
    color_tablero = None
    jug_actual_idx = None

    # Agrega todos los jugadores al arreglo
    for jug in uno.jugadores:
        arr_jugadores.append(
            {"id": jug.index, "nombre": jug.nombre, "ctd_cartas": len(jug.cartas)})

    # Busca el indice del jugador en turno si existe
    if(uno.jugador_en_curso != None):
        jug_actual_idx = uno.jugador_en_curso.index

    # Carga la carta y color en tablero
    carta_t = uno.tablero.carta_en_curso
    if(carta_t != None):
        carta_tablero = {"color": carta_t.color.name,
                         "valor": carta_t.valor.value}

    color_t = uno.tablero.color_en_curso
    if(color_t != None):
        color_tablero = color_t.name

    juego_json = {
        "estado": uno.estado,
        "reversa": uno.reversa,
        "carta_tablero": carta_tablero,
        "color_tablero": color_tablero,
        "jugador_actual": jug_actual_idx,
        "jugadores": arr_jugadores
    }

    socket.emit("info_uno", juego_json)

    if(uno.estado == UNO.TERMINO):
        juego_terminado()

@socket.on("tomar_carta")
def tomar_carta():

    #Verifica que el juego este en curso, que el jugador sea el que tiene el turno
    if(uno.estado == UNO.EN_CURSO and uno.jugador_en_curso.sid == request.sid):

        jug = uno.jugador_en_curso

        #Verifica si el jugador puede tomar carta
        if(jug.saltar_turno == False):
            uno.tomar_carta_mazo(jug)
            actualizar_cartas(jug)
            emit("tomo_carta")
            actualizar_juego()
            return

        emit("error_uno", {"msg":"No puedes tomar cartas, debes jugar una carta o saltar tu turno"})

@socket.on("saltar_turno")
def saltar_turno():

    #Verifica que el juego este en curso, que el jugador sea el que tiene el turno
    if(uno.estado == UNO.EN_CURSO and uno.jugador_en_curso.sid == request.sid):

        jug = uno.jugador_en_curso

        #Verifica si el jugador puede saltar el turno
        if(jug.saltar_turno == True):
            uno.saltar_turno(jug)
            emit("salta_turno")
            actualizar_juego() #Actualiza el juego para todos los jugadores
            socket.emit("en_turno", room=uno.jugador_en_curso.sid)
            return

        emit("error_uno", {"msg":"No puedes saltar el turno, debes jugar una carta o tomar del mazo"})

def actualizar_cartas(jugador):  # OK

    cartas_json = []

    for carta in jugador.cartas:
        cartas_json.append({"id": jugador.cartas.index(
            carta), "color": carta.color.name, "valor": carta.valor.value})
    # Envia las cartas a los jugadores

    socket.emit("jug_cartas", {
        "jug_id": jugador.index,
        "cartas": cartas_json
    }, room=jugador.sid)

def actualizar_jugador(jugador, es_host=False):
    
    if(jugador != None):
        socket.emit("actualizar_jugador",{
                    "sid": jugador.sid,
                    "id": jugador.index,
                    "nombre": jugador.nombre,
                    "cartas": len(jugador.cartas),
                    "es_host": es_host
                }, room=jugador.sid)

def juego_terminado():

    global uno

    #Verifica que el juego haya terminado
    if(uno.estado == UNO.TERMINO):
        ganador = uno.ganador
        if(ganador != None):
            socket.emit("es_ganador", room=ganador.sid)

            #Envia a todos los jugadores el ganador
            for j in uno.jugadores:
                if (j.sid != ganador.sid):
                    socket.emit("hay_ganador", {"id": ganador.index,"nombre": ganador.nombre}, room=j.sid)
        uno = UNO()

# Main inicio
if __name__ == "__main__":
    socket.run(app, debug=True)
