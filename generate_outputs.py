
import pandas as pd
import numpy as np
import joblib
import os
import json
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay, accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "credit_card_fraud.csv")
MODELS_DIR = os.path.join(BASE_DIR, "backend", "models")
OUTPUT_DIR = os.path.join(BASE_DIR, "frontend", "public", "analysis")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load Data
df = pd.read_csv(DATA_PATH)

# Re-apply preprocessing for consistency (minimal logic from data_pipeline.py)
# Note: we need the same encoding and scaling as the model was trained with.
# But for visual evaluation, we just need the numeric data.
# The data in csv is already processed? No, data_pipeline generates then processes.
# Let's check the CSV content.
sample_df = pd.read_csv(DATA_PATH, nrows=5)
print("CSV Columns:", sample_df.columns.tolist())

# data_pipeline.py preprocesses the DF and THEN saves to models.
# It doesn't save the processed DF to CSV. It saves the RAW DF to CSV and then processes it for training.
# Wait, let's check lines 80-81 of data_pipeline.py:
# 80:     output_path = os.path.join(DATA_DIR, "credit_card_fraud.csv")
# 81:     df.to_csv(output_path, index=False)
# This is called in generate_data.
# Then preprocess_and_split is called on that df.
# So the CSV contains the RAW data.

# We need the encoders and scaler.
UNIFIED_MODEL_PATH = os.path.join(MODELS_DIR, "fraud_model.pkl")
FEATURES_PATH = os.path.join(MODELS_DIR, "features.json")

if os.path.exists(UNIFIED_MODEL_PATH) and os.path.exists(FEATURES_PATH):
    print("🔹 Using Unified Colab Model for evaluation...")
    model = joblib.load(UNIFIED_MODEL_PATH)
    with open(FEATURES_PATH, "r") as f:
        feature_list = json.load(f)
    
    # For the unified model, we assume the CSV features map directly to the feature list
    # but we still need the test split for evaluation.
    # Note: Unified model usually expects raw numeric inputs or handles preprocessing internally.
    # However, for consistency with generate_data, we'll use the CSV data.
    X = df[feature_list]
    y = df['is_fraud']
else:
    print("🔹 Using Local Models for evaluation...")
    le_category = joblib.load(os.path.join(MODELS_DIR, "encoder_category.pkl"))
    le_location = joblib.load(os.path.join(MODELS_DIR, "encoder_location.pkl"))
    scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
    model = joblib.load(os.path.join(MODELS_DIR, "random_forest.pkl"))

    # Preprocess
    df['category'] = le_category.transform(df['category'])
    df['location'] = le_location.transform(df['location'])
    numerical_features = ['amount', 'time', 'age', 'previous_trans']
    df[numerical_features] = scaler.transform(df[numerical_features])

    X = df.drop('is_fraud', axis=1)
    y = df['is_fraud']

_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

y_pred = model.predict(X_test)

print("--- Generating Visuals ---")

# 1. Confusion Matrix
ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, cmap='Blues')
plt.title("Confusion Matrix")
plt.savefig(os.path.join(OUTPUT_DIR, "confusion_matrix.png"))
plt.close()
print("✅ Saved confusion_matrix.png")

# 2. ROC Curve
RocCurveDisplay.from_estimator(model, X_test, y_test)
plt.title("ROC Curve")
plt.savefig(os.path.join(OUTPUT_DIR, "roc_curve.png"))
plt.close()
print("✅ Saved roc_curve.png")

# 3. Feature Importance
importances = model.feature_importances_
features = X.columns
feat_importances = pd.Series(importances, index=features).sort_values()
plt.figure(figsize=(10, 6))
feat_importances.plot(kind="barh", color='skyblue')
plt.title("Feature Importance")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "feature_importance.png"))
plt.close()
print("✅ Saved feature_importance.png")

# 4. Metrics JSON
metrics = {
    "accuracy": round(accuracy_score(y_test, y_pred), 4),
    "precision": round(precision_score(y_test, y_pred), 4),
    "recall": round(recall_score(y_test, y_pred), 4),
    "f1_score": round(f1_score(y_test, y_pred), 4)
}

with open(os.path.join(OUTPUT_DIR, "metrics.json"), "w") as f:
    json.dump(metrics, f, indent=4)
print("✅ Saved metrics.json")
