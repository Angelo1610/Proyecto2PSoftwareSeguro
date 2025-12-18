import sys
sys.path.append('src')
from src.utils.classifier import classify
import os

print("\n" + "="*70)
print("ANÁLISIS LOCAL DE ARCHIVOS JAVA")
print("="*70)

java_files = [f for f in os.listdir('java_tests') if f.endswith('.java')]
print(f"\nArchivos encontrados: {len(java_files)}\n")

for file in java_files:
    with open(f'java_tests/{file}', 'r', encoding='utf-8') as f:
        code = f.read()
    
    pred, prob, details = classify(code)
    
    print(f"📄 {file}")
    print(f"   Predicción: {pred}")
    print(f"   Probabilidad: {prob*100:.1f}%")
    print(f"   Tokens: {details['token_count']}")
    print(f"   Funciones peligrosas: {details['danger_calls']}")
    
    if str(pred) == "1" and prob > 0.5:
        print(f"   ❌ VULNERABLE")
    else:
        print(f"   ✅ SEGURO")
    print()

print("="*70)
