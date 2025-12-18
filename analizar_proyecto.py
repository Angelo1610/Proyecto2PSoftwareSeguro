"""
Script para analizar archivos Python de cualquier proyecto
"""
import sys
import os
from pathlib import Path
sys.path.append('src')
from src.utils.classifier import classify

def analizar_proyecto(ruta_proyecto):
    """Analiza todos los archivos .py en un proyecto"""
    
    ruta = Path(ruta_proyecto)
    if not ruta.exists():
        print(f"❌ Error: La ruta '{ruta_proyecto}' no existe")
        return
    
    archivos_py = list(ruta.rglob('*.py'))
    
    if not archivos_py:
        print(f"⚠️ No se encontraron archivos Python en '{ruta_proyecto}'")
        return
    
    print("=" * 80)
    print(f"🔍 ANÁLISIS DE SEGURIDAD - Proyecto: {ruta.name}")
    print("=" * 80)
    print(f"📁 Ruta: {ruta.absolute()}")
    print(f"📄 Archivos encontrados: {len(archivos_py)}")
    print("=" * 80)
    
    vulnerables = []
    seguros = []
    errores = []
    
    for archivo in archivos_py:
        try:
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
    
    # Mostrar resultados
    print(f"\n{'='*80}")
    print("📊 RESULTADOS DEL ANÁLISIS")
    print("=" * 80)
    
    if vulnerables:
        print(f"\n❌ ARCHIVOS VULNERABLES ({len(vulnerables)}):")
        print("-" * 80)
        for item in vulnerables:
            print(f"\n📄 {item['archivo']}")
            print(f"   🎯 Probabilidad vulnerable: {item['prob']*100:.1f}%")
            print(f"   📋 Tokens: {item['details']['token_count']}")
            print(f"   🌳 AST Depth: {item['details']['ast_depth']}")
            print(f"   ⚠️  Funciones peligrosas: {item['details']['danger_calls']}")
    else:
        print("\n✅ No se detectaron archivos vulnerables")
    
    if seguros:
        print(f"\n✅ ARCHIVOS SEGUROS ({len(seguros)}):")
        print("-" * 80)
        for item in seguros[:5]:  # Mostrar solo los primeros 5
            print(f"   📄 {item['archivo']} - Seguro ({(1-item['prob'])*100:.1f}%)")
        if len(seguros) > 5:
            print(f"   ... y {len(seguros)-5} archivos más")
    
    if errores:
        print(f"\n⚠️ ERRORES AL ANALIZAR ({len(errores)}):")
        print("-" * 80)
        for item in errores:
            print(f"   📄 {item['archivo']}: {item['error']}")
    
    print(f"\n{'='*80}")
    print("📈 RESUMEN FINAL")
    print("=" * 80)
    print(f"   Total archivos: {len(archivos_py)}")
    print(f"   ✅ Seguros: {len(seguros)}")
    print(f"   ❌ Vulnerables: {len(vulnerables)}")
    print(f"   ⚠️ Errores: {len(errores)}")
    
    porcentaje_seguro = (len(seguros) / len(archivos_py) * 100) if archivos_py else 0
    print(f"\n   🎯 Seguridad del proyecto: {porcentaje_seguro:.1f}%")
    print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python analizar_proyecto.py <ruta_al_proyecto>")
        print("\nEjemplos:")
        print("  python analizar_proyecto.py C:\\MiProyecto\\src")
        print("  python analizar_proyecto.py ../OtroProyecto")
        print("  python analizar_proyecto.py .")
    else:
        ruta_proyecto = sys.argv[1]
        analizar_proyecto(ruta_proyecto)
