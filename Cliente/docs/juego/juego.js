//RUTAS
const RUTA_IMAGENES = "img/"
const RUTA_IMG_CARTAS = RUTA_IMAGENES + "cartas/"

//Estados juego
const SIN_INICIAR = 0
const EN_CURSO = 1
const TERMINO = 2
const ESPERANDO_COLOR = 3
const ESPERANDO_COLOR_MAS_4 = 4
const EN_TURNO = 5

//Botones
const btn_accion = document.getElementById("btn_accion")
const btn_iniciar = document.getElementById("iniciar_juego")
const btn_salir = document.getElementById("salir_juego")

//Modal colores
const btn_mod_amarillo = document.getElementById("md_amarillo")
const btn_mod_verde = document.getElementById("md_verde")
const btn_mod_azul = document.getElementById("md_azul")
const btn_mod_rojo = document.getElementById("md_rojo")

//Tablero
const carta_tablero = document.getElementById("carta_tablero")

//Contenedores
const ctr_total_cartas = document.getElementById("jugador_info")
const ctr_baraja = document.getElementById("baraja")
const ctr_estado_juego = document.getElementById("estado_juego")
const ctr_tablero_color = document.getElementById("color_tablero")

//Tabla
const tbl_jugadores = document.getElementById("jugadores_tabla_body")

// Locales
const JUGADOR_LOCAL = {
    sid: 0,
    id: 0,
    nombre: null,
    cartas: [],
    es_host: false
}

const TABLERO = {
    carta: null,
    color: null
}

var pasa_turno = false
var reversa = false

//Actualiza el tablero (Color en juego y carta)
function actualizar_tablero(color_carta, valor_carta, color_tablero) {

    //Actualiza la carta en tablero
    var ruta = RUTA_IMG_CARTAS + color_carta.toLowerCase() + "/" + convertir_valor_carta(valor_carta) + ".png"
    carta_tablero.setAttribute("src", ruta)
    carta_tablero.onerror = () => {
        carta_img.setAttribute("src", RUTA_IMG_CARTAS + "cara.png")
    }

    //Actualiza el color del tablero
    switch (color_tablero) {
        case "AMARILLO":
            ctr_tablero_color.style["background-color"] = "#fff800"
            break
        case "VERDE":
            ctr_tablero_color.style["background-color"] = "#03c04a"
            break
        case "AZUL":
            ctr_tablero_color.style["background-color"] = "#00cfff"
            break
        case "ROJO":
            ctr_tablero_color.style["background-color"] = "#d21f3c"
            break
        default:
            ctr_tablero_color.style["background-color"] = "#1b1b1b"
    }
}

//Actualiza la tabla de jugadores
function actualizar_jugadores(jugadores) {

    let tabla_jugadores2 = document.getElementById("jugadores_tabla")

    //Actualiza las filas de la tabla
    for (let i = 1; i < tabla_jugadores2.rows.length; i++) {

        let fila = tabla_jugadores2.rows[i]

        //Verifica si existe un jugador
        jugador = null
        try {
            jugador = jugadores[i - 1]
        } catch (error) {
            jugador = null
        }

        //Actualiza la info del jugador
        if (jugador) {
            fila.setAttribute("j-id", jugador.id)
            fila.cells[0].innerHTML = jugador.nombre
            fila.cells[1].innerHTML = jugador.ctd_cartas
        } else {
            fila.cells[0].innerHTML = "--"
            fila.cells[1].innerHTML = "--"
        }
    }
}

//Actualiza la informacion en tabla del jugador local
function actualizar_jugador_local(jugador) {

    let tabla_jugadores2 = document.getElementById("jugadores_tabla")
    let fila = tabla_jugadores2.rows[jugador.id + 1]
    let local_row = document.getElementById("row_local")
    if (local_row) {
        local_row.setAttribute("id", "")
    }
    fila.setAttribute("id", "row_local")
}

//Convierte un valor numerico a string para la ruta de la imagen
function convertir_valor_carta(valor) {

    let n_valor = valor
    switch (valor) {
        case 10:
            n_valor = "+2"
            break
        case 11:
            n_valor = "bloqueo"
            break
        case 12:
            n_valor = "reversa"
            break
        case 13:
            n_valor = "color"
            break
        case 14:
            n_valor = "+4"
            break
        default:
            n_valor = valor.toString()
    }
    return n_valor
}

//Carga las cartas del jugador local
function actualizar_cartas_jugador(cartas, funcion = null) {

    ctr_baraja.innerHTML = "" //Limpia la baraja
    if (cartas.length > 0) {
        ctr_total_cartas.innerHTML = "Total Cartas: " + cartas.length
        for (c of cartas) {
            agregar_carta(cartas.indexOf(c), c.color, convertir_valor_carta(c.valor), funcion)
        }
    } else {
        ctr_total_cartas.innerHTML = "Sin Cartas"
    }
}

//Agrega una carta a la baraja
function agregar_carta(idx = -1, color, valor, funcion = null) {

    //Crea la imagen de la carta
    carta = crear_carta(color.toLowerCase(), valor)
    carta.setAttribute("b-id", idx)

    //Funcion al clickear la carta
    if (funcion != null) {
        carta.addEventListener("click", () => {
            funcion(idx)
        })
    }

    //Agrega la carta a la baraja
    ctr_baraja.appendChild(carta)
}

//Crea la imagen de la carta con el color y valor
function crear_carta(color, valor) {

    //Busca la ruta y crea los componentes de la imagen
    let ruta = RUTA_IMG_CARTAS + color + "/" + valor + ".png"
    let carta = document.createElement("div")
    let carta_img = document.createElement("img")

    //Agrega los atributos de la carta
    carta_img.setAttribute("class", "carta_baraja_img")
    carta_img.setAttribute("src", ruta)
    carta_img.onerror = () => {
        carta_img.setAttribute("src", RUTA_IMG_CARTAS + "cara.png")
    }

    //Agrega los atributos del contenedor de la carta
    carta.setAttribute("class", "carta_baraja")
    carta.appendChild(carta_img)

    return carta
}

function actualizar_estado_n(estado) {

    var texto = "En espera..."
    switch (estado) {
        case SIN_INICIAR:
            texto = "Esperando a iniciar..."
            break
        case EN_CURSO:
            ctr_estado_juego.style["background-color"] = "#39b549"
            texto = "Otro jugador esta en turno "
            break
        case TERMINO:
            ctr_estado_juego.style["background-color"] = "#1b1b1b"
            texto = "El juego termino!"
            break
        case ESPERANDO_COLOR:
        case ESPERANDO_COLOR_MAS_4:
            ctr_estado_juego.style["background-color"] = "#ffd300"
            texto = "Esperando la eleccion de color del otro jugador... "
            break
        case EN_TURNO:
            ctr_estado_juego.style["background-color"] = "#8A2BE2"
            texto = "Es tu turno, juega una carta, toma del mazo o salta el turno "
            break
        default:
            ctr_estado_juego.style["background-color"] = "#2B9EB3"
    }

    if (reversa) {
        texto = "Juego en reversa | " + texto
    }
    ctr_estado_juego.innerHTML = texto
}

//Actualiza la barra del estado del juego
function actualizar_estado(estado, msg = "") {


    var texto = "En espera..."
    switch (estado) {
        case "SIN_INICIAR":
            texto = "Esperando a iniciar..."
            break
        case "EN_JUEGO":
            ctr_estado_juego.style["background-color"] = "#39b549"
            texto = "Otro jugador esta en su turno " + msg
            break
        case "TURNO":
            ctr_estado_juego.style["background-color"] = "#8A2BE2"
            texto = "Es tu turno, juega una carta, toma del mazo o salta el turno " + msg
            break
        default:
            texto = "En juego..."
            ctr_estado_juego.style["background-color"] = "#2B9EB3"
    }
    ctr_estado_juego.innerHTML = texto
}

//Redirige al jugador a la pagina de usuarios
function mensaje_pagina(msg) {
    document.location.href = "../mensajes/mensajes.html?msg=" + msg
}