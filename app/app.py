import hashlib
import json
import logging

import joblib
import pandas as pd
from flask import Flask, jsonify, request

from app.config import Config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = joblib.load(Config.MODEL_PATH)
prediction_cache = {}
app = Flask(__name__)

logger.info("Model path: %s", Config.MODEL_PATH)
logger.info("Port: %s", Config.PORT)
logger.info("Cache enabled: %s", Config.CACHE_ENABLED)
logger.info("High threshold: %s", Config.HIGH_THRESHOLD)
logger.info("Medium threshold: %s", Config.MEDIUM_THRESHOLD)
logger.info("Model type: %s", type(model).__name__)


def cache_key(data):
    serialized = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


@app.get("/")
def home():
    return jsonify(
        {
            "project": "Alumni Donor Propensity Forecaster",
            "status": "API is running",
            "endpoint": "/predict",
            "method": "POST",
        }
    )


@app.get("/api-info")
def api_info():
    return jsonify(
        {
            "project": "Alumni Donor Propensity Forecaster",
            "model": "Random Forest Classifier",
            "target": "Is_Donor_2025",
            "prediction_values": ["Yes", "No"],
            "propensity_categories": ["High", "Medium", "Low"],
            "prediction_endpoint": "/predict",
            "prediction_method": "POST",
        }
    )


@app.get("/config")
def config_info():
    return jsonify(
        {
            "port": Config.PORT,
            "model_path": Config.MODEL_PATH,
            "cache_enabled": Config.CACHE_ENABLED,
            "high_threshold": Config.HIGH_THRESHOLD,
            "medium_threshold": Config.MEDIUM_THRESHOLD,
        }
    )


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must contain JSON data."}), 400

    key = cache_key(data)
    if Config.CACHE_ENABLED and key in prediction_cache:
        return jsonify(prediction_cache[key])

    try:
        input_data = pd.DataFrame([data])
        prediction = model.predict(input_data)[0]
        probability = float(model.predict_proba(input_data)[0][1])
        propensity_score = probability * 100

        if propensity_score >= Config.HIGH_THRESHOLD:
            category = "High"
            interpretation = "Likely to Donate"
        elif propensity_score >= Config.MEDIUM_THRESHOLD:
            category = "Medium"
            interpretation = "Moderate Donation Propensity"
        else:
            category = "Low"
            interpretation = "Less Likely to Donate"

        result = {
            "prediction": "Yes" if prediction == 1 else "No",
            "donation_probability": round(probability, 4),
            "propensity_score": round(propensity_score, 2),
            "category": category,
            "interpretation": interpretation,
        }
        if Config.CACHE_ENABLED:
            prediction_cache[key] = result
        return jsonify(result)
    except Exception as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT)