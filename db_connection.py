import sqlite3
from PySide6.QtWidgets import QMessageBox

class DatabaseConnection:
    _connection = None

    @staticmethod
    def get_connection():
        """
        Retorna una conexión única a la base de datos.
        Si la conexión no existe, la crea.
        """
        if DatabaseConnection._connection is None:
            db_path = 'database.db'
            DatabaseConnection._connection = sqlite3.connect(db_path)
            
            # Crear las tablas si no existen
            cursor = DatabaseConnection._connection.cursor()
            
            # Tabla de usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    name TEXT PRIMARY KEY,
                    email TEXT UNIQUE,
                    password TEXT,
                    enabled INTEGER DEFAULT 1,
                    profile TEXT,
                    can_manage_users INTEGER DEFAULT 0,
                    is_registered INTEGER DEFAULT 0
                )
            ''')
            
            # Tabla de perfiles
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS profiles (
                    name TEXT PRIMARY KEY,
                    description TEXT,
                    permissions TEXT
                )
            ''')
            
            # Insertar usuario administrador por defecto si no existe
            cursor.execute('SELECT name FROM users WHERE name = ?', ('Administrador',))
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO users (
                        name, email, password, enabled, 
                        profile, can_manage_users, is_registered
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'Administrador',
                    'admin@example.com',
                    'admin123',
                    1,
                    'Administrador',
                    1,
                    1
                ))
            
            DatabaseConnection._connection.commit()
        
        return DatabaseConnection._connection

    @staticmethod
    def close_connection():
        """
        Cierra la conexión a la base de datos si existe.
        """
        if DatabaseConnection._connection is not None:
            DatabaseConnection._connection.close()
            DatabaseConnection._connection = None

    @staticmethod
    def test_connection(db_type, db_path):
        try:
            if db_type == "SQLite":
                conn = sqlite3.connect(db_path)
                conn.close()
                return True, "Conexión exitosa a la base de datos SQLite."
            
            elif db_type in ["SQL Server", "SQL Server 2000"]:
                # Aquí iría la lógica para SQL Server
                # Por ahora solo simulamos
                if not db_path:
                    return False, "Por favor especifique la ruta de la base de datos."
                return True, "Conexión exitosa a SQL Server."
            
            elif db_type == "Oracle":
                # Aquí iría la lógica para Oracle
                if not db_path:
                    return False, "Por favor especifique la ruta de la base de datos."
                return True, "Conexión exitosa a Oracle."
            
            elif db_type == "Postgres":
                # Aquí iría la lógica para PostgreSQL
                if not db_path:
                    return False, "Por favor especifique la ruta de la base de datos."
                return True, "Conexión exitosa a PostgreSQL."
            
            elif db_type == "MySQL":
                # Aquí iría la lógica para MySQL
                if not db_path:
                    return False, "Por favor especifique la ruta de la base de datos."
                return True, "Conexión exitosa a MySQL."
            
            else:
                return False, f"Tipo de base de datos no soportado: {db_type}"
                
        except sqlite3.Error as e:
            return False, f"Error de conexión SQLite: {str(e)}"
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"

    @staticmethod
    def show_connection_result(parent, success, message):
        icon = QMessageBox.Information if success else QMessageBox.Critical
        title = "Prueba de Conexión" if success else "Error de Conexión"
        
        msg = QMessageBox(parent)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
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
