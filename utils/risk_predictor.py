import joblib
import numpy as np
import os

model_path = os.path.join(os.path.dirname(__file__), '..', 'ml_model', 'final_RFC_model_87.pkl')
model_path = os.path.abspath(model_path)
model = None

try:
    model = joblib.load(model_path)
except (FileNotFoundError, Exception):
    model = None
    
def predict_risk(features):
    if model is None:
        raise ValueError("Model is not loaded. Cannot make predictions.")
    
    features_order = ['Age', 'Sex', 'Chest pain type', 'BP', 'Cholesterol', 
                     'FBS over 120', 'Max HR', 'Exercise angina']
    
    input_data = [features[col] for col in features_order]
    input_array = np.array(input_data).reshape(1, -1)
    
    prediction = model.predict(input_array)[0]
    proba = model.predict_proba(input_array)[0][1]
    return prediction, proba