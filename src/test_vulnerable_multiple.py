"""
Archivo con múltiples vulnerabilidades para probar el sistema de detección
"""

def procesar_datos_usuario(input_usuario):
    # Vulnerabilidad 1: uso de eval
    resultado = eval(input_usuario)
    return resultado

def ejecutar_comando(cmd):
    # Vulnerabilidad 2: uso de exec
    exec(cmd)
    
def consulta_bd(user_id):
    # Vulnerabilidad 3: SQL injection
    import sqlite3
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    return cursor.fetchall()

def sistema_operativo(comando):
    # Vulnerabilidad 4: ejecución de comandos del sistema
    import os
    os.system(comando)
    
# Código vulnerable con eval y exec
eval("print('hola')")
exec("import os")
