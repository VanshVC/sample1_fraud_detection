import pandas as pd
import numpy as np
import joblib
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score, confusion_matrix

# Directories
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BACKEND_DIR, "data", "credit_card_fraud.csv")
MODELS_DIR = os.path.join(BACKEND_DIR, "models")
METRICS_PATH = os.path.join(BACKEND_DIR, "evaluation", "metrics.json")

# Ensure models directory exists
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(METRICS_PATH), exist_ok=True)

def train_and_evaluate():
    print(f"🚀 Starting Model Training (from {DATA_PATH})...")

    # 1. Load Data
    try:
        df = pd.read_csv(DATA_PATH)
        print(f"✅ Data Loaded: {df.shape}")
    except FileNotFoundError:
        print(f"❌ Error: Data file not found at {DATA_PATH}")
        return

    # 2. Preprocessing
    le_category = LabelEncoder()
    df['category'] = le_category.fit_transform(df['category'])
    
    le_location = LabelEncoder()
    df['location'] = le_location.fit_transform(df['location'])

    numerical_features = ['amount', 'time', 'age', 'previous_trans']
    scaler = StandardScaler()
    df[numerical_features] = scaler.fit_transform(df[numerical_features])

    # 3. Split
    X = df.drop('is_fraud', axis=1)
    y = df['is_fraud']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 4. Train Random Forest (best model)
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)

    # Train Logistic Regression (baseline)
    lr_model = LogisticRegression(random_state=42, class_weight='balanced')
    lr_model.fit(X_train, y_train)
    
    # 5. Evaluate Random Forest (Primary)
    precision = precision_score(y_test, rf_preds)
    recall = recall_score(y_test, rf_preds)
    f1 = f1_score(y_test, rf_preds)
    tn, fp, fn, tp = confusion_matrix(y_test, rf_preds).ravel()
    
    metrics = {
        "model": "Random Forest",
        "accuracy": float(rf_model.score(X_test, y_test)),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "confusion_matrix": {
            "tn": int(tn), "fp": int(fp),
            "fn": int(fn), "tp": int(tp)
        }
    }

    print(json.dumps(metrics, indent=2))
    
    # Save Metrics
    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics, f, indent=4)
        
    # Save Artifacts
    joblib.dump(rf_model, os.path.join(MODELS_DIR, "random_forest.pkl"))
    joblib.dump(lr_model, os.path.join(MODELS_DIR, "logistic.pkl"))
    joblib.dump(le_category, os.path.join(MODELS_DIR, "encoder_category.pkl"))
    joblib.dump(le_location, os.path.join(MODELS_DIR, "encoder_location.pkl"))
    joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.pkl"))
    
    print("✨ Training Complete! Models and Metrics Saved.")

if __name__ == "__main__":
    train_and_evaluate()
