"""
controlador/ctr_marca.py
=========================
El CONTROLADOR: es el "intermediario". Solo se encarga de GUARDAR y LEER las
marcas en el archivo. No muestra menus ni pide datos (de eso se encarga la
Vista) y no define que es una marca (de eso se encarga el Modelo).

Cada marca se guarda como una fila de texto separada por comas:
    id,nombre
Ejemplo:  1,Nike
"""

import os

from config.conexion import conectar
from modelo.mdl_marca import Marca

class Controlador:

    def listar(self):
        """
        Obtiene todas las marcas desde PostgreSQL.
        """
        marcas = []
        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT id, nombre
                    FROM marca
                    ORDER BY id ASC
                """)

                filas = cursor.fetchall()

                for fila in filas:
                    id, nombre = fila
                    marcas.append(Marca(nombre, id))

                cursor.close()

            finally:
                conexion.close()

        return marcas

    def agregar(self, nombre):
        """
        Agrega una nueva marca en PostgreSQL.
        """
        marcas = self.listar()

        nuevo_id = Marca.siguiente_id(marcas)

        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    INSERT INTO marca (id, nombre)
                    VALUES (%s, %s)
                """, (nuevo_id, nombre))

                conexion.commit()

                cursor.close()

                print("Marca agregada correctamente.")

            except Exception:
                conexion.rollback()
                raise

            finally:
                conexion.close()

    def editar(self, id, nombre):
        """
        Modifica el nombre de una marca existente.
        """
        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    UPDATE marca
                    SET nombre = %s
                    WHERE id = %s
                """, (nombre, id))

                if cursor.rowcount == 0:
                    raise ValueError(
                        f"No existe una marca con id {id}"
                    )

                conexion.commit()

                cursor.close()

                print("Marca modificada correctamente.")

            except Exception:
                conexion.rollback()
                raise

            finally:
                conexion.close()

    def eliminar(self, id):
        """
        Elimina una marca por su ID.
        """
        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    DELETE FROM marca
                    WHERE id = %s
                """, (id,))

                if cursor.rowcount == 0:
                    raise ValueError(
                        f"No existe una marca con id {id}"
                    )

                conexion.commit()

                cursor.close()

                print("Marca eliminada correctamente.")

            except Exception:
                conexion.rollback()
                raise

            finally:
                conexion.close()