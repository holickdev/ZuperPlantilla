import mysql.connector
import bcrypt
from app.database import get_db_connection

def verify_credentials(email, password):
    """
    Verifica las credenciales del usuario recibiendo el email y la contraseña plana.
    Retorna el diccionario del usuario sin la contraseña si es correcto, o None si es incorrecto.
    """
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True, buffered=True)
    
    sql = "SELECT id, email, password FROM users WHERE email = %s"
    
    try:
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
        
        if user:
            # bcrypt requiere trabajar con cadenas codificadas en bytes (utf-8)
            password_bytes = password.encode('utf-8')
            hashed_password_bytes = user['password'].encode('utf-8')
            
            # Compara la contraseña ingresada con el hash almacenado en la base de datos
            if bcrypt.checkpw(password_bytes, hashed_password_bytes):
                # Buena práctica de seguridad: Eliminar la contraseña del diccionario devuelto
                del user['password']
                return user
                
        return None
        
    finally:
        cursor.close()
        conexion.close()


def register_user(email, password):
    """
    Registra un nuevo usuario en la base de datos hasheando su contraseña.
    Retorna True si el registro fue exitoso o False si el correo ya existe.
    """
    conexion = get_db_connection()
    cursor = conexion.cursor()
    
    sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
    
    # Genera un hash seguro para la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        cursor.execute(sql, (email, hashed_password))
        conexion.commit()
        return True
        
    except mysql.connector.IntegrityError:
        # Ocurre cuando se viola la restricción UNIQUE del correo electrónico
        return False
        
    finally:
        cursor.close()
        conexion.close()
