from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model
model = joblib.load("model.pkl")

@app.route("/health", methods=["GET"])
def health():
    return {"status": "healthy"}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json.get("features")

    if not data:
        return jsonify({"error": "No features provided"}), 400

    features = np.array(data).reshape(1, -1)
    prediction = model.predict(features)

    return jsonify({
        "predicted_house_price": float(prediction[0])
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)