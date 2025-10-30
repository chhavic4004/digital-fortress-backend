import os
import pickle

def load_fraud_model():
    model_path = os.path.join('models', 'fraud_model.pkl')
    
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    else:
        return None

def predict_fraud_with_model(model, text):
    if model is None:
        return None
    
    try:
        prediction = model.predict([text])
        probability = model.predict_proba([text])[0][1]
        return {
            'is_fraud': bool(prediction[0]),
            'probability': float(probability)
        }
    except Exception as e:
        print(f"Error making prediction: {e}")
        return None
