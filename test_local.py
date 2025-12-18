import sys
sys.path.append('src')
from src.utils.classifier import classify

print("=" * 70)
print("PRUEBA LOCAL DEL CLASIFICADOR DE SEGURIDAD")
print("=" * 70)

# Probar archivo vulnerable
print("\n1. Archivo VULNERABLE: test_vulnerable_multiple.py")
print("-" * 70)
with open('src/test_vulnerable_multiple.py', 'r', encoding='utf-8') as f:
    code_vulnerable = f.read()

pred, prob, details = classify(code_vulnerable)
print(f'Predicción: {pred}')
print(f'Probabilidad: {prob*100:.1f}%')
print(f'Detalles: {details}')
if str(pred) == "1" and prob > 0.5:
    print('Resultado:  VULNERABLE - Pipeline FALLARÁ')
else:
    print('Resultado:  SEGURO - Pipeline PASARÁ')

# Probar archivo seguro
print("\n2. Archivo SEGURO: test_seguro.py")
print("-" * 70)
with open('src/test_seguro.py', 'r', encoding='utf-8') as f:
    code_seguro = f.read()

pred, prob, details = classify(code_seguro)
print(f'Predicción: {pred}')
print(f'Probabilidad: {prob*100:.1f}%')
print(f'Detalles: {details}')
if str(pred) == "1" and prob > 0.5:
    print('Resultado:  VULNERABLE - Pipeline FALLARÁ')
else:
    print('Resultado:  SEGURO - Pipeline PASARÁ')

print("\n" + "=" * 70)
