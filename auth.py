import sqlite3
from PySide6.QtWidgets import QMessageBox
from db_connection import DatabaseConnection
import hashlib

class Auth:
    @staticmethod
    def encrypt_password(password):
        """Encripta la contraseña usando MD5"""
        return hashlib.md5(password.encode()).hexdigest()

    @staticmethod
    def verify_credentials(username, password, db_path):
        try:
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT password, enabled 
                FROM users 
                WHERE name = ?
            """, (username,))
            
            user = cursor.fetchone()
            
            if user:
                stored_password, enabled = user
                
                if not enabled:
                    return False, "Usuario deshabilitado"
                
                # Verificar tanto la contraseña plana como la encriptada
                if stored_password == password or stored_password == Auth.encrypt_password(password):
                    return True, "Login exitoso"
                    
            return False, "Usuario o contraseña incorrectos"
            
        except sqlite3.Error as e:
            return False, f"Error de base de datos: {str(e)}"
    
    @staticmethod
    def get_stored_password(username):
        """Obtiene la contraseña almacenada para un usuario"""
        try:
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor()
            
            cursor.execute("SELECT password FROM users WHERE name = ?", (username,))
            result = cursor.fetchone()
            
            return result[0] if result else None
            
        except sqlite3.Error:
            return None

    @staticmethod
    def show_error(parent, message):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error de Autenticación")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #E6E7E8;
            }
            QPushButton {
                padding: 5px 15px;
                border: 1px solid #CCCCCC;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF, stop:1 #E6E6E6);
                min-width: 80px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E6E6E6, stop:1 #FFFFFF);
            }
        """)
        msg.exec_()
