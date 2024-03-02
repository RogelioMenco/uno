const SERVER_IP = "http://127.0.0.1:5000";

//Socket
var socket = null

//Carga la pagina
document.addEventListener("DOMContentLoaded", function(event) {

    iniciar_botones() //Inicia los botones
    socket = io.connect(SERVER_IP) //Conecta al servidor
    $(".owl-carousel").owlCarousel(); //Baraja

    //Conexion socket
    socket.on("connect", () => {
        console.log("Conectado al servidor!")
    })

    socket.on("connect_error", () => {
        error_conexion()
    })

    //El juego debe ser actualizado
    socket.on("info_uno", (data) => {
        actualizar_juego(data)
    })

    //Entro al juego, recibe la informacion del jugador local
    socket.on("actualizar_jugador", (data) => {
        cargar_jugador_local(data)
    })

    //Actualiza las cartas del jugador
    socket.on("jug_cartas", (data) => {
        actualizar_cartas(data)
    })

    //Es el turno del jugador
    socket.on("en_turno", () => {
        entra_turno()
    })

    //El jugador debe seleccionar un color
    socket.on("pedir_color", () => {
        leer_color()
    })

    //Accionaron una carta
    socket.on("accion_carta", (data) => {
        recibe_accion(data)
    })

    //Toma carta
    socket.on("tomo_carta", () => {
        tomo_carta()
    })

    //Salta turno
    socket.on("salta_turno", () => {
        salta_turno()
    })

    //El juego termino y hay ganadores
    socket.on("hay_ganador", (data) => {
        hay_ganador(data)
    })

    socket.on("es_ganador", () => {
        es_ganador()
    })

    //Salio un jugador
    socket.on("salio_jugador", (data) => {
        salio_jugador(data)
    })

    //Errores
    socket.on("error_uno", (msg) => {
        error_uno(msg)
    })

    //Salas llenas o juego iniciado
    socket.on("sala_llena", () => {
        sala_llena()
    })
    socket.on("juego_iniciado", () => {
        juego_iniciado()
    })
})

//Redirige a otra pagina cuando no se puede conectar al servidor
function error_conexion() {
    mensaje_pagina("Se perdio la conexión con el servidor!")
}

//Actualiza el juego
function actualizar_juego(data) {

    //Jugadores
    actualizar_jugadores(data.jugadores)

    //Carta en tablero
    let carta_t = data.carta_tablero
    let color_t = data.color_tablero
    if (carta_t != null) {
        TABLERO.carta = carta_t
        TABLERO.color = color_t
        actualizar_tablero(carta_t.color, carta_t.valor, color_t)
    }
    reversa = data.reversa

    //Estado
    actualizar_estado_n(data.estado)
}

// Jugador local
function cargar_jugador_local(data) {

    JUGADOR_LOCAL.sid = data.sid
    JUGADOR_LOCAL.id = data.id
    JUGADOR_LOCAL.nombre = data.nombre
    if (data.es_host && !JUGADOR_LOCAL.es_host) {
        btn_iniciar.style["visibility"] = "visible"
        mostrar_mensaje("Eres el host de la partida.")
    }
    JUGADOR_LOCAL.es_host = data.es_host
    actualizar_jugador_local(JUGADOR_LOCAL)
}

function actualizar_cartas(data) {
    JUGADOR_LOCAL.cartas = data.cartas
    actualizar_cartas_jugador(JUGADOR_LOCAL.cartas, poner_carta)
}

//Turno
function entra_turno() {
    actualizar_estado_n(EN_TURNO)
}

//Lectura del color en el usuario
function leer_color() {
    $('#modal_colores').modal({ backdrop: 'static', keyboard: false })
}

function enviar_color(color) {
    if (color > 0 && color <= 4) {
        socket.emit("nuevo_color", color)
    }
    $('#modal_colores').modal('toggle')
}

//Accion carta
function recibe_accion(data) {
    console.log(data)
}

//Acciones de la baraja
function tomo_carta() {
    pasa_turno = true
    btn_accion.innerHTML = "Saltar Turno"
}

function salta_turno() {
    pasa_turno = false
    btn_accion.innerHTML = "Tomar Carta"
}

//Ganador
function es_ganador() {
    mostrar_mensaje("Ganaste el juego!")
    setTimeout(() => {
        mensaje_pagina("Ganaste el juego!")
    }, 3000);
    socket.disconnect()
}

function hay_ganador(data) {
    mostrar_mensaje("El juego termino!\nEl jugador " + data.nombre + " es el ganador")
    setTimeout(() => {
        mensaje_pagina("El jugador '" + data.nombre + "' gano el juego")
    }, 3000);
    socket.disconnect()
}

//Notifica de la salida de un jugador
function salio_jugador(data) {
    mostrar_mensaje("El jugador '" + data.nombre + "' salio de la partida.")
}

//Caso de error
function error_uno(msg) {
    mostrar_mensaje(msg.msg)
}

//Envia la carta al servidor
function poner_carta(index) {
    socket.emit("jugar_carta", index)
}

//Modal mensaje
function mostrar_mensaje(msg = "Mensaje UNO") {
    var cnt_mgs = document.getElementById("mdl-msg-txt")
    cnt_mgs.innerHTML = msg
    $('#modal_mensajes').modal("toggle")
}

//Salida
function salir_juego() {
    socket.disconnect()
    mensaje_pagina("Saliste del juego")
}

function sala_llena() {
    socket.disconnect()
    mensaje_pagina("La sala del juego ya esta llena!")
}

function juego_iniciado() {
    socket.disconnect()
    mensaje_pagina("El juego ya inicio!")
}

//Inicia los botones de los modal
function iniciar_botones() {

    //Iniciar
    btn_iniciar.style["visibility"] = "hidden"
    btn_iniciar.addEventListener("click", () => {
        socket.emit("iniciar_uno")
    });

    //Salir
    btn_salir.addEventListener("click", () => {
        salir_juego()
    });

    //Accion baraja
    btn_accion.addEventListener("click", () => {
        if (pasa_turno) {
            socket.emit("saltar_turno")
        } else {
            socket.emit("tomar_carta")
        }
    });

    //Modal colores
    btn_mod_amarillo.addEventListener("click", () => {
        enviar_color(1)
    });

    btn_mod_verde.addEventListener("click", () => {
        enviar_color(2)
    });

    btn_mod_azul.addEventListener("click", () => {
        enviar_color(3)
    });

    btn_mod_rojo.addEventListener("click", () => {
        enviar_color(4)
    });
}