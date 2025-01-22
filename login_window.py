import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
                             QLineEdit, QCheckBox, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QFrame, QMessageBox)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt
from database_selector import DatabaseSelector
from auth import Auth
from main_window import MainWindow
import hashlib

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.setFixedSize(450, 350)
        
        # Establecer el fondo azul de la ventana principal
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0078D7;
            }
            QWidget#centralWidget {
                background-color: #E6E7E8;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #CCCCCC;
                background: white;
            }
            QCheckBox {
                color: #000000;
            }
            QPushButton {
                padding: 5px 15px;
                border: 1px solid #CCCCCC;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF, stop:1 #E6E6E6);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E6E6E6, stop:1 #FFFFFF);
            }
            QPushButton#dbButton {
                border: none;
                background: transparent;
                color: #0066CC;
                text-align: left;
                padding: 0;
            }
            QPushButton#dbButton:hover {
                color: #003399;
                text-decoration: underline;
            }
        """)
        
        # Widget central con fondo gris claro
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(15)
        
        # Header con título
        header_layout = QHBoxLayout()
        title_layout = QVBoxLayout()
        title = QLabel("Inicio de sesión")
        title.setFont(QFont("Segoe UI", 16))
        subtitle = QLabel("Ingrese su usuario y contraseña")
        subtitle.setFont(QFont("Segoe UI", 10))
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Contenedor principal
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        
        # Usuario
        user_layout = QHBoxLayout()
        user_fields = QVBoxLayout()
        user_label = QLabel("Usuario:")
        user_label.setFont(QFont("Segoe UI", 9))
        self.user_input = QLineEdit()
        self.user_input.setFixedWidth(250)
        user_fields.addWidget(user_label)
        user_fields.addWidget(self.user_input)
        user_layout.addLayout(user_fields)
        user_layout.addStretch()
        
        # Contraseña
        pass_layout = QHBoxLayout()
        pass_fields = QVBoxLayout()
        pass_label = QLabel("Contraseña:")
        pass_label.setFont(QFont("Segoe UI", 9))
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setFixedWidth(250)
        pass_fields.addWidget(pass_label)
        pass_fields.addWidget(self.pass_input)
        pass_layout.addLayout(pass_fields)
        pass_layout.addStretch()
        
        # Checkbox
        self.remember_checkbox = QCheckBox("Recordar nombre de usuario")
        self.remember_checkbox.setFont(QFont("Segoe UI", 9))
        
        # Botones inferiores
        button_layout = QHBoxLayout()
        self.db_button = QPushButton("Cambiar base de datos")
        self.db_button.setObjectName("dbButton")
        self.db_button.setFont(QFont("Segoe UI", 9))
        
        button_container = QHBoxLayout()
        self.login_button = QPushButton("Ingresar")
        self.login_button.setIcon(QIcon("icons/key.png"))
        self.login_button.setFont(QFont("Segoe UI", 9))
        
        self.close_button = QPushButton("Cerrar")
        self.close_button.setIcon(QIcon("icons/close.png"))
        self.close_button.setFont(QFont("Segoe UI", 9))
        
        button_layout.addWidget(self.db_button)
        button_layout.addStretch()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.close_button)
        
        # Agregar todos los elementos al layout principal
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(user_layout)
        main_layout.addLayout(pass_layout)
        main_layout.addWidget(self.remember_checkbox)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # Conectar señales
        self.close_button.clicked.connect(self.close)
        self.login_button.clicked.connect(self.login)
        self.db_button.clicked.connect(self.show_database_selector)
        
    def encrypt_password(self, password):
        """Encripta la contraseña usando MD5"""
        return hashlib.md5(password.encode()).hexdigest()

    def login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor ingrese usuario y contraseña")
            return
            
        # Por ahora pasamos una ruta vacía ya que estamos simulando
        success, message = Auth.verify_credentials(username, password, "")
        
        if success:
            # Ocultar la ventana de login
            self.hide()
            
            # Mostrar la ventana principal
            self.main_window = MainWindow()
            self.main_window.set_current_user(username)  # Establecer usuario actual
            self.main_window.show()
        else:
            # Verificar contraseña con MD5
            stored_password = Auth.get_stored_password(username)
            if stored_password == self.encrypt_password(password):
                # Ocultar la ventana de login
                self.hide()
                
                # Mostrar la ventana principal
                self.main_window = MainWindow()
                self.main_window.set_current_user(username)  # Establecer usuario actual
                self.main_window.show()
            else:
                QMessageBox.warning(self, "Error", message)
    
    def show_database_selector(self):
        dialog = DatabaseSelector(self)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
