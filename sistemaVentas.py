import sqlite3
import datetime

from ArbolBinario import ArbolBinario
from pila import Pila


class SistemaVentas:
    def __conn(self):
        # Conexión a la base de datos SQLite
        self.conn = sqlite3.connect("ConfiguracionBaseDatos/BaseDatos.db")
        self.cursor = self.conn.cursor()

        # Creación de la tabla productos (si no existe)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            precio REAL,
            cantidad INTEGER
        )""")

        # Creación de la tabla ventas (si no existe)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER,
            cantidad INTEGER,
            fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")

    def __init__(self):
        self.__conn()
        self.arbol_productos = ArbolBinario()
        self.pila_historial = Pila()

    def agregar_producto(self, producto):
        # Se agrega el producto al árbol binario
        self.arbol_productos.insertar(producto)

        self.cursor.execute("INSERT INTO productos (id_producto, cantidad) VALUES (?, ?, ?)",
                            (producto["nombre"], producto["precio"], producto["cantidad"]))
        self.conn.commit()

        print("Producto agregado exitosamente.")

    def buscar_producto(self, id_producto):
        producto = self.arbol_productos.buscar(id_producto)
        if producto is not None:
            print(f"Producto encontrado: {producto.nombre} (ID: {producto.id}, Precio: {producto.precio}, Cantidad: {producto.cantidad})")
        else:
            print("Producto no encontrado.")

    def eliminar_producto(self, id_producto):
        producto_eliminado = self.arbol_productos.eliminar(id_producto)
        if producto_eliminado is not None:
            self.cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
            self.conn.commit()
            print("Producto eliminado exitosamente.")
        else:
            print("Producto no encontrado.")

    def recorrer_productos_inorden(self):
        print("Recorrido inorden:")
        self.arbol_productos.recorrer_inorden(self.arbol_productos.raiz)

    def recorrer_productos_preorden(self):
        print("Recorrido preorden:")
        self.arbol_productos.recorrer_preorden(self.arbol_productos.raiz)

    def realizar_venta(self, id_producto, cantidad_venta):
        producto = self.arbol_productos.buscar(id_producto)
        if producto is not None:
            if producto.cantidad >= cantidad_venta:
                # Se actualiza la cantidad del producto en el árbol
                producto.cantidad -= cantidad_venta

                # Se guarda la venta en la pila de historial
                venta = {"id_producto": producto.id, "cantidad": cantidad_venta,
                         "fecha_hora": self._obtener_fecha_hora_actual()}
                self.pila_historial.apilar(venta)

                # Se guarda la venta en la base de datos (con fecha y hora)
                self.cursor.execute("INSERT INTO productos (id_producto, cantidad, fecha_hora) VALUES (?, ?, ?)",
                                    (producto.id, cantidad_venta, venta["fecha_hora"]))
                self.conn.commit()

                print(
                    f"Venta realizada: {cantidad_venta} unidades de {producto.nombre} (fecha y hora: {venta['fecha_hora']})")
            else:
                print(
                    f"Venta no realizada: No hay suficientes unidades del producto {producto.nombre} (stock disponible: {producto.cantidad}).")

    def _obtener_fecha_hora_actual(self):
        fecha_hora_actual = datetime.datetime.now()
        fecha_hora_formateada = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")
        return fecha_hora_formateada


    def historial_ventas(self):
        print("Historial de ventas:")
        self.cursor.execute(
            "SELECT v.id_producto, v.cantidad, v.fecha_hora FROM productos v JOIN productos p ON v.id_producto = p.id_producto ORDER BY v.fecha_hora DESC")
        for venta in self.cursor.fetchall():
            id_producto, nombre_producto, cantidad_venta, fecha_hora = venta
            print(f"Venta: {cantidad_venta} unidades de {nombre_producto} (fecha y hora: {fecha_hora})")