

import psycopg2


def conectar():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="tecnored",
            user="postgres",
            port="5432"
        )

        print("Conexión exitosa a PostgreSQL")

        return conexion

    except Exception as ex:
        print(f"Error de conexión: {ex}")
        return None