from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QMessageBox, QGroupBox)
from PySide6.QtCore import Qt
from db_connection import DatabaseConnection
import hashlib
import sqlite3

class ChangePasswordDialog(QDialog):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.username = username
        self.setWindowTitle("Cambiar clave")
        self.setMinimumWidth(400)
        
        # Conectar a la base de datos usando la conexión global
        self.connection = DatabaseConnection.get_connection()
        self.cursor = self.connection.cursor()
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Grupo de datos del usuario
        user_group = QGroupBox("Datos del usuario")
        user_layout = QVBoxLayout()
        
        # Login de usuario (no editable)
        login_layout = QHBoxLayout()
        login_label = QLabel("Login de usuario:")
        login_value = QLabel(username)
        login_value.setStyleSheet("font-weight: bold;")
        login_layout.addWidget(login_label)
        login_layout.addWidget(login_value)
        login_layout.addStretch()
        user_layout.addLayout(login_layout)
        
        # Clave anterior
        old_pass_layout = QHBoxLayout()
        old_pass_label = QLabel("Clave anterior:")
        self.old_pass_edit = QLineEdit()
        self.old_pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        old_pass_layout.addWidget(old_pass_label)
        old_pass_layout.addWidget(self.old_pass_edit)
        user_layout.addLayout(old_pass_layout)
        
        # Nueva clave
        new_pass_layout = QHBoxLayout()
        new_pass_label = QLabel("Nueva clave:")
        self.new_pass_edit = QLineEdit()
        self.new_pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        new_pass_layout.addWidget(new_pass_label)
        new_pass_layout.addWidget(self.new_pass_edit)
        user_layout.addLayout(new_pass_layout)
        
        # Confirmar clave
        confirm_pass_layout = QHBoxLayout()
        confirm_pass_label = QLabel("Confirmar clave:")
        self.confirm_pass_edit = QLineEdit()
        self.confirm_pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        confirm_pass_layout.addWidget(confirm_pass_label)
        confirm_pass_layout.addWidget(self.confirm_pass_edit)
        user_layout.addLayout(confirm_pass_layout)
        
        user_group.setLayout(user_layout)
        layout.addWidget(user_group)
        
        # Botones
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        accept_button = QPushButton("Aceptar")
        accept_button.clicked.connect(self.accept_change)
        
        cancel_button = QPushButton("Cerrar")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(accept_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        # Estilo
        self.setStyleSheet("""
            QDialog {
                background-color: #F0F0F0;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                padding: 5px 15px;
                background-color: #E6E6E6;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #D6D6D6;
            }
            QLabel {
                color: #333333;
            }
        """)
    
    def encrypt_password(self, password):
        """Encripta la contraseña usando MD5"""
        return hashlib.md5(password.encode()).hexdigest()
    
    def accept_change(self):
        old_password = self.old_pass_edit.text()
        new_password = self.new_pass_edit.text()
        confirm_password = self.confirm_pass_edit.text()
        
        # Validar campos vacíos
        if not old_password or not new_password or not confirm_password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return
        
        # Validar que las contraseñas nuevas coincidan
        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Las contraseñas nuevas no coinciden")
            return
        
        # Verificar contraseña actual
        self.cursor.execute("""
            SELECT password
            FROM users 
            WHERE name = ?
        """, (self.username,))
        current_user = self.cursor.fetchone()
        
        if not current_user:
            QMessageBox.warning(self, "Error", "Usuario no encontrado")
            return
            
        current_password = current_user[0]
        
        # Verificar la contraseña actual
        if current_password != old_password:
            # Intentar verificar con MD5
            if current_password != self.encrypt_password(old_password):
                QMessageBox.warning(self, "Error", "La contraseña actual es incorrecta")
                return
        
        try:
            # Actualizar contraseña usando MD5
            encrypted_new_pass = self.encrypt_password(new_password)
            self.cursor.execute("""
                UPDATE users 
                SET password = ?
                WHERE name = ?
            """, (encrypted_new_pass, self.username))
            
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Contraseña actualizada correctamente")
            self.accept()
            
        except sqlite3.Error as e:
            self.connection.rollback()
            QMessageBox.critical(self, "Error", f"Error al actualizar la contraseña: {str(e)}")
    
    def closeEvent(self, event):
        # No cerramos la conexión ya que es compartida
        event.accept()
