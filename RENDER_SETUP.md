# 🚀 CONFIGURAR RENDER PARA DEPLOYMENT

## Paso 1: Crear cuenta en Render

1. Ve a: https://render.com/
2. Haz clic en **"Get Started"**
3. Conéctate con tu cuenta de GitHub

---

## Paso 2: Crear Web Service

1. En el Dashboard de Render, haz clic en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio: `Angelo1610/Proyecto2PSoftwareSeguro`
4. Haz clic en **"Connect"**

---

## Paso 3: Configurar el servicio

**Name:** `proyecto-seguridad-backend`

**Branch:** `test` (o `main` si quieres deploy de main)

**Root Directory:** *(dejar vacío)*

**Environment:** `Python 3`

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn --bind 0.0.0.0:$PORT wsgi:app
```

**Instance Type:** `Free`

---

## Paso 4: Variables de Entorno (Opcional)

Si necesitas variables:
- `PYTHON_VERSION` = `3.10.0`

---

## Paso 5: Deploy

1. Haz clic en **"Create Web Service"**
2. Render automáticamente:
   - Clonará tu repo
   - Instalará dependencias
   - Iniciará el servidor
3. **Espera 3-5 minutos** para el primer deploy

---

## Paso 6: Obtener la URL

Cuando termine el deploy:
1. Verás la URL en la parte superior: `https://proyecto-seguridad-backend.onrender.com`
2. Copia esa URL

**Probar:**
```powershell
Invoke-RestMethod https://proyecto-seguridad-backend.onrender.com/
```

Deberías ver:
```json
{
  "status": "online",
  "message": "🚀 Backend de análisis de seguridad corriendo",
  "version": "2.0",
  ...
}
```

---

## Paso 7: Deploy Hook para GitHub Actions (Opcional)

1. En Render, ve a **Settings** del servicio
2. Scroll hasta **"Deploy Hook"**
3. Copia la URL del webhook
4. En GitHub:
   - Ve a: Settings → Secrets and variables → Actions
   - Crea nuevo secret: `RENDER_DEPLOY_HOOK`
   - Pega la URL del webhook

Ahora cada PR que pase tests desplegará automáticamente a Render 🚀

---

## 🎯 Ventajas de Render vs Railway

✅ Más confiable
✅ Mejor logging
✅ No requiere configuración de puertos
✅ Deploy automático desde GitHub
✅ Free tier más generoso

---

## ⚠️ Nota Importante

El primer deploy puede tardar **5-10 minutos** porque:
1. Render instala todas las dependencias
2. scikit-learn es pesado (~200MB)
3. Compila modelos de ML

**Después de eso, los deploys son mucho más rápidos (~2-3 min)**
