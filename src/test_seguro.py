"""
Archivo con código seguro para probar el sistema de detección
"""

def procesar_datos_seguros(datos):
    """Procesa datos de manera segura usando funciones estándar"""
    resultado = []
    for item in datos:
        if isinstance(item, (int, float)):
            resultado.append(item * 2)
        elif isinstance(item, str):
            resultado.append(item.strip().upper())
    return resultado

def consulta_bd_segura(user_id):
    """Consulta base de datos usando parámetros preparados"""
    import sqlite3
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    # Uso seguro con parámetros
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

def leer_archivo_seguro(ruta):
    """Lee archivos de manera segura con manejo de excepciones"""
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
        return contenido
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def calcular_estadisticas(numeros):
    """Calcula estadísticas básicas de una lista"""
    if not numeros:
        return None
    
    return {
        'suma': sum(numeros),
        'promedio': sum(numeros) / len(numeros),
        'maximo': max(numeros),
        'minimo': min(numeros)
    }

# Uso de funciones seguras
datos = [1, 2, 3, 4, 5]
resultado = procesar_datos_seguros(datos)
print(f"Resultado: {resultado}")

estadisticas = calcular_estadisticas([10, 20, 30, 40])
print(f"Estadísticas: {estadisticas}")
