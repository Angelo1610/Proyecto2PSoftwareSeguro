"""
Script para analizar archivos Java de cualquier proyecto
"""
import sys
import os
from pathlib import Path
sys.path.append('src')
from src.utils.classifier import classify

def analizar_proyecto_java(ruta_proyecto):
    """Analiza todos los archivos .java en un proyecto"""
    
    ruta = Path(ruta_proyecto)
    if not ruta.exists():
        print(f"❌ Error: La ruta '{ruta_proyecto}' no existe")
        return
    
    archivos_java = list(ruta.rglob('*.java'))
    
    if not archivos_java:
        print(f"⚠️ No se encontraron archivos Java en '{ruta_proyecto}'")
        return
    
    print("=" * 80)
    print(f"🔍 ANÁLISIS DE SEGURIDAD - Proyecto Java")
    print("=" * 80)
    print(f"📁 Ruta: {ruta.absolute()}")
    print(f"📄 Archivos .java encontrados: {len(archivos_java)}")
    print("=" * 80)
    
    vulnerables = []
    seguros = []
    errores = []
    
    for idx, archivo in enumerate(archivos_java, 1):
        try:
            print(f"\r⏳ Analizando... {idx}/{len(archivos_java)}", end='', flush=True)
            
            with open(archivo, 'r', encoding='utf-8') as f:
                codigo = f.read()
            
            pred, prob, details = classify(codigo)
            
            # Determinar si es vulnerable (predicción = 1 y probabilidad > 50%)
            es_vulnerable = (str(pred) == "1") and (prob > 0.5)
            
            if es_vulnerable:
                vulnerables.append({
                    'archivo': archivo.relative_to(ruta),
                    'prob': prob,
                    'details': details
                })
            else:
                seguros.append({
                    'archivo': archivo.relative_to(ruta),
                    'prob': prob
                })
                
        except Exception as e:
            errores.append({
                'archivo': archivo.relative_to(ruta),
                'error': str(e)
            })
    
    print("\r" + " " * 50 + "\r", end='')  # Limpiar línea de progreso
    
    # Mostrar resultados
    print(f"\n{'='*80}")
    print("📊 RESULTADOS DEL ANÁLISIS")
    print("=" * 80)
    
    if vulnerables:
        print(f"\n❌ ARCHIVOS VULNERABLES ({len(vulnerables)}):")
        print("-" * 80)
        for item in sorted(vulnerables, key=lambda x: x['prob'], reverse=True):
            print(f"\n📄 {item['archivo']}")
            print(f"   🎯 Probabilidad vulnerable: {item['prob']*100:.1f}%")
            print(f"   📋 Tokens: {item['details']['token_count']}")
            print(f"   🌳 AST Depth: {item['details']['ast_depth']}")
            print(f"   ⚠️  Funciones peligrosas detectadas: {item['details']['danger_calls']}")
            
            # Recomendación basada en probabilidad
            if item['prob'] > 0.8:
                print(f"   🚨 CRÍTICO: Revisar inmediatamente")
            elif item['prob'] > 0.6:
                print(f"   ⚠️  ALTO: Revisar pronto")
            else:
                print(f"   ⚡ MEDIO: Considerar revisión")
    else:
        print("\n✅ No se detectaron archivos con vulnerabilidades críticas")
    
    if seguros:
        print(f"\n✅ ARCHIVOS SEGUROS ({len(seguros)}):")
        print("-" * 80)
        for item in seguros[:10]:  # Mostrar solo los primeros 10
            prob_seguro = (1 - item['prob']) * 100
            print(f"   📄 {item['archivo']} - {prob_seguro:.1f}% seguro")
        if len(seguros) > 10:
            print(f"   ... y {len(seguros)-10} archivos seguros más")
    
    if errores:
        print(f"\n⚠️ ERRORES AL ANALIZAR ({len(errores)}):")
        print("-" * 80)
        for item in errores[:5]:
            print(f"   📄 {item['archivo']}: {item['error']}")
        if len(errores) > 5:
            print(f"   ... y {len(errores)-5} errores más")
    
    print(f"\n{'='*80}")
    print("📈 RESUMEN FINAL")
    print("=" * 80)
    print(f"   Total archivos Java: {len(archivos_java)}")
    print(f"   ✅ Seguros: {len(seguros)} ({len(seguros)/len(archivos_java)*100:.1f}%)")
    print(f"   ❌ Vulnerables: {len(vulnerables)} ({len(vulnerables)/len(archivos_java)*100:.1f}%)")
    if errores:
        print(f"   ⚠️ Errores: {len(errores)}")
    
    porcentaje_seguro = (len(seguros) / len(archivos_java) * 100) if archivos_java else 0
    
    print(f"\n   🎯 Seguridad del proyecto: {porcentaje_seguro:.1f}%")
    
    if porcentaje_seguro >= 90:
        print("   ✅ Estado: EXCELENTE")
    elif porcentaje_seguro >= 70:
        print("   ⚠️ Estado: BUENO - Algunas mejoras recomendadas")
    elif porcentaje_seguro >= 50:
        print("   ⚠️ Estado: REGULAR - Se recomienda revisión")
    else:
        print("   🚨 Estado: CRÍTICO - Requiere atención inmediata")
    
    print("=" * 80)
    
    # Exportar reporte si hay vulnerabilidades
    if vulnerables:
        print(f"\n💾 Exportando reporte detallado...")
        with open('reporte_vulnerabilidades.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("REPORTE DE VULNERABILIDADES DETECTADAS\n")
            f.write("=" * 80 + "\n\n")
            for item in sorted(vulnerables, key=lambda x: x['prob'], reverse=True):
                f.write(f"Archivo: {item['archivo']}\n")
                f.write(f"Probabilidad: {item['prob']*100:.1f}%\n")
                f.write(f"Tokens: {item['details']['token_count']}\n")
                f.write(f"AST Depth: {item['details']['ast_depth']}\n")
                f.write(f"Funciones peligrosas: {item['details']['danger_calls']}\n")
                f.write("-" * 80 + "\n\n")
        print(f"✅ Reporte guardado en: reporte_vulnerabilidades.txt")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("=" * 80)
        print("🔍 ANALIZADOR DE SEGURIDAD PARA PROYECTOS JAVA")
        print("=" * 80)
        print("\nUso: python analizar_java.py <ruta_al_proyecto>\n")
        print("Ejemplos:")
        print('  python analizar_java.py "C:\\MiProyecto\\src"')
        print('  python analizar_java.py "C:\\Users\\sanch\\OneDrive\\Documentos\\SEPTIMO\\Distribuidas\\ms-clientes"')
        print('  python analizar_java.py .')
        print("\n" + "=" * 80)
    else:
        ruta_proyecto = sys.argv[1]
        analizar_proyecto_java(ruta_proyecto)
