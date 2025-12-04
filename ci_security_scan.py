import sys
import os
sys.path.append(os.path.abspath("src"))

import subprocess
import requests
from src.utils.classifier import classify

TG_TOKEN = os.environ.get("TG_TOKEN")
TG_CHAT = os.environ.get("TG_CHAT")

# Ruta absoluta del ejecutable GH CLI
GH = r"C:\Program Files\GitHub CLI\gh.exe"   # ← ESTA ES LA CLAVE

def notify(msg: str):
    """Enviar mensajes por Telegram."""
    if TG_TOKEN and TG_CHAT:
        requests.get(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            params={"chat_id": TG_CHAT, "text": msg}
        )

notify("🔍 Iniciando revisión de seguridad del PR...")

# ---- FIX PARA WINDOWS (UTF-8) ----
diff = subprocess.check_output(
    "git diff HEAD~1",
    shell=True,
    stderr=subprocess.STDOUT,
    encoding="utf-8",
    errors="replace"
)
# -----------------------------------

prediction, prob, details = classify(diff)

if prediction == "vulnerable":
    notify(f"❌ Código vulnerable detectado. Prob: {prob*100:.2f}%")

    # Crear issue automática (usando ruta absoluta)
    subprocess.run([
        GH, "issue", "create",
        "--title", "⚠ Vulnerabilidad detectada en PR",
        "--body", f"Probabilidad: {prob}\n\nDetalles:\n{details}"
    ])

    raise SystemExit("Vulnerabilidad encontrada. Pipeline detenido.")

notify(f"✔ Código seguro. Prob: {prob*100:.2f}%")
