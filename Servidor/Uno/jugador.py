class Jugador:

    """
    Se encarga de almacenar las cartas y tirarlas en partida
    """

    def __init__(self, nombre):
        self.cartas = []
        self.index = 0
        self.nombre = nombre
        self.saltar_turno = False
        self.sid = None
        self.en_juego = False

    def dar_carta(self, carta):
        self.cartas.append(carta)

    def tirar_carta(self, carta):
        self.cartas.remove(carta)

    def __str__(self):
        jug = "\nNombre: " + self.nombre + " - Index: " + str(self.index) + " - SID: " + str(self.sid)
        jug += "\n[=====================================]\n"
        for carta in self.cartas:
            jug += str(self.cartas.index(carta)) + ") " + str(carta)+"\n"
        jug += "[=====================================]\n"

        return jug
