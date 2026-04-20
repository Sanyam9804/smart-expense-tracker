import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

def get_dummy_data():
    data = [
        {"description": "Starbucks coffee", "category": "Food & Dining"},
        {"description": "McDonalds burger alone", "category": "Food & Dining"},
        {"description": "Grocery shopping at Walmart", "category": "Groceries"},
        {"description": "Monthly rent payment", "category": "Housing"},
        {"description": "Uber ride to airport", "category": "Transportation"},
        {"description": "Gas station fill up", "category": "Transportation"},
        {"description": "Netflix subscription", "category": "Entertainment"},
        {"description": "Movie tickets", "category": "Entertainment"},
        {"description": "Pharmacy meds", "category": "Health"},
        {"description": "Gym membership", "category": "Health"},
        {"description": "Electric bill", "category": "Utilities"},
        {"description": "Water bill", "category": "Utilities"},
        {"description": "Bought a new t-shirt", "category": "Shopping"},
        {"description": "Amazon purchase", "category": "Shopping"},
        {"description": "Salary deposit", "category": "Income"}, # Though expenses usually don't have this, good for robust
    ]
    return pd.DataFrame(data)

def train_and_save_model():
    df = get_dummy_data()
    X = df['description']
    y = df['category']
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', lowercase=True)),
        ('clf', LogisticRegression(random_state=42))
    ])
    
    pipeline.fit(X, y)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_and_save_model()
