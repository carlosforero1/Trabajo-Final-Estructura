from Nodo import Nodo


class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, producto):
        # Si el árbol está vacío, el producto se convierte en la raíz
        if self.raiz is None:
            self.raiz = Nodo(producto["nombre"], producto["id"], producto["precio"], producto["cantidad"])
            return

        # Se busca el lugar adecuado para insertar el producto
        nodo_actual = self.raiz
        while True:
            if producto["id"] < nodo_actual.id:
                if nodo_actual.izquierdo is None:
                    nodo_actual.izquierdo = Nodo(producto["nombre"], producto["id"], producto["precio"], producto["cantidad"])
                    return
                else:
                    nodo_actual = nodo_actual.izquierdo
            else:
                if nodo_actual.derecho is None:
                    nodo_actual.derecho = Nodo(producto["nombre"], producto["id"], producto["precio"], producto["cantidad"])
                    return
                else:
                    nodo_actual = nodo_actual.derecho

    def buscar(self, id_producto):
        nodo_actual = self.raiz
        while nodo_actual is not None:
            if nodo_actual.id == id_producto:
                return nodo_actual
            elif id_producto < nodo_actual.id:
                nodo_actual = nodo_actual.izquierdo
            else:
                nodo_actual = nodo_actual.derecho
        return None

    def eliminar(self, id_producto):
        nodo_padre = None
        nodo_actual = self.raiz
        while nodo_actual is not None:
            if nodo_actual.id == id_producto:
                # Se elimina el nodo actual
                if nodo_actual.izquierdo is None and nodo_actual.derecho is None:
                    if nodo_padre is None:
                        self.raiz = None
                    elif nodo_padre.izquierdo == nodo_actual:
                        nodo_padre.izquierdo = None
                    else:
                        nodo_padre.derecho = None
                elif nodo_actual.izquierdo is None:
                    nodo_actual = nodo_actual.derecho
                elif nodo_actual.derecho is None:
                    nodo_actual = nodo_actual.izquierdo
                else:
                    # Se encuentra el sucesor inorden del nodo a eliminar
                    nodo_sucesor = nodo_actual.derecho
                    nodo_padre_sucesor = nodo_actual
                    while nodo_sucesor.izquierdo is not None:
                        nodo_padre_sucesor = nodo_sucesor
                        nodo_sucesor = nodo_sucesor.izquierdo

                    # Se reemplaza el nodo actual por su sucesor inorden
                    nodo_actual.id = nodo_sucesor.id
                    nodo_actual.nombre = nodo_sucesor.nombre
                    nodo_actual.precio = nodo_sucesor.precio
                    nodo_actual.cantidad = nodo_sucesor.cantidad

                    if nodo_padre_sucesor == nodo_actual:
                        nodo_padre_sucesor.derecho = nodo_sucesor.derecho
                    else:
                        nodo_padre_sucesor.izquierdo = nodo_sucesor.izquierdo
                break
            elif id_producto < nodo_actual.id:
                nodo_padre = nodo_actual
                nodo_actual = nodo_actual.izquierdo
            else:
                nodo_padre = nodo_actual
                nodo_actual = nodo_actual.derecho

    def recorrer_inorden(self, nodo):
        if nodo is not None:
            self.recorrer_inorden(nodo.izquierdo)
            print(f"Producto: {nodo.nombre} (ID: {nodo.id}, Precio: {nodo.precio}, Cantidad: {nodo.cantidad})")
            self.recorrer_inorden(nodo.derecho)

    def recorrer_preorden(self, nodo):
        if nodo is not None:
            print(f"Producto: {nodo.nombre} (ID: {nodo.id}, Precio: {nodo.precio}, Cantidad: {nodo.cantidad})")
            self.recorrer_preorden(nodo.izquierdo)
            self.recorrer_preorden(nodo.derecho)