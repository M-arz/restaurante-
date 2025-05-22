# PROYECTO FINAL_JHAN

Aplicación web desarrollada en **Python (Flask)** para la gestión de menús y pedidos. Incluye funcionalidades de autenticación de usuarios, registro, administración de menús y visualización de pedidos.

---

## 📁 Estructura del Proyecto

```
PROYECTO_FINAL_JHAN/
│
├── BD/
│   └── schema.sql                # Script SQL para crear las tablas de la base de datos
│
├── conexion/                     # Lógica de conexión a la base de datos
│
├── controllers/                 # Controladores para lógica de negocio
│   ├── auth_controller.py        # Lógica de autenticación y registro
│   ├── menu_controller.py        # Lógica relacionada con los menús
│   └── order_controller.py       # Controlador de pedidos
│
├── routers/                      # Carpeta para rutas (puede estar vacía o en desarrollo)
│
├── templates/                    # Archivos HTML renderizados con Jinja2
│   ├── dashboard.html
│   ├── layout.html
│   ├── login.html
│   ├── menu_form.html
│   ├── menu.html
│   ├── order_detail.html
│   ├── order_form.html
│   ├── orders.html
│   └── register.html
│
├── venv/                         # Entorno virtual de Python
│
├── app.py                        # Archivo principal de configuración de Flask
├── requirements.txt              # Lista de dependencias del proyecto
└── run.py                        # Archivo para ejecutar la aplicación
```

---

## 🚀 Funcionalidades Principales

- Registro e inicio de sesión de usuarios
- Panel de administración (dashboard)
- Crear, leer y eliminar menús
- Registrar y ver pedidos
- Plantillas reutilizables con Jinja2

---

## ⚙️ Tecnologías Usadas

- Python 3.x
- Flask
- SQLite (o base de datos definida en `conexion`)
- HTML5 + Jinja2
- Bootstrap (si se aplica)

---

## 🛠️ Instalación y Ejecución

1. **Clona el repositorio:**

```bash
git clone https://github.com/tuusuario/PROYECTO_FINAL_JHAN.git
cd PROYECTO_FINAL_JHAN
```

2. **Crea el entorno virtual:**

```bash
python -m venv venv
```

3. **Activa el entorno virtual:**

- En Windows:

```bash
venv\Scripts\activate
```

- En macOS/Linux:

```bash
source venv/bin/activate
```

4. **Instala las dependencias:**

```bash
pip install -r requirements.txt
```

5. **Inicializa la base de datos:**

```bash
sqlite3 basedatos.db < BD/schema.sql
```

6. **Ejecuta la aplicación:**

```bash
python run.py
```

---

## 📌 Mejoras Futuras

- Agregar roles de usuario (administrador, cliente)
- Agregar validaciones avanzadas en formularios
- Mejorar el diseño visual con CSS o frameworks modernos
- Modularizar rutas en la carpeta `routers/`

---



**Desarrollado por:** Jhan-Andres-Brian



