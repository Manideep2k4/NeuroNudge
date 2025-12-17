# core/ml/sentiment_model.py

import pandas as pd
import nltk
import pickle
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

nltk.download('stopwords')

# Load dataset
df = pd.read_csv('core/ml/emotion.csv', encoding='latin1', header=None)
df = df[[0, 5]]
df.columns = ['sentiment', 'text']
df['sentiment'] = df['sentiment'].apply(lambda x: 1 if x == 4 else 0)

# Preprocess
stop_words = set(stopwords.words('english'))
df['text'] = df['text'].str.lower().str.replace(r'[^\w\s]', '', regex=True)
df['text'] = df['text'].apply(lambda x: ' '.join(word for word in x.split() if word not in stop_words))

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['sentiment'], test_size=0.2, random_state=42)

# Vectorize
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)

# Train model
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Save vectorizer and model
with open('core/ml/sentiment_pipeline.pkl', 'wb') as f:
    pickle.dump((vectorizer, model), f)

print(" Sentiment model trained and saved successfully.")
