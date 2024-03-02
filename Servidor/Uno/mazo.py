from Uno.carta import Carta
from Uno.color_carta import CartaColor
from Uno.carta_valor import CartaValor
import random

class Mazo:

    """
    Solo se encarga de generar y dar cartas
    """

    def __init__(self) -> None:
        pass

    def toma_carta(self):
        prob_num = random.uniform(0,1)
        
        #Informacion para la carta
        valor = None
        color = None
        comodin = False

        #Carta comodin negra
        if(prob_num < 0.5):
            color = CartaColor.NEGRO
            comodin = True

            #Probabilidad para la carta especial
            if(random.uniform(0,1) < 0.4):
                valor = CartaValor.TOMA_CUATRO
            else:
                valor = CartaValor.CAMBIA_COLOR

        #Cartas de color normales
        else:
            color = self.__color_aleatorio() #Color aleatorio con la funcion

            #Comodin
            if(random.uniform(0,1) < 0.2):
                comodin = True
                valor = CartaValor(random.randint(10,12))
            
            #Numero normal
            else:
                valor = CartaValor(random.randint(0,9))

        #Retorna la carta creada
        return self.__crear_carta(valor, color, comodin)

    def tomar_carta_numero(self):
        carta = self.toma_carta()
        while(carta.valor.value > 9):
            carta = self.toma_carta()
        return carta

    #Carta de color con numero
    def __color_aleatorio(self):

        prob_num = random.uniform(0,1)
        color = None

        #Partes iguales en la probabilidad al momento de elegir color
        if(prob_num < 0.25):
            color = CartaColor.AZUL
        elif(prob_num < 0.50):
            color = CartaColor.AMARILLO
        elif(prob_num < 0.75):
            color = CartaColor.VERDE
        else:
            color = CartaColor.ROJO

        return color

    def __crear_carta(self, valor, color, comodin):

        if(valor != None and color != None):
            if(comodin and valor.value > 9):
                return Carta(valor, color, comodin)
            elif(comodin is False and valor.value < 10):
                return Carta(valor, color)