
import pandas as pd
import numpy as np
import random
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# Set Seeds for Reproducibility
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)
random.seed(RANDOM_STATE)

BASE_DIR = r"c:\Users\vansh\Downloads\Fraud_Detection"
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

###############################################################################
# PHASE 1: Synthetic Data Generation
###############################################################################
def generate_data(num_samples=10000):
    print(f"🔹 PHASE 1: Generating {num_samples} Synthetic Transactions...")
    
    # 1. Feature Generation
    amounts = np.random.lognormal(mean=3.5, sigma=1.2, size=num_samples)
    amounts = np.round(amounts, 2)

    times = np.random.randint(0, 24, size=num_samples)

    categories_list = ['groceries', 'electronics', 'utilities', 'entertainment', 'travel', 'dining', 'gas']
    categories = np.random.choice(categories_list, size=num_samples)

    ages = np.random.randint(18, 91, size=num_samples)

    locations_list = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    locations = np.random.choice(locations_list, size=num_samples)
    previous_trans = np.random.poisson(lam=15, size=num_samples)


    # 2. Fraud Logic (Deterministic for high F1 in demonstration)

    is_fraud = []
    
    for i in range(num_samples):
        # A transaction is fraud if it meets ANY of these suspicious conditions
        rule1 = (amounts[i] > 600) and (0 <= times[i] <= 5)
        rule2 = (categories[i] == 'travel') and (amounts[i] > 900)
        rule3 = (previous_trans[i] < 2) and (amounts[i] > 400)
        rule4 = (categories[i] == 'electronics') and (locations[i] in ['New York', 'Los Angeles']) and (times[i] > 22)
        
        # Adding a tiny bit of noise (5% chance of random flip) to keep it interesting
        if rule1 or rule2 or rule3 or rule4:
            label = 1 if random.random() < 0.95 else 0
        else:
            label = 1 if random.random() < 0.02 else 0 # 2% random fraud
            
        is_fraud.append(label)




    # Create DataFrame
    df = pd.DataFrame({
        'amount': amounts,
        'time': times,
        'category': categories,
        'age': ages,
        'location': locations,
        'previous_trans': previous_trans,
        'is_fraud': is_fraud
    })

    output_path = os.path.join(DATA_DIR, "credit_card_fraud.csv")
    df.to_csv(output_path, index=False)
    print(f"✅ Data saved to: {output_path}")
    return df

###############################################################################
# PHASE 2: Preprocessing + Split
###############################################################################
def preprocess_and_split(df):
    print("🔹 PHASE 2: Preprocessing & Splitting...")
    
    # Label Encoding
    le_category = LabelEncoder()
    df['category'] = le_category.fit_transform(df['category'])
    
    le_location = LabelEncoder()
    df['location'] = le_location.fit_transform(df['location'])
    
    # Feature Scaling
    scaler = StandardScaler()
    numerical_features = ['amount', 'time', 'age', 'previous_trans']
    df[numerical_features] = scaler.fit_transform(df[numerical_features])
    
    # Save Preprocessors (Optional but good practice)
    joblib.dump(le_category, os.path.join(MODELS_DIR, "encoder_category.pkl"))
    joblib.dump(le_location, os.path.join(MODELS_DIR, "encoder_location.pkl"))
    joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.pkl"))

    # Split
    X = df.drop('is_fraud', axis=1)
    y = df['is_fraud']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    
    print(f"✅ Data split: Train({X_train.shape[0]}), Test({X_test.shape[0]})")
    return X_train, X_test, y_train, y_test

from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score, accuracy_score
import json

###############################################################################
# PHASE 3: Model Training & Evaluation
###############################################################################
def train_and_evaluate(X_train, X_test, y_train, y_test):
    print("🔹 PHASE 3: Training & Evaluating Models...")
    
    # Logistic Regression
    lr = LogisticRegression(random_state=RANDOM_STATE, class_weight='balanced', max_iter=1000)
    lr.fit(X_train, y_train)
    lr_preds = lr.predict(X_test)
    joblib.dump(lr, os.path.join(MODELS_DIR, "logistic.pkl"))
    
    # Random Forest (Main)
    rf = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, class_weight='balanced')
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)
    joblib.dump(rf, os.path.join(MODELS_DIR, "random_forest.pkl"))
    
    # Generate Metrics for Random Forest (as it's the chosen model)
    tn, fp, fn, tp = confusion_matrix(y_test, rf_preds).ravel()
    
    metrics = {
        "accuracy": round(accuracy_score(y_test, rf_preds), 4),
        "precision": round(precision_score(y_test, rf_preds), 4),
        "recall": round(recall_score(y_test, rf_preds), 4),
        "f1_score": round(f1_score(y_test, rf_preds), 4),
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp)
        }
    }
    
    # Save to JSON for Backend/Frontend
    eval_dir = os.path.join(BASE_DIR, "backend", "evaluation")
    os.makedirs(eval_dir, exist_ok=True)
    metrics_path = os.path.join(eval_dir, "metrics.json")
    
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)
        
    print(f"✅ Random Forest F1: {metrics['f1_score']}")
    print(f"✅ Metrics saved to: {metrics_path}")

if __name__ == "__main__":
    df = generate_data()
    X_train, X_test, y_train, y_test = preprocess_and_split(df)
    train_and_evaluate(X_train, X_test, y_train, y_test)
    print("🚀 All Phases Complete!")

