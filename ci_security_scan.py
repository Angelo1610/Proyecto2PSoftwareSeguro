import os
import subprocess
import requests
from src.utils.classifier import classify

TG_TOKEN = os.environ.get("TG_TOKEN")
TG_CHAT = os.environ.get("TG_CHAT")

def notify(msg: str):
    """Envía mensajes vía Telegram."""
    if TG_TOKEN and TG_CHAT:
        requests.get(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            params={"chat_id": TG_CHAT, "text": msg},
        )

# Leer el diff del PR
diff = subprocess.getoutput("git diff HEAD~1")

notify("🔍 Iniciando revisión de seguridad del PR...")

prediction, prob, details = classify(diff)

if prediction == "vulnerable":
    notify(f"❌ Código vulnerable detectado. Probabilidad: {prob*100:.2f}%")

    # Crear issue automática
    subprocess.run([
        "gh", "issue", "create",
        "--title", "⚠ Vulnerabilidad detectada en PR",
        "--body", f"Probabilidad: {prob}\n\nDetalles:\n{details}"
    ])

    # Fallar pipeline
    raise SystemExit("Vulnerabilidad encontrada. Pipeline detenido.")

notify(f"✔ Código seguro. Probabilidad: {prob*100:.2f}%")
