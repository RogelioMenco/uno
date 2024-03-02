from Uno.carta_valor import CartaValor
from Uno.color_carta import CartaColor
from Uno.juego_acciones import JuegoAccion

class ManejadorJugadas:

    """
    Valida los movimientos del tablero para la proxima carta
    """

    def __init__(self):
        pass
        #self.state = True

    def validar_jugada(self, carta, carta_en_curso, color_tablero):

        #Verifica si la carta es comodin
        if(carta.es_comodin() and carta.valor.value > 9):

            #Si la carta es comodin negro se puede lanzar
            if(carta.color != CartaColor.NEGRO):
                    
                #En caso de no ser comodin negro verifica que el valor o color sean iguales
                if(carta_en_curso.mismo_color(carta.color) or carta_en_curso.mismo_valor(carta.valor) or carta.mismo_color(color_tablero)):
                    return True
            else:
                return True
        #La carta no es comodin, es un numero normal
        else:
            #Verifica si el color o valor es el mismo de la ultima carta
            if(carta_en_curso.mismo_color(carta.color) or carta_en_curso.mismo_valor(carta.valor) or carta.mismo_color(color_tablero)):
                return True
        return False
    
    #Verifica dependiendo de la carta la accion a realizar
    def accion_carta(self, carta):
        
        accion = JuegoAccion.CONTINUAR

        #Verifica que la carta sea un comodint
        if(carta.valor.value > 9 and carta.es_comodin()):
            
            #Comodines de color
            if(carta.valor == CartaValor.QUITA_TURNO):
                accion =  JuegoAccion.BLOQUEAR_PROXIMO
            elif(carta.valor == CartaValor.CAMBIA_SENTIDO):
                accion =  JuegoAccion.REVERSA
            elif(carta.valor == CartaValor.TOMA_DOS):
                  accion = JuegoAccion.TOMA_DOS

            #Comodines negros
            elif(carta.valor == CartaValor.CAMBIA_COLOR):
                accion = JuegoAccion.CAMBIO_COLOR
            elif(carta.valor == CartaValor.TOMA_CUATRO):
                accion =  JuegoAccion.TOMA_CUATRO
                
        return accion
            