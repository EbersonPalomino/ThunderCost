from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt
import os
import shutil
import datetime

class BackupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generar Backup")
        self.setMinimumWidth(500)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Label y campo para la ubicación
        location_label = QLabel("Nombre y Ubicación de backup:")
        layout.addWidget(location_label)
        
        # Layout para el campo de ubicación y botón
        path_layout = QHBoxLayout()
        
        # Campo de ubicación
        self.path_input = QLineEdit()
        default_name = f"BASE DE DATOS MANT. SBI_{datetime.datetime.now().strftime('%Y%b%d')}.bak"
        default_path = os.path.join("D:", "Backups", default_name)
        self.path_input.setText(default_path)
        path_layout.addWidget(self.path_input)
        
        # Botón de elegir ubicación
        browse_button = QPushButton("Elegir Ubicación")
        browse_button.clicked.connect(self.browse_location)
        path_layout.addWidget(browse_button)
        
        layout.addLayout(path_layout)
        
        # Layout para los botones
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Botón generar
        generate_button = QPushButton("Generar")
        generate_button.clicked.connect(self.generate_backup)
        button_layout.addWidget(generate_button)
        
        # Botón cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        # Estilo
        self.setStyleSheet("""
            QDialog {
                background-color: #F0F0F0;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
                background-color: white;
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
    
    def browse_location(self):
        """Abre un diálogo para seleccionar la ubicación del backup"""
        from PySide6.QtWidgets import QFileDialog
        
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Backup",
            self.path_input.text(),
            "Backup Files (*.bak)"
        )
        
        if file_name:
            self.path_input.setText(file_name)
    
    def generate_backup(self):
        """Genera la copia de seguridad de la base de datos"""
        backup_path = self.path_input.text()
        
        # Verificar que la ruta no esté vacía
        if not backup_path:
            QMessageBox.warning(self, "Error", "Por favor especifique una ubicación para el backup")
            return
        
        try:
            # Crear el directorio si no existe
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            # Copiar el archivo de la base de datos
            shutil.copy2('database.db', backup_path)
            
            QMessageBox.information(
                self,
                "Éxito",
                f"Backup generado exitosamente en:\n{backup_path}"
            )
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al generar el backup:\n{str(e)}"
            )
