import joblib
import os

base_path = r"c:\Users\vansh\Downloads\Fraud_Detection\backend\models"
category_encoder = joblib.load(os.path.join(base_path, "encoder_category.pkl"))
print("Category classes:", category_encoder.classes_)

location_encoder = joblib.load(os.path.join(base_path, "encoder_location.pkl"))
print("Location classes:", location_encoder.classes_)
