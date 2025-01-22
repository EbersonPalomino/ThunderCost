from PySide6.QtWidgets import (QDialog, QLabel, QComboBox, QLineEdit, 
                             QPushButton, QVBoxLayout, QHBoxLayout, 
                             QFrame, QFileDialog, QGroupBox, QMessageBox)
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt
from db_connection import DatabaseConnection

class DatabaseSelector(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar base de datos")
        self.setFixedSize(600, 400)
        
        # Estilo general
        self.setStyleSheet("""
            QDialog {
                background-color: #E6E7E8;
            }
            QGroupBox {
                background-color: #F0F0F0;
                border: 1px solid #CCCCCC;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                background: white;
            }
            QComboBox {
                min-width: 200px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(icons/dropdown.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #CCCCCC;
                selection-background-color: #FFE794;
                selection-color: black;
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
        """)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header con ícono y título
        header_layout = QHBoxLayout()
        
        # Ícono de base de datos
        icon_label = QLabel()
        icon_label.setFixedSize(48, 48)
        icon_label.setPixmap(QPixmap("icons/database.png").scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header_layout.addWidget(icon_label)
        
        # Título y descripción
        title_layout = QVBoxLayout()
        title = QLabel("Seleccionar base de datos")
        title.setFont(QFont("Segoe UI", 14))
        description = QLabel("Configure aquí la conexión a la base de datos cuando inicia por\nprimera vez o cuando necesite cambiar de base de datos")
        description.setFont(QFont("Segoe UI", 9))
        title_layout.addWidget(title)
        title_layout.addWidget(description)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Grupo: Tipo de base de datos
        db_type_group = QGroupBox("Tipo de base de datos")
        db_type_layout = QVBoxLayout(db_type_group)
        
        type_layout = QHBoxLayout()
        type_label = QLabel("Tipo de base de datos:")
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "SQLite",
            "SQL Server",
            "SQL Server 2000",
            "Oracle",
            "Postgres",
            "SQLite",
            "MySQL",
            "<Importar conexión...>"
        ])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        type_layout.addStretch()
        db_type_layout.addLayout(type_layout)
        
        # Grupo: Ubicación de la base de datos
        db_location_group = QGroupBox("Ubicación de la base de datos")
        db_location_layout = QVBoxLayout(db_location_group)
        
        path_layout = QHBoxLayout()
        path_label = QLabel("Archivo de Base de Datos:")
        self.path_input = QLineEdit()
        self.browse_button = QPushButton("...")
        self.browse_button.setFixedWidth(30)
        self.browse_button.setIcon(QIcon("icons/folder.png"))
        self.browse_button.clicked.connect(self.browse_file)
        
        self.new_db_button = QPushButton("Iniciar base de datos en blanco")
        self.new_db_button.setIcon(QIcon("icons/new.png"))
        
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_button)
        
        db_location_layout.addLayout(path_layout)
        db_location_layout.addWidget(self.new_db_button, alignment=Qt.AlignRight)
        
        # Botones inferiores
        button_layout = QHBoxLayout()
        self.test_button = QPushButton("Probar conexión")
        self.test_button.setIcon(QIcon("icons/test.png"))
        self.accept_button = QPushButton("Aceptar")
        self.accept_button.setIcon(QIcon("icons/accept.png"))
        self.close_button = QPushButton("Cerrar")
        self.close_button.setIcon(QIcon("icons/cancel.png"))
        
        button_layout.addWidget(self.test_button)
        button_layout.addStretch()
        button_layout.addWidget(self.accept_button)
        button_layout.addWidget(self.close_button)
        
        # Conectar señales
        self.close_button.clicked.connect(self.reject)
        self.accept_button.clicked.connect(self.accept)
        self.test_button.clicked.connect(self.test_connection)
        
        # Agregar todos los elementos al layout principal
        main_layout.addLayout(header_layout)
        main_layout.addWidget(db_type_group)
        main_layout.addWidget(db_location_group)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
    
    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de base de datos",
            "",
            "Archivos de base de datos (*.db *.sqlite);;Todos los archivos (*.*)"
        )
        if file_name:
            self.path_input.setText(file_name)
    
    def test_connection(self):
        db_type = self.type_combo.currentText()
        db_path = self.path_input.text().strip()
        
        if not db_path:
            DatabaseConnection.show_connection_result(
                self,
                False,
                "Por favor seleccione un archivo de base de datos."
            )
            return
        
        success, message = DatabaseConnection.test_connection(db_type, db_path)
        DatabaseConnection.show_connection_result(self, success, message)
