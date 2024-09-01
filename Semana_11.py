# Semana 11
# Tarea: Sistema Avanzado de Gestión de Inventario

import json
import os

class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        # Inicializa los atributos del producto
        self.id_producto = id_producto  # ID único del producto
        self.nombre = nombre  # Nombre del producto
        self.cantidad = cantidad  # Cantidad en inventario
        self.precio = precio  # Precio del producto

    def __str__(self):
        # Devuelve una representación en texto del producto
        return f"ID: {self.id_producto}, Nombre: {self.nombre}, Cantidad: {self.cantidad}, Precio: ${self.precio}"


class Inventario:
    def __init__(self, archivo='inventario.json'):
        # Inicializa el inventario como un diccionario y el archivo JSON para almacenamiento
        self.productos = {}  # Diccionario para almacenar productos
        self.archivo = archivo  # Archivo donde se guarda el inventario
        self.cargar_inventario()  # Carga los productos desde el archivo

    def cargar_inventario(self):
        # Carga los productos desde un archivo JSON
        try:
            if os.path.exists(self.archivo):
                with open(self.archivo, 'r') as f:
                    self.productos = json.load(f)
                print("Inventario cargado desde archivo con éxito.")
            else:
                print(f"Archivo '{self.archivo}' no encontrado. Se creará uno nuevo al guardar.")
        except FileNotFoundError:
            print("Error: Archivo de inventario no encontrado.")
        except json.JSONDecodeError:
            print("Error: Problema al leer el archivo de inventario. Verifique el formato JSON.")

    def guardar_inventario(self):
        # Guarda los productos en un archivo JSON
        try:
            with open(self.archivo, 'w') as f:
                json.dump(self.productos, f, indent=4)
            print("Inventario guardado en archivo con éxito.")
        except Exception as e:
            print(f"Error al guardar el inventario: {e}")

    def agregar_producto(self, producto):
        # Añade un nuevo producto al inventario
        if producto.id_producto in self.productos:
            print("Error: Ya existe un producto con ese ID.")
        else:
            self.productos[producto.id_producto] = producto.__dict__
            print("Producto añadido con éxito.")
            self.guardar_inventario()  # Guarda el inventario después de añadir el producto

    def eliminar_producto(self, id_producto):
        # Elimina un producto del inventario por su ID
        if id_producto in self.productos:
            del self.productos[id_producto]
            print(f"Producto {id_producto} eliminado con éxito.")
            self.guardar_inventario()  # Guarda el inventario después de eliminar el producto
        else:
            print("Error: Producto no encontrado.")

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        # Actualiza la cantidad o el precio de un producto por su ID
        if id_producto in self.productos:
            if cantidad is not None:
                self.productos[id_producto]['cantidad'] = cantidad
            if precio is not None:
                self.productos[id_producto]['precio'] = precio
            print(f"Producto {id_producto} actualizado con éxito.")
            self.guardar_inventario()  # Guarda el inventario después de actualizar el producto
        else:
            print("Error: Producto no encontrado.")

    def buscar_producto(self, nombre):
        # Busca productos por nombre
        resultados = [Producto(id_producto, p['nombre'], p['cantidad'], p['precio'])
                      for id_producto, p in self.productos.items()
                      if nombre.lower() in p['nombre'].lower()]
        if resultados:
            for producto in resultados:
                print(producto)
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_inventario(self):
        # Muestra todos los productos en el inventario
        if self.productos:
            for id_producto, info in self.productos.items():
                producto = Producto(id_producto, info['nombre'], info['cantidad'], info['precio'])
                print(producto)
        else:
            print("El inventario está vacío.")


def menu() -> object:
    # Inicializa el inventario con el archivo JSON
    inventario = Inventario()

    while True:
        print("\nSistema de Gestión de Inventarios")
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar cantidad o precio de un producto")
        print("4. Buscar producto(s) por nombre")
        print("5. Mostrar todos los productos")
        print("6. Guardar y Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            id_producto = input("Ingrese el ID del producto: ")
            nombre = input("Ingrese el nombre del producto: ")
            cantidad = int(input("Ingrese la cantidad: "))
            precio = float(input("Ingrese el precio: "))
            producto = Producto(id_producto, nombre, cantidad, precio)
            inventario.agregar_producto(producto)

        elif opcion == '2':
            id_producto = input("Ingrese el ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)

        elif opcion == '3':
            id_producto = input("Ingrese el ID del producto a actualizar: ")
            cantidad = input("Ingrese la nueva cantidad (o presione Enter para no cambiarla): ")
            precio = input("Ingrese el nuevo precio (o presione Enter para no cambiarlo): ")
            cantidad = int(cantidad) if cantidad else None
            precio = float(precio) if precio else None
            inventario.actualizar_producto(id_producto, cantidad, precio)

        elif opcion == '4':
            nombre = input("Ingrese el nombre del producto a buscar: ")
            inventario.buscar_producto(nombre)

        elif opcion == '5':
            inventario.mostrar_inventario()

        elif opcion == '6':
            inventario.guardar_inventario()
            print("Inventario guardado. Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")


# Ejecución del menú si se ejecuta como script principal
if __name__ == "__main__":
    menu()


# Universidad Estatal Amazónica
# Andrés Ponce M.