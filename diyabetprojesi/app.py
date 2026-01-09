from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os




app = Flask(__name__)
CORS(app)



# Ana sayfa → risk.html
@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "risk.html")

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    age = data.get("age", 0)
    glucose = data.get("glucose", 0)
    hba1c = data.get("hba1c", 0)
    bmi = data.get("bmi", 0)
    diabetes = data.get("diabetes", 0)

    # ✅ GERÇEK sayısal risk hesabı (deterministik)
    risk_score = (
        age * 0.01 +
        glucose * 0.003 +
        hba1c * 0.1 +
        bmi * 0.02 +
        diabetes * 0.2
    )

    risk_score = max(0, min(risk_score / 6, 1))

    return jsonify({
        "results": [{
            "heart_disease_pred": int(risk_score > 0.5),
            "risk_score": round(float(risk_score), 3)
        }]
    })

if __name__ == "__main__":
    app.run(debug=True)
