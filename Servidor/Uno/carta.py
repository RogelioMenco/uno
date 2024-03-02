class Carta:
    
    def __init__(self, valor, color, comodin=False):
        self.valor = valor
        self.color = color
        self.comodin = comodin
    
    def __str__(self):
        return self.color.name + " -> " + self.valor.name + " -> " + str(self.comodin)

    def mismo_color(self, color):
        return self.color.value == color.value

    def mismo_valor(self, valor):
        return self.valor.value == valor.value
    
    def es_comodin(self):
        return self.comodin