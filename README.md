Sistema de Notas Académicas
1. Descripción del proyecto

El Sistema de Notas Académicas es una aplicación web desarrollada con Python y Flask, cuyo objetivo es facilitar la administración de la información académica de una institución educativa.

El sistema permite gestionar estudiantes, docentes, asignaturas y calificaciones mediante una interfaz web intuitiva, organizada y adaptable a diferentes dispositivos.

La aplicación utiliza plantillas Jinja2 para la presentación de las vistas y Bootstrap 5 para el diseño de la interfaz gráfica.

2. Objetivos
Administrar la información de los estudiantes.
Gestionar los datos de los docentes.
Registrar y administrar las asignaturas.
Registrar y consultar las calificaciones de los estudiantes.
Facilitar la organización de la información académica.
Proporcionar una interfaz sencilla y amigable para los usuarios.
3. Funcionalidades principales
Gestión de estudiantes
Registrar estudiantes.
Consultar estudiantes registrados.
Editar información de estudiantes.
Eliminar registros de estudiantes.
Gestión de docentes
Registrar docentes.
Consultar docentes.
Actualizar información.
Eliminar registros.
Gestión de asignaturas
Registrar asignaturas.
Consultar asignaturas.
Modificar información.
Eliminar asignaturas.
Gestión de notas
Registrar calificaciones.
Consultar notas.
Administrar información de las calificaciones.
Interfaz de usuario
Barra de navegación superior (Navbar).
Menú lateral de navegación (Sidebar).
Identificación del usuario autenticado.
Opción para cerrar sesión.
Mensajes de confirmación y notificación.
Diseño adaptable a dispositivos móviles.
4. Tecnologías utilizadas
Tecnología	Descripción
Python	Lenguaje de programación
Flask	Framework para desarrollo web
Jinja2	Motor de plantillas
HTML5	Estructura de las páginas
CSS3	Estilos de la aplicación
Bootstrap 5.3.3	Diseño adaptable
Bootstrap Icons	Iconografía
JavaScript	Interactividad
SQLite / MySQL	Base de datos, según configuración
5. Requisitos previos

Para ejecutar el proyecto es necesario tener instalado:

Python 3.10 o superior.
pip (administrador de paquetes de Python).
Git (opcional).
Un editor de código, como Visual Studio Code.
El motor de base de datos correspondiente a la configuración del proyecto.
6. Instalación del proyecto
Paso 1. Clonar el repositorio
bash
git clone URL_DEL_REPOSITORIO


Ingresar a la carpeta del proyecto:

bash
cd sistema-notas

Paso 2. Crear un entorno virtual

En Windows:

bash
python -m venv venv


Activar el entorno virtual:

bash
venv\Scripts\activate


En Linux o macOS:

bash
python3 -m venv venv
source venv/bin/activate

Paso 3. Instalar dependencias

Si el proyecto dispone de un archivo requirements.txt:

bash
pip install -r requirements.txt


Si todavía no existe, instalar Flask:

bash
pip install Flask


Instalar las demás dependencias que requiera la aplicación según su configuración.

7. Estructura del proyecto

La estructura de referencia del proyecto es la siguiente:

text
sistema-notas/
│
├── app.py
│
├── config.py
│
├── requirements.txt
│
├── README.md
│
├── models/
│   ├── __init__.py
│   ├── estudiante.py
│   ├── docente.py
│   ├── asignatura.py
│   └── nota.py
│
├── routes/
│   ├── __init__.py
│   ├── estudiantes.py
│   ├── docentes.py
│   ├── asignaturas.py
│   └── notas.py
│
├── templates/
│   ├── base.html
│   │
│   ├── estudiantes/
│   ├── docentes/
│   ├── asignaturas/
│   └── notas/
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
└── database/
    └── sistema_notas.db


Nota: Esta estructura es orientativa. Debe ajustarse a la organización real de los archivos del proyecto.

8. Ejecución de la aplicación

Una vez instaladas las dependencias y configurada la base de datos, ejecutar:

bash
python app.py


Si la aplicación utiliza Flask mediante variables de entorno:

Windows:

bash
set FLASK_APP=app.py
flask run


Linux o macOS:

bash
export FLASK_APP=app.py
flask run


Abrir el navegador e ingresar a:

text
http://127.0.0.1:5000

9. Interfaz del sistema

La aplicación cuenta con una estructura visual organizada en tres secciones principales:

Navbar: presenta el nombre del sistema, identificación del usuario y opción de cerrar sesión.
Sidebar: permite navegar entre los módulos de estudiantes, docentes, asignaturas y notas.
Área de contenido: muestra los formularios, tablas y demás funcionalidades de cada módulo.
10. Seguridad y consideraciones
Validar los datos ingresados en los formularios.
Mantener protegidas las credenciales de acceso.
Configurar correctamente la clave secreta de Flask.
Controlar el acceso a las rutas que requieren autenticación.
Realizar copias de seguridad de la base de datos.
Evitar publicar archivos con información sensible.
11. Mejoras futuras

Entre las funcionalidades que pueden incorporarse en futuras versiones se encuentran:

Administración de usuarios y roles.
Reportes de calificaciones.
Cálculo automático de promedios.
Generación de reportes en PDF y Excel.
Gestión de períodos académicos.
Consulta del historial académico.
Panel estadístico de rendimiento académico.
12. Autor

Proyecto: Sistema de Notas Académicas

Desarrollado con: Python, Flask, Jinja2 y Bootstrap.

Versión: 1.0

© 2026 - Sistema de Notas Académicas.