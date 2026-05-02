import sqlite3
from flask import Flask, request, jsonify, session, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
# Usamos una clave secreta para firmar las cookies de sesión
app.secret_key = "secreto_super_seguro_pfo2"

DATABASE = "database.db"

def init_db():
    """Inicializa la base de datos creando la tabla de usuarios si no existe."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contrasena_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    if not datos or not 'usuario' in datos or not 'contraseña' in datos:
        return jsonify({"error": "Faltan datos (usuario y contraseña requeridos)"}), 400

    usuario = datos['usuario']
    contrasena = datos['contraseña']
    
    # Hasheamos la contraseña
    contrasena_hash = generate_password_hash(contrasena)

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)', (usuario, contrasena_hash))
            conn.commit()
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    if not datos or not 'usuario' in datos or not 'contraseña' in datos:
        return jsonify({"error": "Faltan datos (usuario y contraseña requeridos)"}), 400

    usuario = datos['usuario']
    contrasena = datos['contraseña']

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT contrasena_hash FROM usuarios WHERE usuario = ?', (usuario,))
        resultado = cursor.fetchone()

    if resultado and check_password_hash(resultado[0], contrasena):
        # Guardamos el usuario en la sesión para que pueda acceder a /tareas
        session['usuario'] = usuario
        return jsonify({"mensaje": "Inicio de sesión exitoso"}), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

@app.route('/tareas', methods=['GET'])
def tareas():
    # Verificamos si el usuario tiene una sesión activa
    if 'usuario' not in session:
        return jsonify({"error": "No autorizado. Por favor inicie sesión."}), 401
    
    usuario = session['usuario']
    
    # Plantilla HTML básica de bienvenida (podría estar en un archivo separado)
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mis Tareas</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f9; padding: 50px; text-align: center; }}
            .container {{ background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; }}
            h1 {{ color: #333; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ background: #eee; margin: 10px 0; padding: 10px; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Bienvenido a tus tareas, {usuario}</h1>
            <p>Aquí tienes tu lista de cosas por hacer:</p>
            <ul>
                <li>Terminar la API Flask 🚀</li>
                <li>Hacer la documentación 📝</li>
                <li>Aprobar la materia 🎉</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    # Inicializamos la base de datos al arrancar
    init_db()
    # Ejecutamos el servidor
    app.run(debug=True, port=5000)