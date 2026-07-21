import os
import mysql.connector

def get_db_connection():
    """
    Crea y retorna una nueva conexión a la base de datos MySQL 
    utilizando las variables de entorno configuradas en el archivo .env.
    """
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        database=os.getenv("DB_NAME")
    )
    return connection