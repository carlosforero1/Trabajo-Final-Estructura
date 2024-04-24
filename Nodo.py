class Nodo:
    def __init__(self, nombre, id, precio, cantidad):
        self.nombre = nombre
        self.id = id
        self.precio = precio
        self.cantidad = cantidad
        self.izquierdo = None
        self.derecho = None
