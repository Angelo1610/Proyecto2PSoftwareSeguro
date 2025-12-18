import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#  Añadido SOLO para activar el pipeline CI/CD
print("codigo seguro")
print("seguro test 1")

from flask import Flask, request, jsonify
from src.utils.classifier import classify

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "status": "online",
        "message": "🚀 Backend de análisis de seguridad corriendo",
        "version": "2.0",
        "endpoints": {
            "scan": "/scan (POST) - Analizar código Java/Python"
        }
    }

@app.route("/scan", methods=["POST"])
def scan_code():
    code = request.json.get("code", "")
    pred, prob, details = classify(code)

    return jsonify({
        "prediction": str(pred),
        "probability": float(prob),
        "details": details
    })

if __name__ == "__main__":
    # Railway usa PORT variable, local usa 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
