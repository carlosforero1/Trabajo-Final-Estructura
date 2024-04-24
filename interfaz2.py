import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Función para conectar a la base de datos
def conectar_db():
    try:
        conexion = sqlite3.connect("BaseDatos.db")
        cursor = conexion.cursor()
        return conexion, cursor
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        return None, None


def agregar_producto():
    def guardar_producto():
        nombre = entry_nombre.get().strip()
        precio = float(entry_precio.get().strip())
        cantidad = int(entry_cantidad.get().strip())

        if not nombre or not precio or not cantidad:
            messagebox.showwarning("Aviso", "Todos los campos son obligatorios.")
            return

        try:
            conexion, cursor = conectar_db()
            cursor.execute("INSERT INTO BaseDatos (nombre, precio, cantidad) VALUES (?, ?, ?)", (nombre, precio, cantidad))
            conexion.commit()
            messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
            limpiar_formulario_producto()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {e}")
        finally:
            conexion.close()

    def limpiar_formulario_producto():
        entry_nombre.delete(0, tk.END)
        entry_id_producto.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)

    ventana_producto = tk.Toplevel(ventana_principal)
    ventana_producto.title("Agregar producto")

    label_nombre = tk.Label(ventana_producto, text="Nombre:")
    label_nombre.pack(pady=5)

    entry_nombre = tk.Entry(ventana_producto)
    entry_nombre.pack(pady=5)

    label_id_producto = tk.Label(ventana_producto, text="ID producto:")
    label_id_producto.pack(pady=5)

    entry_id_producto = tk.Entry(ventana_producto)
    entry_id_producto.pack(pady=5)

    label_precio = tk.Label(ventana_producto, text="Precio:")
    label_precio.pack(pady=5)

    entry_precio = tk.Entry(ventana_producto)
    entry_precio.pack(pady=5)

    label_cantidad = tk.Label(ventana_producto, text="Cantidad:")
    label_cantidad.pack(pady=5)

    entry_cantidad = tk.Entry(ventana_producto)
    entry_cantidad.pack(pady=5)

    boton_guardar = tk.Button(ventana_producto, text="Guardar", command=guardar_producto)
    boton_guardar.pack(pady=5)

    boton_limpiar = tk.Button(ventana_producto, text="Limpiar", command=limpiar_formulario_producto)
    boton_limpiar.pack(pady=5)

# Función para buscar un producto por ID
def buscar_producto():
    def buscar_por_id():
        id_producto = int(entry_id_producto_buscar.get().strip())

        if not id_producto:
            messagebox.showwarning("Aviso", "Ingrese un ID de producto válido.")
            return

        try:
            conexion, cursor = conectar_db()
            cursor.execute("SELECT * FROM BaseDatos WHERE id = ?", (id_producto,))
            producto = cursor.fetchone()
            conexion.close()

            if producto:
                mostrar_producto_encontrado(producto)
            else:
                messagebox.showinfo("Información", "Producto no encontrado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar producto: {e}")

    def mostrar_producto_encontrado(producto):
        ventana_producto_encontrado = tk.Toplevel(ventana_principal)
        ventana_producto_encontrado.title("Producto encontrado")

        label_nombre = tk.Label(ventana_producto_encontrado, text="Nombre:")
        label_nombre.pack(pady=5)

        label_nombre_valor = tk.Label(ventana_producto_encontrado, text=producto[1])
        label_nombre_valor.pack(pady=5)

        label_precio = tk.Label(ventana_producto_encontrado, text="Precio:")
        label_precio.pack(pady=5)

        label_precio_valor = tk.Label(ventana_producto_encontrado, text=producto[2])
        label_precio_valor.pack(pady=5)

        label_cantidad = tk.Label(ventana_producto_encontrado, text="Cantidad:")
        label_cantidad.pack(pady=5)

        label_cantidad_valor = tk.Label(ventana_producto_encontrado, text=producto[3])
        label_cantidad_valor.pack(pady=5)

    # Creación de la ventana_buscar
    ventana_buscar = tk.Toplevel(ventana_principal)
    ventana_buscar.title("Buscar producto")

    label_id_producto_buscar = tk.Label(ventana_buscar, text="ID producto:")
    label_id_producto_buscar.pack(pady=5)

    entry_id_producto_buscar = tk.Entry(ventana_buscar)
    entry_id_producto_buscar.pack(pady=5)

    boton_buscar = tk.Button(ventana_buscar, text="Buscar", command=buscar_por_id)
    boton_buscar.pack(pady=5)

# Función para eliminar un producto por ID
def eliminar_producto():
    def eliminar_por_id():
        id_producto = int(entry_id_producto_eliminar.get().strip())

        if not id_producto:
            messagebox.showwarning("Aviso", "Ingrese un ID de producto válido.")
            return

        try:
            conexion, cursor = conectar_db()
            cursor.execute("DELETE FROM BaseDatos WHERE id = ?", (id_producto,))
            conexion.commit()
            messagebox.showinfo("Éxito", "Producto eliminado exitosamente.")
            limpiar_formulario_eliminar_producto(entry_id_producto_eliminar)
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {e}")

    ventana_eliminar = tk.Toplevel(ventana_principal)
    ventana_eliminar.title("Eliminar producto")

    label_id_producto_eliminar = tk.Label(ventana_eliminar, text="ID producto:")
    label_id_producto_eliminar.pack(pady=5)

    entry_id_producto_eliminar = tk.Entry(ventana_eliminar)
    entry_id_producto_eliminar.pack(pady=5)

    boton_eliminar = tk.Button(ventana_eliminar, text="Eliminar", command=eliminar_por_id)
    boton_eliminar.pack(pady=5)

    def limpiar_formulario_eliminar_producto(entry_widget):
        entry_widget.delete(0, tk.END)

    limpiar_formulario_eliminar_producto(entry_id_producto_eliminar)

def recorrer_productos(orden):
    def mostrar_productos(productos):
        ventana_recorrido = tk.Toplevel(ventana_principal)
        ventana_recorrido.title(f"Recorrido de productos ({orden})")

        lista_productos = tk.Listbox(ventana_recorrido)
        lista_productos.pack(pady=5)

        for producto in productos:
            lista_productos.insert(tk.END, f"{producto[1]} (ID: {producto[0]}, Precio: {producto[2]}, Cantidad: {producto[3]})")

    try:
        conexion, cursor = conectar_db()
        if orden == "inorden":
            cursor.execute("SELECT * FROM BaseDatos ORDER BY id")
        elif orden == "preorden":
            cursor.execute("SELECT * FROM BaseDatos ORDER BY id ASC")
        else:
            raise ValueError("Orden no válido.")

        productos = cursor.fetchall()
        conexion.close()

        mostrar_productos(productos)
    except Exception as e:
        messagebox.showerror("Error", f"Error al recorrer productos: {e}")

# Función para realizar una venta
def realizar_venta():
    producto_seleccionado = None

    def seleccionar_producto():
        nonlocal producto_seleccionado

        producto_seleccionado = None

        try:
            id_producto = int(entry_id_producto_venta.get().strip())

            conexion, cursor = conectar_db()
            cursor.execute("SELECT * FROM BaseDatos WHERE id = ?", (id_producto,))
            producto = cursor.fetchone()
            conexion.close()

            if producto:
                producto_seleccionado = producto
                label_producto_seleccionado.config(
                    text=f"Producto seleccionado: {producto[1]} (ID: {producto[0]}, Precio: {producto[2]}, Cantidad: {producto[3]})")
            else:
                messagebox.showinfo("Información", "Producto no encontrado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al seleccionar producto: {e}")

    def realizar_venta_confirmada():
        nonlocal producto_seleccionado

        if not producto_seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un producto para realizar la venta.")
            return

        cantidad_venta = int(entry_cantidad_venta.get().strip())

        if not cantidad_venta or cantidad_venta <= 0:
            messagebox.showwarning("Aviso", "Ingrese una cantidad válida a vender.")
            return

        if cantidad_venta > producto_seleccionado[3]:
            messagebox.showwarning("Aviso", "No hay suficiente cantidad de producto en stock.")
            return

        try:
            conexion, cursor = conectar_db()
            cursor.execute("UPDATE BaseDatos SET cantidad = cantidad - ? WHERE id = ?",
                           (cantidad_venta, producto_seleccionado[0]))

            fecha_hora_actual = datetime.now()
            cursor.execute("INSERT INTO productos (id_producto, cantidad, fecha_hora) VALUES (?, ?, ?)",
                           (producto_seleccionado[0], cantidad_venta, fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")))
            conexion.commit()
            messagebox.showinfo("Éxito", "Venta realizada exitosamente.")
            limpiar_formulario_venta()
        except Exception as e:
            messagebox.showerror("Error", f"Error al realizar venta: {e}")

    def limpiar_formulario_venta():
        nonlocal producto_seleccionado

        producto_seleccionado = None
        entry_id_producto_venta.delete(0, tk.END)
        entry_cantidad_venta.delete(0, tk.END)
        label_producto_seleccionado.config(text="Producto seleccionado:")

    ventana_venta = tk.Toplevel(ventana_principal)
    ventana_venta.title("Realizar venta")

    label_id_producto_venta = tk.Label(ventana_venta, text="ID producto:")
    label_id_producto_venta.pack(pady=5)

    entry_id_producto_venta = tk.Entry(ventana_venta)
    entry_id_producto_venta.pack(pady=5)

    boton_seleccionar_producto = tk.Button(ventana_venta, text="Seleccionar producto", command=seleccionar_producto)
    boton_seleccionar_producto.pack(pady=5)

    label_producto_seleccionado = tk.Label(ventana_venta, text="Producto seleccionado:")
    label_producto_seleccionado.pack(pady=5)

    label_cantidad_venta = tk.Label(ventana_venta, text="Cantidad a vender:")
    label_cantidad_venta.pack(pady=5)

    entry_cantidad_venta = tk.Entry(ventana_venta)
    entry_cantidad_venta.pack(pady=5)

    boton_realizar_venta = tk.Button(ventana_venta, text="Realizar venta", command=realizar_venta_confirmada)
    boton_realizar_venta.pack(pady=5)

# Función para mostrar el historial de ventas
def historial_ventas():
    try:
        conexion, cursor = conectar_db()
        cursor.execute("SELECT v.id_producto, p.nombre, v.cantidad, v.fecha_hora FROM productos v JOIN BaseDatos p ON v.id_producto = p.id ORDER BY v.fecha_hora DESC")
        ventas = cursor.fetchall()
        conexion.close()

        if ventas:
            ventana_historial = tk.Toplevel(ventana_principal)
            ventana_historial.title("Historial de ventas")

            lista_ventas = tk.Listbox(ventana_historial)
            lista_ventas.pack(pady=5)

            for venta in ventas:
                lista_ventas.insert(tk.END, f"{venta[1]} (ID: {venta[0]}, Cantidad: {venta[2]}, Fecha/Hora: {venta[3]})")
        else:
            messagebox.showinfo("Información", "No hay registros de ventas.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener historial de ventas: {e}")

# Función principal
def main():
    global ventana_principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Sistema de ventas")
    ventana_principal.config(bg="#F0F8FF")

    barra_menu = tk.Menu(ventana_principal)
    ventana_principal.config(menu=barra_menu)

    menu_productos = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Productos", menu=menu_productos)
    menu_productos.add_command(label="Agregar", command=agregar_producto)
    menu_productos.add_command(label="Buscar", command=buscar_producto)
    menu_productos.add_command(label="Eliminar", command=eliminar_producto)
    menu_productos.add_separator()
    menu_productos.add_command(label="Recorrer (Inorden)", command=lambda: recorrer_productos("inorden"))
    menu_productos.add_command(label="Recorrer (Preorden)", command=lambda: recorrer_productos("preorden"))

    menu_ventas = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Ventas", menu=menu_ventas)
    menu_ventas.add_command(label="Realizar venta", command=realizar_venta)
    menu_ventas.add_command(label="Historial", command=historial_ventas)

    menu_ayuda = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
    menu_ayuda.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Acerca de", "Sistema de ventas desarrollado en Python con Tkinter."))

    ventana_principal.mainloop()

if __name__ == "__main__":
    main()
