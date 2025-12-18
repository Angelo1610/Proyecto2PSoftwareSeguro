import sys
import os
import subprocess
import requests
import platform
import glob

sys.path.append(os.path.abspath("src"))

from src.utils.classifier import classify

TG_TOKEN = os.environ.get("TG_TOKEN")
TG_CHAT = os.environ.get("TG_CHAT")

# GH CLI path (Windows vs Linux)
GH = r"C:\Program Files\GitHub CLI\gh.exe" if platform.system() == "Windows" else "gh"

def notify(msg: str):
    if TG_TOKEN and TG_CHAT:
        requests.get(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            params={"chat_id": TG_CHAT, "text": msg}
        )

notify("🔍 Iniciando revisión de seguridad del PR...")

# Obtener archivos modificados en el PR
try:
    # Obtener la rama base desde las variables de entorno de GitHub
    base_ref = os.environ.get("GITHUB_BASE_REF", "origin/test")
    
    # Obtener los archivos modificados en el PR
    changed_files = subprocess.check_output(
        f"git diff --name-only origin/{base_ref}...HEAD",
        shell=True,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace"
    ).strip().split("\n")
    
    # Filtrar archivos Python y Java
    python_files = [f for f in changed_files if f.endswith(".py") and os.path.exists(f)]
    java_files = [f for f in changed_files if f.endswith(".java") and os.path.exists(f)]
    
    all_files = python_files + java_files
    
    if not all_files:
        notify("✔ No hay archivos Python o Java modificados")
        sys.exit(0)
    
    notify(f"📝 Analizando {len(python_files)} archivos Python y {len(java_files)} archivos Java...")
    
    # Analizar cada archivo (Python y Java)
    vulnerable_files = []
    
    for file_path in all_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            
            prediction, prob, details = classify(code)
            
            # El modelo devuelve 1 para vulnerable, 0 para safe
            # Umbral reducido a 50% para ser más estricto
            if (prediction == "1" or prediction == 1 or prediction == "vulnerable") and prob > 0.5:
                vulnerable_files.append({
                    "file": file_path,
                    "prob": prob,
                    "details": details
                })
                notify(f"⚠️ {file_path}: {prob*100:.1f}% vulnerable")
        except Exception as e:
            print(f"Error analizando {file_path}: {e}")
    
    # Si hay vulnerabilidades, detener el pipeline
    if vulnerable_files:
        msg = "❌ Vulnerabilidades detectadas:\n\n"
        for item in vulnerable_files:
            msg += f"• {item['file']}: {item['prob']*100:.1f}% vulnerable\n"
            msg += f"  Detalles: {item['details']}\n\n"
        
        notify(msg[:4000])  # Telegram tiene límite de caracteres
        
        # Crear issue en GitHub
        issue_body = f"## ⚠️ Vulnerabilidades Detectadas\n\n"
        for item in vulnerable_files:
            issue_body += f"### 📄 `{item['file']}`\n"
            issue_body += f"- **Probabilidad:** {item['prob']*100:.1f}%\n"
            issue_body += f"- **Detalles:** {item['details']}\n\n"
        
        subprocess.run([
            GH, "issue", "create",
            "--title", "⚠️ Vulnerabilidades detectadas en PR",
            "--body", issue_body
        ], check=False)
        
        raise SystemExit(f"❌ {len(vulnerable_files)} archivo(s) vulnerable(s) detectado(s)")
    
    notify(f"✅ Todos los archivos son seguros")
    
except Exception as e:
    print(f"Error en análisis: {e}")
    notify(f"❌ Error en análisis: {str(e)[:100]}")
    raise
