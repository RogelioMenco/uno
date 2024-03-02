from Uno.color_carta import CartaColor
from Uno.carta_valor import CartaValor
from Uno.juego_acciones import JuegoAccion
from Uno.manejador_jugadas import ManejadorJugadas

class Tablero():

    """
    Se encarga de manejar la ultima carta, validar que la proxima a poner sea valida
    y en retornar la accion a seguir (+4, reversa...)
    """

    def __init__(self) -> None:
        self.man_jugadas = ManejadorJugadas()
        self.carta_en_curso = None
        self.color_en_curso = None

    #Actualiza la carta en curso por la nueva si es valido el movimiento
    def poner_carta(self, carta):

        #Verifica que exista una carta en curso, si no es porque el juego hasta ahora inicia
        if(self.carta_en_curso):

            #Valida que este el color
            if(self.color_en_curso):

                #Valida el movimiento para colocar la carta
                if(self.man_jugadas.validar_jugada(carta, self.carta_en_curso, self.color_en_curso)):
                    self.__cambiar_carta(carta)
                    return self.man_jugadas.accion_carta(carta)
        else:
            self.__cambiar_carta(carta)
        
        return None

    #Valida si es posible poner la carta que se recibe
    def puede_poner_carta(self, carta):
        return self.man_jugadas.validar_jugada(carta, self.carta_en_curso, self.color_en_curso)

    #Actualiza el color en caso de que se encontrara esperando
    def actualizar_color(self, color):
        if(self.carta_en_curso and self.color_en_curso == None):
            self.color_en_curso = color

    #Actualiza la carta en curso con la nueva recibida
    def __cambiar_carta(self, carta):
        self.carta_en_curso = carta
        self.color_en_curso = carta.color
        if(carta.valor.value >= 13):
            self.color_en_curso = None

    def __str__(self):
        tab = "|------------TABLERO------------|\n"
        tab += "Carta: " + str(self.carta_en_curso) + "\n"
        tab += "Color: " + str(self.color_en_curso) + "\n"
        tab += "|-------------------------------|\n"
        return tab
