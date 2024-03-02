import enum

class CartaValor(enum.Enum):

    #Val. numericos
    CERO = 0
    UNO = 1
    DOS = 2
    TRES = 3
    CUATRO = 4
    CINCO = 5
    SEIS = 6
    SIETE = 7
    OCHO = 8
    NUEVE = 9

    #Comodin color
    TOMA_DOS = 10
    QUITA_TURNO = 11
    CAMBIA_SENTIDO = 12

    #Comodin negro
    CAMBIA_COLOR = 13
    TOMA_CUATRO = 14

