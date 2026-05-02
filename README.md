Sistema de Gestión de Tareas (PFO 2)

Este proyecto implementa una API REST utilizando **Flask** para el backend y **SQLite** para la base de datos, junto con un cliente interactivo en consola para probar las funcionalidades de registro, inicio de sesión y gestión de tareas.

## Requisitos Previos
Tener instalado Python (recomendado 3.8 o superior).

## Instalación y Ejecución

1. Clonar este repositorio (o descomprimir los archivos).
2. Abrir una terminal en la carpeta del proyecto.
3. Instalar las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
4. Iniciar el servidor:
   ```bash
   python servidor.py
   ```
   *El servidor se ejecutará en `http://127.0.0.1:5000` y creará automáticamente el archivo `database.db` en el mismo directorio la primera vez que se inicie.*

5. Abrir una **segunda terminal** (sin cerrar la primera) y ejecutar el cliente:
   ```bash
   python cliente.py
   ```
6. Sigue las instrucciones del menú interactivo para registrarte, iniciar sesión y ver tus tareas.

---

## Respuestas Conceptuales

### ¿Por qué hashear contraseñas?
Hashear las contraseñas es una medida de seguridad fundamental. Si guardáramos las contraseñas en texto plano (tal cual las ingresa el usuario), cualquier persona que obtenga acceso a la base de datos podría leer las claves de todos los usuarios. Al aplicar una función de "hash" criptográfico (como hace `werkzeug.security` en este proyecto), la contraseña se transforma en una cadena ininteligible. Este proceso es de un solo sentido: es fácil calcular el hash a partir de la contraseña, pero es computacionalmente inviable obtener la contraseña original a partir del hash. De este modo, si la base de datos se ve comprometida, las credenciales reales de los usuarios permanecen protegidas.

### Ventajas de usar SQLite en este proyecto
1. **Sin configuración (Serverless):** No requiere instalar, configurar ni administrar un servidor de base de datos como MySQL o PostgreSQL. 
2. **Portabilidad:** Toda la base de datos se guarda en un único archivo (`database.db`). Esto hace que sea muy sencillo de compartir, copiar o versionar para proyectos académicos.
3. **Integración nativa:** Python incluye el módulo `sqlite3` en su biblioteca estándar, por lo que no es necesario instalar dependencias adicionales a nivel de sistema operativo para conectarse a ella.
4. **Ideal para desarrollo y pruebas:** Es suficientemente rápida y potente para manejar el tráfico de una aplicación pequeña o de entorno de pruebas sin la sobrecarga de un motor de bases de datos completo.

---

## Alojamiento en Github Pages (Aclaración)
> **Nota importante:** Github Pages es un servicio diseñado exclusivamente para alojar contenido **estático** (HTML, CSS y JavaScript ejecutado en el navegador). Dado que este proyecto incluye un backend programado en **Python (Flask)** y requiere acceso a un sistema de archivos para usar **SQLite**, el código del servidor (`servidor.py`) no puede ser "ejecutado" en Github Pages. 
> 