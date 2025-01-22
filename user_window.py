from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget,
                               QTableWidgetItem, QPushButton, QMessageBox, QInputDialog,
                               QHeaderView, QWidget, QLabel, QComboBox, QCheckBox, 
                               QDialog, QGroupBox, QLineEdit, QStyle)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import sqlite3

class AddEditUserDialog(QDialog):
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.setWindowTitle("Registro de usuario" if not user_data else "Editar Usuario")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        
        # Datos del usuario
        user_group = QGroupBox("Datos del usuario")
        user_layout = QGridLayout()
        
        self.registered_check = QCheckBox("El usuario ya está registrado en Persona General")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ingrese nombres")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ingrese e-mail")
        
        user_layout.addWidget(self.registered_check, 0, 0, 1, 2)
        user_layout.addWidget(QLabel("Nombres y Apellidos:"), 1, 0)
        user_layout.addWidget(self.name_input, 1, 1)
        user_layout.addWidget(QLabel("Email:"), 2, 0)
        user_layout.addWidget(self.email_input, 2, 1)
        
        user_group.setLayout(user_layout)
        layout.addWidget(user_group)
        
        # Datos de acceso
        access_group = QGroupBox("Datos de acceso")
        access_layout = QGridLayout()
        
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.enabled_check = QCheckBox("Habilitado")
        self.enabled_check.setChecked(True)
        
        # Radio buttons para cifrado
        cipher_label = QLabel("Cifrado:")
        self.cipher_none = QRadioButton("Ninguna")
        self.cipher_basic = QRadioButton("Básica")
        self.cipher_md5 = QRadioButton("Avanzada (MD5)")
        self.cipher_none.setChecked(True)
        
        cipher_layout = QHBoxLayout()
        cipher_layout.addWidget(self.cipher_none)
        cipher_layout.addWidget(self.cipher_basic)
        cipher_layout.addWidget(self.cipher_md5)
        
        access_layout.addWidget(QLabel("Login:"), 0, 0)
        access_layout.addWidget(self.login_input, 0, 1)
        access_layout.addWidget(self.enabled_check, 0, 2)
        access_layout.addWidget(QLabel("Password:"), 1, 0)
        access_layout.addWidget(self.password_input, 1, 1)
        access_layout.addWidget(cipher_label, 2, 0)
        access_layout.addLayout(cipher_layout, 2, 1, 1, 2)
        
        access_group.setLayout(access_layout)
        layout.addWidget(access_group)
        
        # Opciones de Acceso
        options_group = QGroupBox("Opciones de Acceso")
        options_layout = QGridLayout()
        
        self.profile_combo = QComboBox()
        self.load_profiles()  # Cargar perfiles desde la base de datos
        
        self.manage_users_check = QCheckBox("Administrar usuarios")
        
        options_layout.addWidget(QLabel("Perfil:"), 0, 0)
        options_layout.addWidget(self.profile_combo, 0, 1)
        options_layout.addWidget(self.manage_users_check, 1, 0, 1, 2)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Botones
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Guardar")
        close_btn = QPushButton("Cerrar")
        close_btn.setIcon(QIcon("icons/close.png"))
        
        save_btn.clicked.connect(self.accept)
        close_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        # Cargar datos si es edición
        if user_data:
            self.name_input.setText(user_data['username'])
            self.email_input.setText(user_data['email'])
            self.enabled_check.setChecked(user_data['enabled'])
            self.login_input.setText(user_data['username'])
            self.profile_combo.setCurrentText(user_data['profile'])
            self.manage_users_check.setChecked(user_data['can_manage_users'])
            self.registered_check.setChecked(user_data['is_registered'])
            
        # Estilo
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #CCCCCC;
                margin-top: 12px;
                padding-top: 24px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 3px;
            }
            QPushButton {
                min-width: 80px;
                padding: 5px 10px;
                background-color: #E6E6E6;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #D6D6D6;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
                background-color: white;
            }
        """)
    
    def load_profiles(self):
        # Limpiar el combo
        self.profile_combo.clear()
        
        # Agregar opción "Todos"
        self.profile_combo.addItem("(Todos)")
        
        # Cargar perfiles desde la base de datos
        try:
            self.cursor.execute("SELECT name FROM profiles ORDER BY name")
            profiles = self.cursor.fetchall()
            for profile in profiles:
                self.profile_combo.addItem(profile[0])
        except sqlite3.OperationalError:
            # Si la tabla no existe, usar valores por defecto
            self.profile_combo.addItems(["Administrador", "Usuario", "Residente", "Supervisor/Inspector"])
    
    def get_password(self):
        password = self.password_input.text()
        if self.cipher_md5.isChecked():
            return hashlib.md5(password.encode()).hexdigest()
        elif self.cipher_basic.isChecked():
            # Implementar cifrado básico aquí si es necesario
            return password
        return password

class UserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administrador de Usuarios")
        self.setMinimumSize(900, 600)

        # Conectar a la base de datos
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        
        # Crear tabla si no existe
        self.create_table()

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Barra superior
        top_bar = QHBoxLayout()
        
        # Perfil combobox
        profile_label = QLabel("Perfil")
        self.profile_combo = QComboBox()
        self.load_profiles()  # Cargar perfiles desde la base de datos
        self.profile_combo.currentTextChanged.connect(self.load_users)
        
        top_bar.addWidget(profile_label)
        top_bar.addWidget(self.profile_combo)
        top_bar.addStretch()

        # Botones
        self.new_btn = QPushButton("Nuevo")
        self.edit_btn = QPushButton("Editar")
        self.view_btn = QPushButton("Ver")
        
        self.new_btn.clicked.connect(self.add_user)
        self.edit_btn.clicked.connect(self.edit_user)
        self.view_btn.clicked.connect(self.view_user)
        
        top_bar.addWidget(self.new_btn)
        top_bar.addWidget(self.edit_btn)
        top_bar.addWidget(self.view_btn)
        
        layout.addLayout(top_bar)

        # Tabla de usuarios
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels([
            "Nombre de Usuario", "Habilitado", "E-mail", "Perfil"
        ])
        self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.user_table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.user_table)

        # Barra inferior
        bottom_bar = QHBoxLayout()
        
        self.hide_disabled = QCheckBox("Ocultar usuarios deshabilitados")
        self.hide_disabled.stateChanged.connect(self.load_users)
        
        self.close_btn = QPushButton("Cerrar")
        self.close_btn.clicked.connect(self.close)
        
        bottom_bar.addWidget(self.hide_disabled)
        bottom_bar.addStretch()
        bottom_bar.addWidget(self.close_btn)
        
        layout.addLayout(bottom_bar)

        # Cargar usuarios
        self.load_users()

        # Estilo
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }
            QPushButton {
                min-width: 80px;
                padding: 5px 10px;
                background-color: #E6E6E6;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #D6D6D6;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #CCCCCC;
            }
            QHeaderView::section {
                background-color: #E6E6E6;
                padding: 4px;
                border: 1px solid #CCCCCC;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
                background-color: white;
            }
        """)
    
    def create_table(self):
        # Respaldar datos existentes
        try:
            self.cursor.execute("SELECT name, email, password FROM users")
            existing_users = self.cursor.fetchall()
        except sqlite3.OperationalError:
            existing_users = []

        # Eliminar tabla existente
        self.cursor.execute("DROP TABLE IF EXISTS users")
        
        # Crear nueva tabla con la estructura actualizada
        self.cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                enabled INTEGER DEFAULT 1,
                profile TEXT DEFAULT 'Administrador',
                can_manage_users INTEGER DEFAULT 0,
                is_registered INTEGER DEFAULT 0
            )
        ''')

        # Restaurar datos existentes
        for user in existing_users:
            try:
                self.cursor.execute("""
                    INSERT INTO users (name, email, password, enabled, profile, can_manage_users)
                    VALUES (?, ?, ?, 1, 'Administrador', 1)
                """, user)
            except sqlite3.IntegrityError:
                continue

        self.connection.commit()

    def load_profiles(self):
        # Limpiar el combo
        self.profile_combo.clear()
        
        # Agregar opción "Todos"
        self.profile_combo.addItem("(Todos)")
        
        # Cargar perfiles desde la base de datos
        try:
            self.cursor.execute("SELECT name FROM profiles ORDER BY name")
            profiles = self.cursor.fetchall()
            for profile in profiles:
                self.profile_combo.addItem(profile[0])
        except sqlite3.OperationalError:
            # Si la tabla no existe, usar valores por defecto
            self.profile_combo.addItems(["Administrador", "Usuario", "Residente", "Supervisor/Inspector"])
    
    def load_users(self):
        query = """
            SELECT name as username, 
                   enabled, 
                   email,
                   COALESCE(profile, 'Administrador') as profile 
            FROM users
            WHERE 1=1
        """
        
        # Filtrar por perfil seleccionado
        selected_profile = self.profile_combo.currentText()
        if selected_profile != "(Todos)":
            query += f" AND profile = '{selected_profile}'"

        # Filtrar usuarios deshabilitados
        if self.hide_disabled.isChecked():
            query += " AND enabled = 1"
            
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        self.user_table.setRowCount(len(users))

        for row_idx, user in enumerate(users):
            # Username
            self.user_table.setItem(row_idx, 0, QTableWidgetItem(user[0]))
            
            # Enabled checkbox
            enabled_check = QCheckBox()
            enabled_check.setChecked(bool(user[1]))
            enabled_check.setEnabled(False)
            self.user_table.setCellWidget(row_idx, 1, enabled_check)
            
            # Email
            self.user_table.setItem(row_idx, 2, QTableWidgetItem(user[2]))
            
            # Profile
            self.user_table.setItem(row_idx, 3, QTableWidgetItem(user[3]))

    def add_user(self):
        dialog = AddEditUserDialog(self)
        if dialog.exec_():
            username = dialog.name_input.text().strip()
            email = dialog.email_input.text().strip()
            password = dialog.get_password()
            enabled = dialog.enabled_check.isChecked()
            profile = dialog.profile_combo.currentText()
            can_manage_users = dialog.manage_users_check.isChecked()
            is_registered = dialog.registered_check.isChecked()
            
            if username and email and password:
                try:
                    self.cursor.execute("""
                        INSERT INTO users (
                            name, email, password, enabled, 
                            profile, can_manage_users, is_registered
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (username, email, password, enabled,
                          profile, can_manage_users, is_registered))
                    self.connection.commit()
                    self.load_users()
                    QMessageBox.information(self, "Éxito", "Usuario agregado correctamente")
                except sqlite3.IntegrityError as e:
                    if "name" in str(e):
                        QMessageBox.warning(self, "Error", "El nombre de usuario ya existe")
                    else:
                        QMessageBox.warning(self, "Error", "El email ya está registrado")
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son requeridos")

    def edit_user(self):
        current_row = self.user_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Por favor seleccione un usuario")
            return

        username = self.user_table.item(current_row, 0).text()
        self.cursor.execute("""
            SELECT name, email, password, enabled, profile, 
                   can_manage_users, is_registered 
            FROM users WHERE name = ?
        """, (username,))
        user = self.cursor.fetchone()
        
        if user:
            dialog = QDialog(self)
            dialog.setWindowTitle("Editar Usuario")
            dialog.setMinimumWidth(400)
            
            layout = QVBoxLayout(dialog)
            
            # Datos del usuario
            user_group = QGroupBox("Datos del usuario")
            user_layout = QVBoxLayout()
            
            # Nombre
            name_layout = QHBoxLayout()
            name_label = QLabel("Nombre:")
            self.name_edit = QLineEdit(user[0])
            name_layout.addWidget(name_label)
            name_layout.addWidget(self.name_edit)
            user_layout.addLayout(name_layout)
            
            # Email
            email_layout = QHBoxLayout()
            email_label = QLabel("Email:")
            self.email_edit = QLineEdit(user[1])
            email_layout.addWidget(email_label)
            email_layout.addWidget(self.email_edit)
            user_layout.addLayout(email_layout)
            
            user_group.setLayout(user_layout)
            layout.addWidget(user_group)
            
            # Datos de acceso
            access_group = QGroupBox("Datos de acceso")
            access_layout = QVBoxLayout()
            
            # Login (nombre de usuario, no editable)
            login_layout = QHBoxLayout()
            login_label = QLabel("Login:")
            self.login_edit = QLineEdit(user[0])
            self.login_edit.setReadOnly(True)
            login_layout.addWidget(login_label)
            login_layout.addWidget(self.login_edit)
            access_layout.addLayout(login_layout)
            
            # Contraseña
            password_layout = QHBoxLayout()
            password_label = QLabel("Contraseña:")
            self.password_edit = QLineEdit()
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_edit.setPlaceholderText("Dejar en blanco para mantener la actual")
            password_layout.addWidget(password_label)
            password_layout.addWidget(self.password_edit)
            access_layout.addLayout(password_layout)
            
            # Perfil
            profile_layout = QHBoxLayout()
            profile_label = QLabel("Perfil:")
            self.dialog_profile_combo = QComboBox()
            
            # Cargar perfiles desde la base de datos
            try:
                self.cursor.execute("SELECT name FROM profiles ORDER BY name")
                profiles = self.cursor.fetchall()
                for profile in profiles:
                    self.dialog_profile_combo.addItem(profile[0])
                # Seleccionar el perfil actual del usuario
                index = self.dialog_profile_combo.findText(user[4])
                if index >= 0:
                    self.dialog_profile_combo.setCurrentIndex(index)
            except sqlite3.OperationalError:
                # Si la tabla no existe, usar valores por defecto
                self.dialog_profile_combo.addItems(["Administrador", "Usuario", "Residente", "Supervisor/Inspector"])
                
            profile_layout.addWidget(profile_label)
            profile_layout.addWidget(self.dialog_profile_combo)
            access_layout.addLayout(profile_layout)
            
            access_group.setLayout(access_layout)
            layout.addWidget(access_group)
            
            # Opciones de acceso
            options_group = QGroupBox("Opciones de acceso")
            options_layout = QVBoxLayout()
            
            # Usuario habilitado
            self.enabled_check = QCheckBox("Usuario habilitado")
            self.enabled_check.setChecked(bool(user[3]))
            options_layout.addWidget(self.enabled_check)
            
            # Usuario registrado
            self.registered_check = QCheckBox("Usuario registrado")
            self.registered_check.setChecked(bool(user[6]))
            options_layout.addWidget(self.registered_check)
            
            # Gestión de usuarios
            self.manage_users_check = QCheckBox("Puede gestionar usuarios")
            self.manage_users_check.setChecked(bool(user[5]))
            options_layout.addWidget(self.manage_users_check)
            
            options_group.setLayout(options_layout)
            layout.addWidget(options_group)
            
            # Botones
            button_layout = QHBoxLayout()
            save_button = QPushButton("Guardar")
            save_button.clicked.connect(lambda: self.save_edited_user(username))
            cancel_button = QPushButton("Cancelar")
            cancel_button.clicked.connect(dialog.reject)
            
            button_layout.addWidget(save_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)
            
            self.dialog = dialog
            dialog.exec_()

    def save_edited_user(self, old_username):
        # Validar campos requeridos
        if not self.name_edit.text().strip():
            QMessageBox.warning(self.dialog, "Error", "El nombre es obligatorio")
            return
        if not self.email_edit.text().strip():
            QMessageBox.warning(self.dialog, "Error", "El email es obligatorio")
            return
            
        try:
            # Preparar la consulta SQL
            if self.password_edit.text():
                # Si se proporcionó una nueva contraseña
                self.cursor.execute("""
                    UPDATE users SET 
                        name = ?, 
                        email = ?,
                        password = ?,
                        enabled = ?,
                        profile = ?,
                        can_manage_users = ?,
                        is_registered = ?
                    WHERE name = ?
                """, (
                    self.name_edit.text(),
                    self.email_edit.text(),
                    self.password_edit.text(),
                    self.enabled_check.isChecked(),
                    self.dialog_profile_combo.currentText(),
                    self.manage_users_check.isChecked(),
                    self.registered_check.isChecked(),
                    old_username
                ))
            else:
                # Si no se proporcionó nueva contraseña, mantener la actual
                self.cursor.execute("""
                    UPDATE users SET 
                        name = ?, 
                        email = ?,
                        enabled = ?,
                        profile = ?,
                        can_manage_users = ?,
                        is_registered = ?
                    WHERE name = ?
                """, (
                    self.name_edit.text(),
                    self.email_edit.text(),
                    self.enabled_check.isChecked(),
                    self.dialog_profile_combo.currentText(),
                    self.manage_users_check.isChecked(),
                    self.registered_check.isChecked(),
                    old_username
                ))
                
            self.connection.commit()
            self.dialog.accept()
            self.load_users()
            
        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self.dialog,
                "Error",
                "El nombre de usuario o email ya existe"
            )

    def view_user(self):
        current_row = self.user_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Por favor seleccione un usuario")
            return

        username = self.user_table.item(current_row, 0).text()
        self.cursor.execute("""
            SELECT name, email, enabled, profile 
            FROM users WHERE name = ?
        """, (username,))
        user = self.cursor.fetchone()
        
        if user:
            dialog = QDialog(self)
            dialog.setWindowTitle("Detalles del Usuario")
            dialog.setMinimumWidth(400)
            
            layout = QVBoxLayout(dialog)
            
            # Contenedor principal
            content_layout = QHBoxLayout()
            
            # Icono de información
            icon_label = QLabel()
            icon = dialog.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
            icon_label.setPixmap(icon.pixmap(48, 48))
            content_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignTop)
            
            # Información del usuario
            info_layout = QVBoxLayout()
            
            fields = [
                ("Nombre de Usuario:", user[0]),
                ("Email:", user[1]),
                ("Habilitado:", "Sí" if user[2] else "No"),
                ("Perfil:", user[3] if user[3] else "No asignado")
            ]
            
            for label, value in fields:
                text = QLabel(f"<b>{label}</b> {value}")
                text.setTextFormat(Qt.TextFormat.RichText)
                info_layout.addWidget(text)
            
            content_layout.addLayout(info_layout)
            layout.addLayout(content_layout)
            
            # Botón OK
            button_layout = QHBoxLayout()
            ok_button = QPushButton("OK")
            ok_button.setFixedWidth(100)
            ok_button.clicked.connect(dialog.accept)
            button_layout.addStretch()
            button_layout.addWidget(ok_button)
            layout.addLayout(button_layout)
            
            # Estilo
            dialog.setStyleSheet("""
                QDialog {
                    background-color: white;
                }
                QLabel {
                    font-size: 10pt;
                    color: #333333;
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
            """)
            
            dialog.exec_()
    
    def closeEvent(self, event):
        self.connection.close()
        event.accept()
