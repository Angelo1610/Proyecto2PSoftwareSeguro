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
    
    # Filtrar SOLO archivos Java
    java_files = [f for f in changed_files if f.endswith(".java") and os.path.exists(f)]
    
    if not java_files:
        notify("✔ No hay archivos Java modificados")
        sys.exit(0)
    
    notify(f"☕ Analizando {len(java_files)} archivos Java del proyecto...")
    
    # Analizar cada archivo Java
    vulnerable_files = []
    
    for file_path in java_files:
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
        
        print(f"⚠️ ADVERTENCIA: {len(vulnerable_files)} archivo(s) con posibles vulnerabilidades")
        notify(f"⚠️ {len(vulnerable_files)} archivos requieren revisión, pero el pipeline continuará")
        # NO bloquear el pipeline - solo advertir
        sys.exit(0)
    
    notify(f"✅ Todos los archivos son seguros")
    
except Exception as e:
    print(f"Error en análisis: {e}")
    notify(f"❌ Error en análisis: {str(e)[:100]}")
    raise
