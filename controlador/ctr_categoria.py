"""
controlador/ctr_categoria.py
=============================
El CONTROLADOR: es el "intermediario". Solo se encarga de GUARDAR y LEER las
categorias en el archivo. No muestra menus ni pide datos (de eso se encarga
la Vista) y no define que es una categoria (de eso se encarga el Modelo).

Cada categoria se guarda como una fila de texto separada por comas:
    id,nombre
Ejemplo:  1,Calzado
"""
import os

from config.conexion import conectar
from modelo.mdl_categoria import Categoria

class Controlador:

    def listar(self):
        """
        Obtiene todas las categorias desde PostgreSQL.
        """
        categorias = []

        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT id, nombre
                    FROM categoria
                    ORDER BY id;
                """)

                registros = cursor.fetchall()

                for id, nombre in registros:
                    categorias.append(Categoria(nombre, id))

                cursor.close()

            except Exception as ex:
                print(f"Error al listar categorias: {ex}")

            finally:
                conexion.close()

        return categorias

    def agregar(self, nombre):
        """
        Agrega una nueva categoria en PostgreSQL.
        """

        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                # Obtener el siguiente ID
                cursor.execute("""
                    SELECT COALESCE(MAX(id), 0) + 1
                    FROM categoria;
                """)

                nuevo_id = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO categoria (id, nombre)
                    VALUES (%s, %s);
                """, (nuevo_id, nombre))

                conexion.commit()

                cursor.close()

                print("Categoria agregada correctamente.")

            except Exception as ex:
                conexion.rollback()
                print(f"Error al agregar categoria: {ex}")

            finally:
                conexion.close()

    def editar(self, id, nombre):
        """
        Modifica el nombre de una categoria existente.
        """

        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    UPDATE categoria
                    SET nombre = %s
                    WHERE id = %s;
                """, (nombre, id))

                if cursor.rowcount == 0:
                    raise ValueError(
                        f"No existe una categoria con id {id}"
                    )

                conexion.commit()

                cursor.close()

                print("Categoria modificada correctamente.")

            except Exception as ex:
                conexion.rollback()
                print(f"Error al editar categoria: {ex}")

            finally:
                conexion.close()

    def eliminar(self, id):
        """
        Elimina una categoria existente.
        """

        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    DELETE FROM categoria
                    WHERE id = %s;
                """, (id,))

                if cursor.rowcount == 0:
                    raise ValueError(
                        f"No existe una categoria con id {id}"
                    )

                conexion.commit()

                cursor.close()

                print("Categoria eliminada correctamente.")

            except Exception as ex:
                conexion.rollback()
                print(f"Error al eliminar categoria: {ex}")

            finally:
                conexion.close()