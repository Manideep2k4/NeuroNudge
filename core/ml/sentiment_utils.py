# core/ml/sentiment_utils.py

import pickle
import re

# Load the saved vectorizer and model
with open('core/ml/sentiment_pipeline.pkl', 'rb') as f:
    vectorizer, model = pickle.load(f)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def predict_sentiment(text):
    cleaned = preprocess_text(text)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]


    if prediction == 1:
        return "positive"
    elif prediction == 0:
        return "negative"
    else:
        return "unknown"
