import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, f1_score

# Configuration
DATA_PATH = r"c:\Users\vansh\Downloads\Fraud_Detection\credit_card_fraud.csv"
MODEL_PATH_LR = r"c:\Users\vansh\Downloads\Fraud_Detection\backend\app\ml\logistic_regression.pkl"
MODEL_PATH_RF = r"c:\Users\vansh\Downloads\Fraud_Detection\backend\app\ml\random_forest.pkl"
ENCODER_PATH_CAT = r"c:\Users\vansh\Downloads\Fraud_Detection\backend\app\ml\encoder_category.pkl"
ENCODER_PATH_LOC = r"c:\Users\vansh\Downloads\Fraud_Detection\backend\app\ml\encoder_location.pkl"
SCALER_PATH = r"c:\Users\vansh\Downloads\Fraud_Detection\backend\app\ml\scaler.pkl"

def train_models():
    print("🚀 Starting Model Training Pipeline...")

    # 1. Load Data
    try:
        df = pd.read_csv(DATA_PATH)
        print(f"✅ Data Loaded: {df.shape}")
    except FileNotFoundError:
        print(f"❌ Error: Data file not found at {DATA_PATH}")
        return

    # 2. Preprocessing
    print("🛠 Preprocessing Data...")
    
    # Label Encoding for categorical variables
    le_category = LabelEncoder()
    df['category'] = le_category.fit_transform(df['category'])
    
    le_location = LabelEncoder()
    df['location'] = le_location.fit_transform(df['location'])

    # Feature Scaling
    scaler = StandardScaler()
    numerical_features = ['amount', 'time', 'age', 'previous_trans'] # category and location are now int-encoded
    # Ideally we scale numericals. We can scale everything or just specific columns.
    # RF is invariant to scaling, but LR needs it.
    df[numerical_features] = scaler.fit_transform(df[numerical_features])

    # 3. Feature-Target Separation
    X = df.drop('is_fraud', axis=1)
    y = df['is_fraud']
    
    # 4. Train-Test Split (Stratified)
    print("✂️  Splitting Data (80/20 Stratified)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 5. Model Training
    
    # Model 1: Logistic Regression
    print("🤖 Training Logistic Regression...")
    lr_model = LogisticRegression(random_state=42, class_weight='balanced') # Handling imbalance
    lr_model.fit(X_train, y_train)
    
    lr_preds = lr_model.predict(X_test)
    lr_f1 = f1_score(y_test, lr_preds)
    print(f"   -> LR F1-Score: {lr_f1:.4f}")
    
    # Model 2: Random Forest
    print("🌲 Training Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    rf_model.fit(X_train, y_train)
    
    rf_preds = rf_model.predict(X_test)
    rf_f1 = f1_score(y_test, rf_preds)
    print(f"   -> RF F1-Score: {rf_f1:.4f}")

    # 6. Evaluation
    print("\n📊 Evaluation Report (Random Forest):")
    print(classification_report(y_test, rf_preds))
    
    # 7. Save Artifacts
    print("💾 Saving Models & Preprocessors...")
    joblib.dump(lr_model, MODEL_PATH_LR)
    joblib.dump(rf_model, MODEL_PATH_RF)
    joblib.dump(le_category, ENCODER_PATH_CAT)
    joblib.dump(le_location, ENCODER_PATH_LOC)
    joblib.dump(scaler, SCALER_PATH)
    
    print("✨ Training Complete! All artifacts saved.")

if __name__ == "__main__":
    train_models()
