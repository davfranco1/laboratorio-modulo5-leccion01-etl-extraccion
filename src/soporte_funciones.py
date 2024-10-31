# Librerías para gestión de tiempos
from time import sleep
from tqdm import tqdm

# Librerías para tratamiento de datos

import pandas as pd
import numpy as np

# Librerías para captura de datos
import requests

# Librería para trabajar con bases de datos SQL
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors

# Librería para manejar archivos .env, para cargar tokens y claves
import os
import dotenv
dotenv.load_dotenv()

# Librería para ignorar avisos
import warnings
warnings.filterwarnings("ignore") # Ignora TODOS los avisos


# Importamos el usuario y contraseña que hemos guardado en el archivo .env, de modo que podamos utilizarlos como inputs de nuestra función.
dbeaver_pw = os.getenv("dbeaver_pw")
dbeaver_user = os.getenv("dbeaver_user")


def dbeaver_conexion(database):
    """
    Establece una conexión a una base de datos DBeaver.

    Args:
        database (str): El nombre de la base de datos.

    Returns:
        connection: Un objeto de conexión a la base de datos.
    """
    try:
        conexion = psycopg2.connect(
            database=database,
            user=dbeaver_user,
            password=dbeaver_pw,
            host="localhost",
            port="5432"
        )
    except OperationalError as e:
        if e.pgcode == errorcodes.INVALID_PASSWORD:
            print("Contraseña es errónea")
        elif e.pgcode == errorcodes.CONNECTION_EXCEPTION:
            print("Error de conexión")
        else:
            print(f"Ocurrió el error {e}")

    return conexion


def crear_db(database_name):
    """
    Creates a PostgreSQL database if it does not already exist.

    Parameters:
    -----------
    database_name : str
        The name of the database to be created.

    This function connects to the PostgreSQL server using user credentials, checks if a database 
    with the given name exists, and creates it if it does not. If a connection error occurs, 
    the function will print the specific error type, such as an incorrect password or connection 
    issue. 

    Dependencies:
    -------------
    Requires psycopg2 package and the following global variables:
    - dbeaver_user: str - The username to connect to PostgreSQL.
    - dbeaver_pw: str - The password associated with the username.

    Returns:
    --------
    None
    """
    try:
        conexion = psycopg2.connect(
            user=dbeaver_user,
            password=dbeaver_pw,
            host="localhost",
            port="5432"
        )

        # Create a cursor with the new connection
        cursor = conexion.cursor()
        
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
        
        # Store the result of fetchone; if exists, it will have a row, else None
        bbdd_existe = cursor.fetchone()
        
        # If bbdd_existe is None, create the database
        if not bbdd_existe:
            cursor.execute(f"CREATE DATABASE {database_name};")
            print(f"Base de datos {database_name} creada con éxito")
        else:
            print("La base de datos ya existe")
            
        # Close the cursor and connection
        cursor.close()
        conexion.close()

    except OperationalError as e:
        if e.pgcode == errorcodes.INVALID_PASSWORD:
            print("Contraseña es errónea")
        elif e.pgcode == errorcodes.CONNECTION_EXCEPTION:
            print("Error de conexión")
        else:
            print(f"Ocurrió el error {e}")


def dbeaver_fetch(conexion, query):
    """
    Ejecuta una consulta y obtiene los resultados en un dataframe.

    Args:
        conexion (connection): Un objeto de conexión a la base de datos.
        query (str): La consulta SQL a ejecutar.

    Returns:
        list: Los resultados de la consulta en un dataframe.
    """
    cursor = conexion.cursor()
    cursor.execute(query)
    # resultado_query = cursor.fetchall()
    # Si quisiéramos que el resultado fuera en forma de lista podríamos utilizar esta línea de código.
    # En este caso, sin embargo, nos interesa obtener directamente DFs.
    
    df = pd.DataFrame(cursor.fetchall())
    df.columns = [col[0] for col in cursor.description]

    cursor.close()
    conexion.close()

    return df


def dbeaver_commit(conexion, query, *values):
    """
    Ejecuta una consulta y realiza un commit de los cambios.

    Args:
        conexion (connection): Un objeto de conexión a la base de datos.
        query (str): La consulta SQL a ejecutar.
        *values: Los valores a incluir en la consulta.

    Returns:
        str: Un mensaje de confirmación después del commit.
    """
    cursor = conexion.cursor()
    cursor.execute(query, *values)
    conexion.commit()
    cursor.close()
    conexion.close()
    return print("Commit realizado")


def dbeaver_commitmany(conexion, query, *values):
    """
    Ejecuta múltiples consultas y realiza un commit de los cambios.

    Args:
        conexion (connection): Un objeto de conexión a la base de datos.
        query (str): La consulta SQL a ejecutar.
        *values: Los valores a incluir en la consulta.

    Returns:
        str: Un mensaje de confirmación después del commit.
    """
    cursor = conexion.cursor()
    cursor.executemany(query, *values)
    conexion.commit()
    cursor.close()
    conexion.close()
    return print("Commit realizado")


def identificar_outliers(df, columna):
    """
    Identifica outliers en una columna de un DataFrame utilizando el método IQR.
    
    Parámetros:
    df (DataFrame): El DataFrame que contiene la columna a evaluar.
    columna (str): El nombre de la columna a evaluar.

    Retorna:
    DataFrame: Un DataFrame que contiene solo los outliers.
    """
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df[columna] < lower_bound) | (df[columna] > upper_bound)]
    return outliers
