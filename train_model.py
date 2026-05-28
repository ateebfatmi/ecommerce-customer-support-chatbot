import pandas as pd
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
data = pd.read_csv("training_data.csv")

# Features (questions/messages)
X = data["text"]

# Labels (intents)
y = data["intent"]

# Convert text into vectors
vectorizer = CountVectorizer()

X_vectorized = vectorizer.fit_transform(X)

# Create Logistic Regression model
model = LogisticRegression()

# Train model
model.fit(X_vectorized, y)

# Save trained model
with open("chatbot_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

# Save vectorizer
with open("vectorizer.pkl", "wb") as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

print("Model trained successfully")