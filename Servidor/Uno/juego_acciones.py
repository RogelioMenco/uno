import enum


class JuegoAccion(enum.Enum):

    MOV_INVALIDO = 0

    # Comodin con color
    BLOQUEAR_PROXIMO = 1
    REVERSA = 2
    TOMA_DOS = 3

    # Comodin negro
    TOMA_CUATRO = 4
    CAMBIO_COLOR = 5

    # Cartas regulares
    CONTINUAR = 6
