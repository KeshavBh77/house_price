from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load your ML model
model = joblib.load('model.pkl')

# Serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    bedrooms = data.get('bedrooms', 0)
    bathrooms = data.get('bathrooms', 0)
    area = data.get('area', 0)

    prediction = model.predict(np.array([[bedrooms, bathrooms, area]]))[0]

    return jsonify({'price': float(prediction)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)