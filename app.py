from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load trained model
MODEL_PATH = "model.pkl"

if not os.path.exists(MODEL_PATH):
    raise RuntimeError("model.pkl not found. Did you train the model before running the app?")

model = joblib.load(MODEL_PATH)

@app.route("/", methods=["GET"])
def home():
    """Root endpoint to check if API is running"""
    return jsonify({"message": "House Price Prediction API is running"}), 200

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    """Predict house price from features"""
    try:
        data = request.json.get("features")
        if data is None:
            return jsonify({"error": "No features provided"}), 400

        # Convert input to numpy array and reshape
        features = np.array(data).reshape(1, -1)
        prediction = model.predict(features)

        return jsonify({"predicted_house_price": float(prediction[0])}), 200

    except ValueError as ve:
        return jsonify({"error": f"Invalid input shape or type: {ve}"}), 400
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {e}"}), 500

if __name__ == "__main__":
    # Use 0.0.0.0 to allow Docker to bind the port
    app.run(host="0.0.0.0", port=5001, debug=True)