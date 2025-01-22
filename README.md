# Sistema de Gestión de Mantenimiento

Sistema de gestión desarrollado en Python con PySide6 para la administración de mantenimiento.

## Características

- Gestión de usuarios y perfiles
- Sistema de autenticación seguro
- Interfaz gráfica moderna y amigable
- Copias de seguridad de la base de datos
- Base de datos SQLite

## Requisitos

- Python 3.x
- PySide6
- SQLite3

## Instalación

1. Clonar el repositorio
```bash
git clone https://github.com/EbersonPalomino/sistema-gestion-mantenimiento.git
```

2. Instalar dependencias
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación
```bash
python login_window.py
```

## Estructura del Proyecto

- `login_window.py`: Ventana de inicio de sesión
- `main_window.py`: Ventana principal de la aplicación
- `user_window.py`: Administración de usuarios
- `profile_window.py`: Gestión de perfiles
- `db_connection.py`: Manejo de la base de datos
- `auth.py`: Sistema de autenticación
- `backup_dialog.py`: Gestión de copias de seguridad

## Contribuir

1. Fork el proyecto
2. Crear una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.
