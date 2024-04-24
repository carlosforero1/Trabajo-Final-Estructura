class Pila:
    def __init__(self):
        self.datos = []

    def apilar(self, elemento):
        self.datos.append(elemento)

    def desapilar(self):
        if not self.esta_vacia():
            return self.datos.pop()
        else:
            print("La pila está vacía.")
            return None

    def esta_vacia(self):
        return len(self.datos) == 0

    def ver_cima(self):
        if not self.esta_vacia():
            return self.datos[-1]
        else:
            print("La pila está vacía.")
            return None
