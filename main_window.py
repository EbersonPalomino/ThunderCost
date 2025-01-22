from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QGridLayout, QToolBar, QTableWidget, QTableWidgetItem, QLineEdit)
from PySide6.QtGui import QIcon, QFont, QAction
from PySide6.QtCore import Qt
from user_window import UserWindow
from profile_window import ProfileWindow
from change_password_dialog import ChangePasswordDialog
from backup_dialog import BackupDialog

class DashboardButton(QPushButton):
    def __init__(self, title, icon_path, color, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.setIconSize(32, 32)
        if icon_path:
            self.setIcon(QIcon(icon_path))
        
        # Establecer el texto
        self.setText(title)
        self.setFont(QFont("Segoe UI", 9))
        
        # Estilo del botón
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                color: white;
                padding: 10px;
                text-align: center;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
        """)
    
    def darken_color(self, color):
        # Oscurecer el color para el efecto hover
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(max(0, c - 20) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión")
        self.setMinimumSize(1024, 768)
        
        # Almacenar el nombre de usuario actual
        self.current_user = None
        
        # Barra de herramientas superior
        toolbar = QToolBar("Toolbar")
        self.addToolBar(toolbar)
        
        actions = [
            ("Cerrar sesión", "icons/logout.png", self.logout),
            ("Usuarios", "icons/users.png", self.show_user_window),
            ("Perfiles", "icons/profiles.png", self.show_profile_window),
            ("Actualizar Perfil", "icons/update.png", None),
            ("Cambiar contraseña", "icons/password.png", self.show_change_password),
            ("Copia de seguridad", "icons/backup.png", self.show_backup_dialog),
            ("Optimizar base", "icons/optimize.png", None)
        ]
        
        for label, icon, slot in actions:
            action = QAction(QIcon(icon), label, self)
            if slot:
                action.triggered.connect(slot)
            toolbar.addAction(action)
        
        # Widget y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Sección de búsqueda
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Buscar proyecto aquí")
        search_button = QPushButton("Buscar")
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)
        
        # Sección de proyectos
        project_label = QLabel("Proyectos tipo (Todos)")
        project_label.setFont(QFont("Segoe UI", 12))
        main_layout.addWidget(project_label)
        
        # Tabla de proyectos
        project_table = QTableWidget()
        project_table.setColumnCount(2)
        project_table.setHorizontalHeaderLabels(["Proyecto", "Descripción"])
        project_table.setRowCount(2)
        project_table.setItem(0, 0, QTableWidgetItem("MUNICIPALIDAD DISTRITAL DE VILCABAMBA"))
        project_table.setItem(0, 1, QTableWidgetItem("MANTENIMIENTO DE LOS SISTEMAS DE SANEAMIENTO BÁSICO INTEGRAL DE LOS CENTROS POBLADOS FOCALIZADOS, EN LA CUENCA DE SAN MIGUEL, DISTRITO DE VILCABAMBA - LA CONVENCIÓN - CUSCO."))
        project_table.setItem(1, 0, QTableWidgetItem("MUNICIPALIDAD DISTRITAL DE VILCABAMBA"))
        project_table.setItem(1, 1, QTableWidgetItem("MANTENIMIENTO DE LAS ESCALINATAS DEL SECTOR DE TABLADA, CUENCA DE VILCABAMBA, DISTRITO DE VILCABAMBA - LA CONVENCIÓN – CUSCO"))
        main_layout.addWidget(project_table)

        # Estilo general de la ventana
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }
            QWidget {
                font-family: 'Segoe UI';
            }
            QToolBar {
                background-color: #2B579A;
                color: white;
            }
            QToolBar QToolButton {
                padding: 5px;
            }
            QToolBar QToolButton:hover {
                background-color: #1A4D8F;
            }
            QLabel {
                padding: 10px;
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
    
    def logout(self):
        from login_window import LoginWindow
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()

    def show_user_window(self):
        self.user_window = UserWindow()
        self.user_window.show()

    def show_profile_window(self):
        self.profile_window = ProfileWindow()
        self.profile_window.show()

    def set_current_user(self, username):
        self.current_user = username

    def show_change_password(self):
        if self.current_user:
            dialog = ChangePasswordDialog(self.current_user, self)
            dialog.exec_()

    def show_backup_dialog(self):
        """Muestra el diálogo de copia de seguridad"""
        dialog = BackupDialog(self)
        dialog.exec_()
