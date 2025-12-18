# Archivo de prueba con múltiples vulnerabilidades para testing del pipeline
import os
import sqlite3

# Vulnerabilidad 1: eval() - Ejecución de código arbitrario
def calcular_resultado(expresion):
    """Función vulnerable que usa eval()"""
    resultado = eval(expresion)  # PELIGRO: eval permite ejecución de código
    return resultado

# Vulnerabilidad 2: exec() - Ejecución de código arbitrario
def ejecutar_comando(codigo):
    """Función vulnerable que usa exec()"""
    exec(codigo)  # PELIGRO: exec ejecuta código Python arbitrario

# Vulnerabilidad 3: os.system() - Inyección de comandos
def listar_archivos(directorio):
    """Función vulnerable que usa os.system()"""
    comando = f"ls {directorio}"
    os.system(comando)  # PELIGRO: permite inyección de comandos

# Vulnerabilidad 4: SQL Injection
def buscar_usuario(nombre):
    """Función vulnerable a SQL Injection"""
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM usuarios WHERE nombre = '{nombre}'"  # PELIGRO: SQL injection
    cursor.execute(query)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# Código de prueba
if __name__ == "__main__":
    print("Este archivo contiene vulnerabilidades intencionales para testing")
    # NO EJECUTAR en producción
