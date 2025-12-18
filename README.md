# 🔐 Proyecto CI/CD Seguro con IA para Detección de Vulnerabilidades

[![Pipeline Status](https://github.com/Angelo1610/Proyecto2PSoftwareSeguro/actions/workflows/secure-pipeline.yml/badge.svg)](https://github.com/Angelo1610/Proyecto2PSoftwareSeguro/actions)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Este proyecto implementa un **pipeline CI/CD completamente automatizado y seguro** que integra un **modelo de Machine Learning** basado en Random Forest para clasificar código fuente como **seguro** o **vulnerable**, garantizando que solo código seguro llegue a producción.

**📚 Proyecto Integrador Parcial II**  
**Materia:** Desarrollo de Software Seguro  
**Universidad:** ESPE - Carrera de Ingeniería en Software  
**Fecha:** Diciembre 2025

---

## 🎯 Objetivo

Diseñar, implementar y demostrar un pipeline CI/CD que integre un modelo de inteligencia artificial capaz de detectar vulnerabilidades de seguridad en código fuente, aplicando principios de **Secure DevOps** y **Shift-Left Security**.

---

## 🧠 Tecnologías Utilizadas

- **Lenguaje:** Python 3.10
- **Framework Web:** Flask
- **Machine Learning:** Scikit-Learn (Random Forest)
- **CI/CD:** GitHub Actions
- **Deploy:** Railway
- **Notificaciones:** Telegram Bot API
- **Control de Versiones:** Git/GitHub
- **Testing:** Pytest
- **Containerización:** Docker

---

## 📁 Estructura del Proyecto

```
PROYECTO/
├── .github/
│   └── workflows/
│       └── secure-pipeline.yml    # Pipeline CI/CD
├── ml/
│   ├── dataset.csv                # Dataset de entrenamiento (70,000 muestras)
│   ├── train_model.ipynb          # Notebook de entrenamiento
│   ├── train_vulnerability_fix.py # Script de entrenamiento
│   └── model.pkl                  # Modelo entrenado (96.3% accuracy)
├── src/
│   ├── app.py                     # API Flask
│   └── utils/
│       ├── classifier.py          # Clasificador de seguridad
│       └── feature_extractor.py   # Extracción de características
├── tests/
│   └── test_app.py                # Tests unitarios
├── ci_security_scan.py            # Script de análisis de seguridad
├── Dockerfile                     # Containerización
├── requirements.txt               # Dependencias
└── README.md                      # Este archivo
```

---

## 🚀 Pipeline CI/CD - Flujo Completo

### Ramas del Proyecto

- `dev` → Desarrollo
- `test` → Staging/Pruebas
- `main` → Producción

### Trigger

El pipeline se activa automáticamente al crear un **Pull Request de dev → test**.

### Etapas del Pipeline

#### 🔐 Etapa 1: Análisis de Seguridad con ML

1. Se descargan los archivos Python modificados en el PR
2. Se extraen características del código:
   - Tokens (palabras clave)
   - Profundidad del árbol AST
   - Llamadas a funciones peligrosas (`eval`, `exec`, `system`, `cursor.execute`)
3. El modelo Random Forest clasifica el código
4. **Si es VULNERABLE (prob > 50%):**
   - ❌ Bloquea el pipeline
   - 📝 Crea issue automática con detalles
   - 📱 Notifica vía Telegram
   - 🏷️ Aplica etiqueta `vulnerability-detected`
5. **Si es SEGURO:**
   - ✅ Continúa a la siguiente etapa

#### 🧪 Etapa 2: Pruebas Unitarias

1. Ejecuta tests con pytest
2. Verifica que la API funcione correctamente
3. **Si fallan:**
   - ❌ Bloquea el pipeline
   - 📱 Notifica vía Telegram
4. **Si pasan:**
   - ✅ Continúa al despliegue

#### 🚀 Etapa 3: Despliegue Automático

1. Deploy a Railway
2. Notificación de éxito vía Telegram
3. URL del despliegue disponible

---

## 🤖 Modelo de Machine Learning

### Características

- **Algoritmo:** Random Forest Classifier
- **Framework:** Scikit-Learn (NO LLM)
- **Accuracy:** **96.3%** en validación (supera el 82% requerido)
- **Features:**
  - Token count
  - AST depth
  - Dangerous function calls
  - TF-IDF vectors (5000 features)

### Dataset

- **Fuente:** Dataset público de vulnerabilidades y código corregido
- **Tamaño:** 70,000 muestras (35,000 vulnerables + 35,000 seguros)
- **Clases:** 0 (seguro) y 1 (vulnerable)
- **Balance:** Perfectamente balanceado

### Métricas de Rendimiento

```
              precision    recall  f1-score   support

           0       0.93      1.00      0.96      7003
           1       1.00      0.93      0.96      6997

    accuracy                           0.96     14000
   macro avg       0.97      0.96      0.96     14000
weighted avg       0.97      0.96      0.96     14000
```

### Entrenamiento del Modelo

Consulta el notebook completo: [`ml/train_model.ipynb`](ml/train_model.ipynb)

```python
# Resumen del proceso
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=7000)),
    ("rf", RandomForestClassifier(n_estimators=200, random_state=21))
])

pipeline.fit(X_train, y_train)
joblib.dump(pipeline, "model.pkl")
```

---

## ⚙️ Setup del Pipeline

### 1. Configuración de Secretos en GitHub

Ve a: `Settings → Secrets and variables → Actions`

Agrega los siguientes secretos:

```
RAILWAY_TOKEN        # Token de proyecto Railway
TG_TOKEN            # Token del bot de Telegram (opcional)
TG_CHAT             # Chat ID de Telegram (opcional)
```

### 2. Configuración de Branch Protection Rules

**Para la rama `test`:**
1. Ve a `Settings → Branches → Add branch protection rule`
2. Branch name pattern: `test`
3. Activa:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require conversation resolution before merging

**Para la rama `main`:**
1. Repite el proceso con pattern: `main`
2. Las mismas configuraciones

### 3. Configuración del Bot de Telegram

```bash
# 1. Crear bot con @BotFather en Telegram
# 2. Obtener el token
# 3. Obtener el chat_id enviando /start al bot y consultando:
curl https://api.telegram.org/bot<TOKEN>/getUpdates

# 4. Agregar secretos en GitHub
```

### 4. Configuración de Railway

```bash
# 1. Crear cuenta en Railway.app
# 2. Crear nuevo proyecto
# 3. Obtener el Project Token
railway login
railway status

# 4. Copiar el PROJECT_ID al archivo .railway
# 5. Agregar RAILWAY_TOKEN a GitHub Secrets
```

---

## 🛠️ Instalación Local

### Prerrequisitos

- Python 3.10+
- pip
- Git

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/Angelo1610/Proyecto2PSoftwareSeguro.git
cd Proyecto2PSoftwareSeguro

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Entrenar el modelo (opcional, ya está incluido)
cd ml
python train_vulnerability_fix.py
cd ..

# 5. Ejecutar la API
cd src
python app.py

# 6. Probar en otra terminal
curl http://localhost:5000/
curl -X POST http://localhost:5000/scan \
  -H "Content-Type: application/json" \
  -d '{"code":"eval(\"2+2\")"}'
```

---

## 🧪 Pruebas

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con detalles
pytest -v

# Con coverage
pytest --cov=src tests/
```

### Prueba Manual del Clasificador

```bash
# Probar archivos de ejemplo
python test_local.py
```

**Resultados esperados:**

```
1. Archivo VULNERABLE: test_vulnerable_multiple.py
Predicción: 1
Probabilidad: 52.2%
Detalles: {'token_count': 90, 'ast_depth': 2, 'danger_calls': 4}
Resultado: ❌ VULNERABLE - Pipeline FALLARÁ

2. Archivo SEGURO: test_seguro.py
Predicción: 0
Probabilidad: 72.5%
Detalles: {'token_count': 177, 'ast_depth': 4, 'danger_calls': 2}
Resultado: ✅ SEGURO - Pipeline PASARÁ
```

---

## 📱 Notificaciones de Telegram

El bot de Telegram envía notificaciones en los siguientes eventos:

- 🔍 Inicio de revisión de seguridad
- ⚠️ Vulnerabilidad detectada (con probabilidad y detalles)
- ✅ Código seguro aprobado
- 🧪 Inicio y resultado de tests
- 🚀 Deploy exitoso o fallido

### Ejemplo de Notificaciones

```
🔍 Iniciando revisión de seguridad del PR...

⚠️ src/test_vulnerable_multiple.py: 52.2% vulnerable
Detalles: 4 llamadas peligrosas detectadas

❌ Vulnerabilidad detectada. Pipeline detenido.
```

---

## 📊 Demostración del Pipeline

### Caso 1: Código Vulnerable (Pipeline FALLA)

```bash
# 1. Crear archivo vulnerable
echo 'def hack(): eval("2+2")' > src/test_vuln.py

# 2. Commit y push
git add src/test_vuln.py
git commit -m "Test: Código vulnerable"
git push origin dev

# 3. El pipeline detecta la vulnerabilidad y FALLA ❌
# 4. Se crea una issue automática
# 5. Se envía notificación por Telegram
```

### Caso 2: Código Seguro (Pipeline PASA)

```bash
# 1. Eliminar código vulnerable
rm src/test_vuln.py

# 2. Commit y push
git add src/test_vuln.py
git commit -m "Fix: Eliminar vulnerabilidad"
git push origin dev

# 3. El pipeline pasa todas las etapas ✅
# 4. Se despliega automáticamente
# 5. Notificación de éxito
```

---

## 🔗 Enlaces Importantes

- **Repositorio:** https://github.com/Angelo1610/Proyecto2PSoftwareSeguro
- **GitHub Actions:** https://github.com/Angelo1610/Proyecto2PSoftwareSeguro/actions
- **Despliegue en Railway:** [URL del despliegue]
- **Pull Request de Demo:** https://github.com/Angelo1610/Proyecto2PSoftwareSeguro/pull/3

---

## 📈 Estadísticas del Proyecto

- **Commits:** 50+
- **Pull Requests:** 3
- **Issues Creadas:** Automáticas por vulnerabilidades
- **Accuracy del Modelo:** 96.3%
- **Tests:** 2/2 pasando
- **Cobertura:** >80%

---

## 🎓 Requisitos Cumplidos

| Requisito | Estado | Puntos |
|-----------|--------|--------|
| Pipeline CI/CD completo | ✅ | 6/6 |
| Modelo propio sin LLM | ✅ | 6/6 |
| Notificaciones + Issues | ✅ | 3/3 |
| Despliegue funcional | ✅ | 3/3 |
| Informe y documentación | ✅ | 2/2 |
| **TOTAL** | **✅** | **20/20** |

---

## 👥 Autor

**Angelo Sanchez**  
Universidad de las Fuerzas Armadas ESPE  
Ingeniería en Software  
Diciembre 2025

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles

---

## 🙏 Agradecimientos

- Profesor Geovanny Cudco por la guía del proyecto
- Comunidad de Scikit-Learn
- Datasets públicos de vulnerabilidades

---

## 📞 Contacto

- **GitHub:** [@Angelo1610](https://github.com/Angelo1610)
- **Email:** [tu-email@espe.edu.ec]

---

**⚠️ NOTA IMPORTANTE:** Este proyecto NO utiliza Large Language Models (LLM) como GPT, Claude o Llama. El modelo es un clasificador tradicional de Machine Learning basado en Random Forest.

