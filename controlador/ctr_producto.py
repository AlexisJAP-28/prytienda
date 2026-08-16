"""
controlador/ctr_producto.py
============================
El CONTROLADOR: es el "intermediario". Solo se encarga de GUARDAR y LEER los
productos en el archivo. No muestra menus ni pide datos (de eso se encarga
la Vista) y no define que es un producto (de eso se encarga el Modelo).

Cada producto se guarda como una fila de texto separada por comas:
    id,nombre,id_marca,id_categoria,id_linea,precio,stock
Ejemplo:  1,Zapatilla Air,1,2,1,59.99,10

Las columnas id_marca, id_categoria e id_linea son las FK: apuntan a los
ids de los catalogos de Marca, Categoria y Linea.
"""

import os

from config.conexion import conectar
from modelo.mdl_producto import Producto


class Controlador:

    def listar(self):
        productos = []

        conexion = conectar()

        if conexion is None:
            return productos

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id, nombre, id_marca, id_categoria,
                       id_linea, precio, stock
                FROM producto
                ORDER BY id ASC
            """)

            filas = cursor.fetchall()

            for fila in filas:
                id, nombre, id_marca, id_categoria, id_linea, precio, stock = fila

                producto = Producto(
                    nombre,
                    id_marca,
                    id_categoria,
                    id_linea,
                    precio,
                    stock,
                    id
                )

                productos.append(producto)

            cursor.close()
            conexion.close()

        except Exception as ex:
            print(f"Error al listar productos: {ex}")

        return productos

    def agregar(self, nombre, id_marca, id_categoria, id_linea, precio, stock):

        conexion = conectar()

        if conexion is None:
            return

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT COALESCE(MAX(id), 0) + 1
                FROM producto
            """)

            nuevo_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO producto
                (id, nombre, id_marca, id_categoria, id_linea, precio, stock)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                nuevo_id,
                nombre,
                id_marca,
                id_categoria,
                id_linea,
                precio,
                stock
            ))

            conexion.commit()

            cursor.close()
            conexion.close()

            print("Producto agregado correctamente.")

        except Exception as ex:
            conexion.rollback()
            conexion.close()
            raise ex

    def editar(self, id, nombre, id_marca, id_categoria, id_linea,
               precio, stock):

        conexion = conectar()

        if conexion is None:
            return

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE producto
                SET nombre = %s,
                    id_marca = %s,
                    id_categoria = %s,
                    id_linea = %s,
                    precio = %s,
                    stock = %s
                WHERE id = %s
            """, (
                nombre,
                id_marca,
                id_categoria,
                id_linea,
                precio,
                stock,
                id
            ))

            if cursor.rowcount == 0:
                raise ValueError(
                    f"No existe un producto con id {id}"
                )

            conexion.commit()

            cursor.close()
            conexion.close()

            print("Producto modificado correctamente.")

        except Exception as ex:
            conexion.rollback()
            conexion.close()
            raise ex

    def eliminar(self, id):

        conexion = conectar()

        if conexion is None:
            return

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                DELETE FROM producto
                WHERE id = %s
            """, (id,))

            if cursor.rowcount == 0:
                raise ValueError(
                    f"No existe un producto con id {id}"
                )

            conexion.commit()

            cursor.close()
            conexion.close()

            print("Producto eliminado correctamente.")

        except Exception as ex:
            conexion.rollback()
            conexion.close()
            raise ex