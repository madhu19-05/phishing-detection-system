# backend/predict.py

import joblib
import pandas as pd

# Load the model
model = joblib.load('models/phishing_model.pkl')

def predict(email_text=None, url=None):
    features = []
    if email_text:
        features = extract_features(pd.DataFrame([{'email_text': email_text}]), 'email')
    elif url:
        features = extract_features(pd.DataFrame([{'url': url}]), 'url')
    
    prediction = model.predict(features)
    return prediction[0]

def extract_features(df, type_):
    features = pd.DataFrame()
    if type_ == 'email':
        features['length'] = df['email_text'].apply(len)
    elif type_ == 'url':
        features['length'] = df['url'].apply(len)
    return features
