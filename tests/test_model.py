import os
import joblib

def test_model_file_exists():
    assert os.path.exists("model.pkl")

def test_model_loads():
    model = joblib.load("model.pkl")
    assert model is not None