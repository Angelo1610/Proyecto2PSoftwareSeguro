import sys
import os
sys.path.append(os.path.abspath("src"))

import subprocess
import requests
from src.utils.classifier import classify

TG_TOKEN = os.environ.get("TG_TOKEN")
TG_CHAT = os.environ.get("TG_CHAT")

# Variables que vienen del workflow (base_ref y head_ref)
BASE = os.environ.get("BASE")
HEAD = os.environ.get("HEAD")

def notify(msg: str):
    if TG_TOKEN and TG_CHAT:
        requests.get(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            params={"chat_id": TG_CHAT, "text": msg}
        )

notify("🔍 Iniciando revisión de seguridad del PR...")

# ============================
# Obtener diff del Pull Request
# ============================
diff_cmd = f"git diff origin/{BASE}...origin/{HEAD}"

diff = subprocess.check_output(
    diff_cmd,
    shell=True,
    stderr=subprocess.STDOUT,
    encoding="utf-8",
    errors="replace"
)

# ============================
# Clasificación con ML
# ============================
prediction, prob, details = classify(diff)

if prediction == "vulnerable":
    notify(f"❌ Código vulnerable detectado. Prob: {prob*100:.2f}%")

    # Crear issue con GH CLI (Linux, ya instalado en Actions)
    subprocess.run([
        "gh", "issue", "create",
        "--title", "⚠ Vulnerabilidad detectada en PR",
        "--body", f"Probabilidad: {prob}\n\nDetalles:\n{details}"
    ])

    raise SystemExit("Vulnerabilidad encontrada. Pipeline detenido.")

notify(f"✔ Código seguro. Prob: {prob*100:.2f}%")
