from flask import Flask, request, jsonify
from utils.classifier import classify

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "API funcionando"}

@app.route("/scan", methods=["POST"])
def scan_code():
    code = request.json.get("code", "")
    pred, prob, details = classify(code)

    return jsonify({
        "prediction": pred,
        "probability": prob,
        "details": details
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
