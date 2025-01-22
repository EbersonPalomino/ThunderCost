from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QTextEdit, QCheckBox, QPushButton, QGroupBox,
                               QMessageBox)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

class ProfileDialog(QDialog):
    def __init__(self, parent=None, profile_data=None):
        super().__init__(parent)
        self.setWindowTitle("Perfil de Usuario")
        self.setMinimumWidth(600)
        self.profile_data = profile_data
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Grupo de datos del perfil
        profile_group = QGroupBox("Datos del perfil")
        profile_layout = QVBoxLayout(profile_group)
        
        # ID del Perfil
        id_layout = QHBoxLayout()
        id_label = QLabel("Id. del Perfil:")
        self.id_edit = QLineEdit()
        self.id_edit.setMaximumWidth(100)
        if profile_data:
            self.id_edit.setText(str(profile_data.get('id', '')))
            self.id_edit.setReadOnly(True)
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.id_edit)
        id_layout.addStretch()
        profile_layout.addLayout(id_layout)
        
        # Nombre del Perfil
        name_layout = QHBoxLayout()
        name_label = QLabel("Nombre de Perfil:")
        self.name_edit = QLineEdit()
        if profile_data:
            self.name_edit.setText(profile_data.get('name', ''))
            if profile_data.get('name') == "Administrador":
                self.name_edit.setReadOnly(True)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        profile_layout.addLayout(name_layout)
        
        # Descripción
        desc_label = QLabel("Descripción:")
        self.desc_edit = QTextEdit()
        self.desc_edit.setMinimumHeight(100)
        if profile_data:
            self.desc_edit.setText(profile_data.get('description', ''))
        profile_layout.addWidget(desc_label)
        profile_layout.addWidget(self.desc_edit)
        
        # Checkboxes de permisos
        self.store_required = QCheckBox("Los usuarios de este perfil deben tener una almacen asignada")
        self.can_change_store = QCheckBox("Los usuarios de este perfil pueden cambiar de almacen")
        self.can_have_cashbox = QCheckBox("Los usuarios de este perfil pueden tener una caja asignada")
        self.can_request_store = QCheckBox("Los usuarios de este perfil pueden solicitar a su mismo almacén asignado")
        
        if profile_data:
            self.store_required.setChecked(profile_data.get('store_required', False))
            self.can_change_store.setChecked(profile_data.get('can_change_store', False))
            self.can_have_cashbox.setChecked(profile_data.get('can_have_cashbox', False))
            self.can_request_store.setChecked(profile_data.get('can_request_store', False))
        
        profile_layout.addWidget(self.store_required)
        profile_layout.addWidget(self.can_change_store)
        profile_layout.addWidget(self.can_have_cashbox)
        profile_layout.addWidget(self.can_request_store)
        
        layout.addWidget(profile_group)
        
        # Botones
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.accept_btn = QPushButton("Aceptar")
        self.accept_btn.setIcon(QIcon("icons/accept.png"))
        self.accept_btn.clicked.connect(self.accept)
        
        self.cancel_btn = QPushButton("Cerrar")
        self.cancel_btn.setIcon(QIcon("icons/close.png"))
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.accept_btn)
        button_layout.addWidget(self.cancel_btn)
        
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
            QLineEdit, QTextEdit {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
                padding: 3px;
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
    
    def get_profile_data(self):
        return {
            'name': self.name_edit.text().strip(),
            'description': self.desc_edit.toPlainText().strip(),
            'store_required': self.store_required.isChecked(),
            'can_change_store': self.can_change_store.isChecked(),
            'can_have_cashbox': self.can_have_cashbox.isChecked(),
            'can_request_store': self.can_request_store.isChecked()
        }
    
    def validate(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Error", "El nombre del perfil es obligatorio")
            return False
        if not self.desc_edit.toPlainText().strip():
            QMessageBox.warning(self, "Error", "La descripción es obligatoria")
            return False
        return True
    
    def accept(self):
        if self.validate():
            super().accept()
