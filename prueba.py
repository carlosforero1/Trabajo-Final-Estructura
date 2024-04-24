from sistemaVentas import SistemaVentas

if __name__ == "__main__":
    BaseDatos = SistemaVentas()

    # Menú principal
    while True:
        print("\nMenú principal:")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Eliminar producto")
        print("4. Recorrer productos (inorden)")
        print("5. Recorrer productos (preorden)")
        print("6. Realizar venta")
        print("7. Ver historial de ventas")
        print("8. Salir")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            nombre = input("Nombre del producto: ")
            id_producto = int(input("ID del producto: "))
            precio = float(input("Precio del producto: "))
            cantidad = int(input("Cantidad inicial del producto: "))
            producto = {"nombre": nombre, "id": id_producto, "precio": precio, "cantidad": cantidad}
            BaseDatos.agregar_producto(producto)
        elif opcion == "2":
            id_producto = int(input("ID del producto a buscar: "))
            BaseDatos.buscar_producto(id_producto)
        elif opcion == "3":
            id_producto = int(input("ID del producto a eliminar: "))
            BaseDatos.eliminar_producto(id_producto)
        elif opcion == "4":
            BaseDatos.recorrer_productos_inorden()
        elif opcion == "5":
            BaseDatos.recorrer_productos_preorden()
        elif opcion == "6":
            id_producto = int(input("ID del producto a vender: "))
            cantidad_venta = int(input("Cantidad a vender: "))
            BaseDatos.realizar_venta(id_producto, cantidad_venta)
        elif opcion == "7":
            BaseDatos.historial_ventas()
        elif opcion == "8":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")