import requests
import sys

# URL base de API Flask
BASE_URL = 'http://127.0.0.1:5000'

# Uso una sesión de requests para mantener las cookies entre peticiones (para la autenticación)
sesion = requests.Session()

def mostrar_menu():
    print("\n" + "="*30)
    print("SISTEMA DE GESTIÓN DE TAREAS")
    print("="*30)
    print("1. Registrarse")
    print("2. Iniciar Sesión")
    print("3. Ver mis tareas")
    print("4. Salir")
    print("="*30)

def registrarse():
    print("\n--- Registro de Usuario ---")
    usuario = input("Ingrese su nuevo usuario: ")
    contrasena = input("Ingrese su contraseña: ")
    
    url = f"{BASE_URL}/registro"
    datos = {"usuario": usuario, "contraseña": contrasena}
    
    try:
        respuesta = requests.post(url, json=datos)
        datos_resp = respuesta.json()
        if respuesta.status_code == 201:
            print(f"Éxito: {datos_resp['mensaje']}")
        else:
            print(f"Error: {datos_resp.get('error', 'Error desconocido')}")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar con el servidor. ¿Está ejecutándose servidor.py?")

def iniciar_sesion():
    print("\n--- Inicio de Sesión ---")
    usuario = input("Ingrese su usuario: ")
    contrasena = input("Ingrese su contraseña: ")
    
    url = f"{BASE_URL}/login"
    datos = {"usuario": usuario, "contraseña": contrasena}
    
    try:
        # Usamos la sesión para que guarde la cookie si el login es exitoso
        respuesta = sesion.post(url, json=datos)
        datos_resp = respuesta.json()
        if respuesta.status_code == 200:
            print(f"Éxito: {datos_resp['mensaje']}")
        else:
            print(f"Error: {datos_resp.get('error', 'Error desconocido')}")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar con el servidor. ¿Está ejecutándose servidor.py?")

def ver_tareas():
    print("\n--- Mis Tareas ---")
    url = f"{BASE_URL}/tareas"
    
    try:
        # Uso la misma sesión; si hay login exitoso, enviará la cookie automáticamente
        respuesta = sesion.get(url)
        if respuesta.status_code == 200:
            print("Conexión autorizada. Se obtuvo el HTML de tareas:")
            print("-" * 40)
            print(respuesta.text)
            print("-" * 40)
        elif respuesta.status_code == 401:
            datos_resp = respuesta.json()
            print(f" Acceso denegado: {datos_resp.get('error', 'No autorizado')}")
        else:
            print(f"Error inesperado: código {respuesta.status_code}")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar con el servidor. ¿Está ejecutándose servidor.py?")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-4): ")
        
        if opcion == '1':
            registrarse()
        elif opcion == '2':
            iniciar_sesion()
        elif opcion == '3':
            ver_tareas()
        elif opcion == '4':
            print("Saliendo del programa...")
            sys.exit(0)
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()