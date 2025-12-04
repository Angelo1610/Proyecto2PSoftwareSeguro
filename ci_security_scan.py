import sys
import os
import subprocess
import requests
import platform

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

# FIJO Y COMPATIBLE CON GITHUB ACTIONS
diff = subprocess.check_output(
    "git diff HEAD~1",
    shell=True,
    stderr=subprocess.STDOUT,
    encoding="utf-8",
    errors="replace"
)

prediction, prob, details = classify(diff)

if prediction == "vulnerable":
    notify(f"❌ Código vulnerable detectado. Prob: {prob*100:.2f}%")

    subprocess.run([
        GH, "issue", "create",
        "--title", "⚠ Vulnerabilidad detectada en PR",
        "--body", f"Probabilidad: {prob}\n\nDetalles:\n{details}"
    ])

    raise SystemExit("Vulnerabilidad encontrada. Pipeline detenido.")

notify(f"✔ Código seguro. Prob: {prob*100:.2f}%")
