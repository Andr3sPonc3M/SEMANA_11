# Semana 11
# Tarea: Sistema Avanzado de Gestión de Inventario

import os
import json  # Módulo para manejo de archivos JSON

class Producto:
    """
    Clase que representa un producto en el inventario.
    """

    def __init__(self, id_producto, nombre, cantidad, precio):
        """
        Inicializa un nuevo producto con los atributos proporcionados.
        """
        self._id_producto = id_producto  # ID único del producto
        self._nombre = nombre            # Nombre del producto
        self._cantidad = cantidad        # Cantidad en inventario
        self._precio = precio            # Precio del producto

    # Métodos getter para los atributos
    def get_id_producto(self):
        return self._id_producto

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    # Métodos setter para los atributos
    def set_nombre(self, nombre):
        self._nombre = nombre

    def set_cantidad(self, cantidad):
        self._cantidad = cantidad

    def set_precio(self, precio):
        self._precio = precio

    def mostrar_info(self):
        """
        Retorna una cadena con la información del producto.
        """
        return f"ID: {self._id_producto}, Nombre: {self._nombre}, Cantidad: {self._cantidad}, Precio: ${self._precio:.2f}"

    def a_dict(self):
        """
        Convierte el producto a un diccionario para serialización.
        """
        return {
            'id_producto': self._id_producto,
            'nombre': self._nombre,
            'cantidad': self._cantidad,
            'precio': self._precio
        }

    @staticmethod
    def desde_dict(datos):
        """
        Crea una instancia de Producto desde un diccionario.
        """
        return Producto(
            id_producto=datos['id_producto'],
            nombre=datos['nombre'],
            cantidad=datos['cantidad'],
            precio=datos['precio']
        )

class Inventario:
    """
    Clase que gestiona el inventario de productos.
    """

    def __init__(self, archivo):
        """
        Inicializa el inventario cargando los productos desde un archivo JSON.
        """
        self.productos = {}  # Diccionario para almacenar productos por ID
        self.archivo = archivo  # Nombre del archivo de almacenamiento
        self.cargar_desde_archivo()  # Carga los datos iniciales

    def cargar_desde_archivo(self):
        """
        Carga los productos desde un archivo JSON.
        """
        try:
            if os.path.exists(self.archivo):
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)  # Carga los datos JSON
                    for item in datos:
                        producto = Producto.desde_dict(item)  # Crea instancia de Producto
                        self.productos[producto.get_id_producto()] = producto  # Añade al diccionario
                print("Inventario cargado desde archivo con éxito.")
            else:
                print(f"Archivo '{self.archivo}' no encontrado, se creará uno nuevo.")
        except json.JSONDecodeError:
            print(f"Error: El archivo '{self.archivo}' está corrupto o no es válido.")
        except PermissionError:
            print(f"Error: Permiso denegado para leer el archivo '{self.archivo}'.")
        except Exception as e:
            print(f"Error inesperado al leer el archivo: {e}")

    def guardar_en_archivo(self):
        """
        Guarda los productos en un archivo JSON.
        """
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                datos = [producto.a_dict() for producto in self.productos.values()]  # Convierte a lista de diccionarios
                json.dump(datos, f, indent=4, ensure_ascii=False)  # Guarda en formato JSON
            print("Inventario guardado en archivo con éxito.")
        except PermissionError:
            print(f"Error: Permiso denegado para escribir en el archivo '{self.archivo}'.")
        except Exception as e:
            print(f"Error inesperado al escribir en el archivo: {e}")

    def añadir_producto(self, producto):
        """
        Añade un nuevo producto al inventario si el ID es único.
        """
        if producto.get_id_producto() in self.productos:
            print("Error: Ya existe un producto con ese ID.")
            return
        self.productos[producto.get_id_producto()] = producto  # Añade al diccionario
        self.guardar_en_archivo()  # Guarda cambios
        print("Producto añadido con éxito.")

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto del inventario por su ID.
        """
        if id_producto in self.productos:
            del self.productos[id_producto]  # Elimina del diccionario
            self.guardar_en_archivo()  # Guarda cambios
            print("Producto eliminado con éxito.")
        else:
            print("Error: Producto no encontrado.")

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        """
        Actualiza la cantidad y/o el precio de un producto por su ID.
        """
        if id_producto in self.productos:
            producto = self.productos[id_producto]  # Obtiene el producto
            if cantidad is not None:
                producto.set_cantidad(cantidad)  # Actualiza cantidad
            if precio is not None:
                producto.set_precio(precio)  # Actualiza precio
            self.guardar_en_archivo()  # Guarda cambios
            print("Producto actualizado con éxito.")
        else:
            print("Error: Producto no encontrado.")

    def buscar_producto(self, nombre):
        """
        Busca y muestra productos cuyo nombre contiene la cadena proporcionada.
        """
        resultados = [p for p in self.productos.values() if nombre.lower() in p.get_nombre().lower()]
        if resultados:
            print(f"Se encontraron {len(resultados)} producto(s):")
            for producto in resultados:
                print(producto.mostrar_info())
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_todos(self):
        """
        Muestra todos los productos en el inventario.
        """
        if self.productos:
            print(f"Inventario contiene {len(self.productos)} producto(s):")
            for producto in self.productos.values():
                print(producto.mostrar_info())
        else:
            print("El inventario está vacío.")

def menu():
    """
    Función que muestra el menú de opciones y maneja la interacción con el usuario.
    """
    inventario = Inventario("inventario.json")  # Inicializa el inventario con archivo JSON

    while True:
        # Muestra el menú de opciones
        print("\nSistema Avanzado de Gestión de Inventarios")
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar cantidad o precio de un producto")
        print("4. Buscar producto(s) por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ").strip()  # Obtiene la opción del usuario

        if opcion == '1':
            # Añadir nuevo producto
            id_producto = input("Ingrese el ID del producto: ").strip()
            if not id_producto:
                print("Error: El ID no puede estar vacío.")
                continue
            nombre = input("Ingrese el nombre del producto: ").strip()
            if not nombre:
                print("Error: El nombre no puede estar vacío.")
                continue
            try:
                cantidad = int(input("Ingrese la cantidad: ").strip())
                if cantidad < 0:
                    print("Error: La cantidad no puede ser negativa.")
                    continue
            except ValueError:
                print("Error: La cantidad debe ser un número entero.")
                continue
            try:
                precio = float(input("Ingrese el precio: ").strip())
                if precio < 0:
                    print("Error: El precio no puede ser negativo.")
                    continue
            except ValueError:
                print("Error: El precio debe ser un número.")
                continue
            producto = Producto(id_producto, nombre, cantidad, precio)  # Crea instancia de Producto
            inventario.añadir_producto(producto)  # Añade al inventario

        elif opcion == '2':
            # Eliminar producto por ID
            id_producto = input("Ingrese el ID del producto a eliminar: ").strip()
            if not id_producto:
                print("Error: El ID no puede estar vacío.")
                continue
            inventario.eliminar_producto(id_producto)  # Elimina del inventario

        elif opcion == '3':
            # Actualizar cantidad o precio de un producto
            id_producto = input("Ingrese el ID del producto a actualizar: ").strip()
            if not id_producto:
                print("Error: El ID no puede estar vacío.")
                continue
            cantidad_input = input("Ingrese la nueva cantidad (o presione Enter para no cambiarla): ").strip()
            precio_input = input("Ingrese el nuevo precio (o presione Enter para no cambiarlo): ").strip()

            cantidad = None
            precio = None

            if cantidad_input:
                try:
                    cantidad = int(cantidad_input)
                    if cantidad < 0:
                        print("Error: La cantidad no puede ser negativa.")
                        continue
                except ValueError:
                    print("Error: La cantidad debe ser un número entero.")
                    continue

            if precio_input:
                try:
                    precio = float(precio_input)
                    if precio < 0:
                        print("Error: El precio no puede ser negativo.")
                        continue
                except ValueError:
                    print("Error: El precio debe ser un número.")
                    continue

            if cantidad is None and precio is None:
                print("No se realizaron cambios.")
                continue

            inventario.actualizar_producto(id_producto, cantidad, precio)  # Actualiza en el inventario

        elif opcion == '4':
            # Buscar producto(s) por nombre
            nombre = input("Ingrese el nombre del producto a buscar: ").strip()
            if not nombre:
                print("Error: El nombre no puede estar vacío.")
                continue
            inventario.buscar_producto(nombre)  # Busca en el inventario

        elif opcion == '5':
            # Mostrar todos los productos
            inventario.mostrar_todos()  # Muestra todos los productos

        elif opcion == '6':
            # Salir del sistema
            print("Saliendo del sistema...")
            break  # Sale del ciclo

        else:
            # Opción inválida
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()  # Ejecuta el menú si se ejecuta como script principal


# Universidad Estatal Amazónica
# Andrés Ponce M.