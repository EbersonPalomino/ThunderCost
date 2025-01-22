from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget,
                               QTableWidgetItem, QPushButton, QMessageBox, QInputDialog,
                               QHeaderView, QWidget, QLabel, QComboBox, QCheckBox)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import sqlite3
from profile_dialog import ProfileDialog

class ProfileWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Administrar Perfiles")
        self.setMinimumSize(800, 400)
        
        # Conectar a la base de datos
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        
        # Crear tabla si no existe
        self.create_table()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Tabla de perfiles
        self.profile_table = QTableWidget()
        self.profile_table.setColumnCount(2)
        self.profile_table.setHorizontalHeaderLabels(["Perfil", "Descripción"])
        self.profile_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.profile_table)
        
        # Botones del lado derecho
        button_layout = QHBoxLayout()
        right_buttons = QVBoxLayout()
        
        buttons = [
            ("Nuevo", "icons/new_user.png", self.add_profile),
            ("Editar", "icons/edit.png", self.edit_profile),
            ("Eliminar", "icons/delete.png", self.delete_profile),
            ("Permisos", "icons/key.png", self.manage_permissions),
            ("Atajos", "icons/shortcut.png", self.manage_shortcuts),
            ("Cerrar", "icons/close.png", self.close)
        ]
        
        for text, icon, slot in buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon))
            btn.clicked.connect(slot)
            btn.setMinimumWidth(120)
            right_buttons.addWidget(btn)
        
        right_buttons.addStretch()
        button_layout.addStretch()
        button_layout.addLayout(right_buttons)
        layout.addLayout(button_layout)
        
        # Cargar datos
        self.load_profiles()
        
        # Estilo
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }
            QPushButton {
                padding: 5px 10px;
                background-color: #E6E6E6;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
                text-align: left;
                padding-left: 10px;
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
        """)

    def create_table(self):
        # Respaldar datos existentes
        try:
            self.cursor.execute("SELECT name, description FROM profiles")
            existing_profiles = self.cursor.fetchall()
        except sqlite3.OperationalError:
            existing_profiles = []

        # Eliminar tabla existente
        self.cursor.execute("DROP TABLE IF EXISTS profiles")
        
        # Crear nueva tabla con la estructura actualizada
        self.cursor.execute('''
            CREATE TABLE profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL,
                store_required INTEGER NOT NULL DEFAULT 0,
                can_change_store INTEGER NOT NULL DEFAULT 0,
                can_have_cashbox INTEGER NOT NULL DEFAULT 0,
                can_request_store INTEGER NOT NULL DEFAULT 0
            )
        ''')
        
        # Restaurar datos existentes con valores por defecto para los nuevos campos
        for name, description in existing_profiles:
            is_admin = name == "Administrador"
            self.cursor.execute("""
                INSERT INTO profiles (
                    name, description, store_required, 
                    can_change_store, can_have_cashbox, can_request_store
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name, 
                description, 
                0,  # store_required
                1 if is_admin else 0,  # can_change_store
                1 if is_admin else 0,  # can_have_cashbox
                1 if is_admin else 0   # can_request_store
            ))

        # Insertar perfiles por defecto si no existen
        default_profiles = [
            ("Administrador", "Perfil de Administrador", 0, 1, 1, 1),
            ("Residente", "Residente de Obra", 0, 0, 0, 0),
            ("Supervisor/Inspector", "Supervisor o Inspector de Obra", 0, 0, 0, 0)
        ]
        
        for profile in default_profiles:
            try:
                self.cursor.execute("""
                    INSERT INTO profiles (
                        name, description, store_required, 
                        can_change_store, can_have_cashbox, can_request_store
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, profile)
            except sqlite3.IntegrityError:
                pass  # El perfil ya existe
                
        self.connection.commit()

    def load_profiles(self):
        self.cursor.execute("SELECT name, description FROM profiles")
        profiles = self.cursor.fetchall()
        
        self.profile_table.setRowCount(len(profiles))
        for row, (name, description) in enumerate(profiles):
            self.profile_table.setItem(row, 0, QTableWidgetItem(name))
            self.profile_table.setItem(row, 1, QTableWidgetItem(description))
            
            # Hacer que la primera columna no sea editable
            item = self.profile_table.item(row, 0)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
            # Colorear la fila del Administrador
            if name == "Administrador":
                for col in range(2):
                    item = self.profile_table.item(row, col)
                    item.setBackground(Qt.GlobalColor.yellow)

    def add_profile(self):
        dialog = ProfileDialog(self)
        if dialog.exec_():
            profile_data = dialog.get_profile_data()
            try:
                self.cursor.execute("""
                    INSERT INTO profiles (
                        name, description, store_required, 
                        can_change_store, can_have_cashbox, can_request_store
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    profile_data['name'],
                    profile_data['description'],
                    profile_data['store_required'],
                    profile_data['can_change_store'],
                    profile_data['can_have_cashbox'],
                    profile_data['can_request_store']
                ))
                self.connection.commit()
                self.load_profiles()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Error", "El perfil ya existe")

    def edit_profile(self):
        current_row = self.profile_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Por favor seleccione un perfil")
            return
            
        profile_name = self.profile_table.item(current_row, 0).text()
        if profile_name == "Administrador":
            QMessageBox.warning(self, "Error", "No se puede editar el perfil Administrador")
            return
            
        # Obtener datos actuales del perfil
        self.cursor.execute("""
            SELECT id, name, description, store_required, 
                   can_change_store, can_have_cashbox, can_request_store 
            FROM profiles WHERE name = ?
        """, (profile_name,))
        profile_data = self.cursor.fetchone()
        
        if profile_data:
            dialog = ProfileDialog(self, {
                'id': profile_data[0],
                'name': profile_data[1],
                'description': profile_data[2],
                'store_required': bool(profile_data[3]),
                'can_change_store': bool(profile_data[4]),
                'can_have_cashbox': bool(profile_data[5]),
                'can_request_store': bool(profile_data[6])
            })
            
            if dialog.exec_():
                new_data = dialog.get_profile_data()
                try:
                    self.cursor.execute("""
                        UPDATE profiles SET 
                            description = ?,
                            store_required = ?,
                            can_change_store = ?,
                            can_have_cashbox = ?,
                            can_request_store = ?
                        WHERE name = ?
                    """, (
                        new_data['description'],
                        new_data['store_required'],
                        new_data['can_change_store'],
                        new_data['can_have_cashbox'],
                        new_data['can_request_store'],
                        profile_name
                    ))
                    self.connection.commit()
                    self.load_profiles()
                except sqlite3.Error as e:
                    QMessageBox.warning(self, "Error", f"Error al actualizar el perfil: {str(e)}")

    def delete_profile(self):
        current_row = self.profile_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Por favor seleccione un perfil")
            return
            
        profile_name = self.profile_table.item(current_row, 0).text()
        if profile_name == "Administrador":
            QMessageBox.warning(self, "Error", "No se puede eliminar el perfil Administrador")
            return
            
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar el perfil {profile_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Verificar si hay usuarios usando este perfil
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE profile = ?", (profile_name,))
            if self.cursor.fetchone()[0] > 0:
                QMessageBox.warning(
                    self,
                    "Error",
                    "No se puede eliminar el perfil porque hay usuarios asignados a él"
                )
                return
                
            self.cursor.execute("DELETE FROM profiles WHERE name = ?", (profile_name,))
            self.connection.commit()
            self.load_profiles()

    def manage_permissions(self):
        QMessageBox.information(
            self,
            "Permisos",
            "Funcionalidad de gestión de permisos en desarrollo"
        )

    def manage_shortcuts(self):
        QMessageBox.information(
            self,
            "Atajos",
            "Funcionalidad de gestión de atajos en desarrollo"
        )

    def closeEvent(self, event):
        self.connection.close()
        event.accept()
