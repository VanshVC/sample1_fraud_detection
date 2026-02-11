import joblib
import pandas as pd
import os

class ModelInference:
    def __init__(self):
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models")
        self.rf_model = None
        self.lr_model = None
        self.category_encoder = None
        self.location_encoder = None
        self.scaler = None
        self.load_models()

    def load_models(self):
        try:
            self.rf_model = joblib.load(os.path.join(self.base_path, "random_forest.pkl"))
            self.lr_model = joblib.load(os.path.join(self.base_path, "logistic.pkl"))
            self.category_encoder = joblib.load(os.path.join(self.base_path, "encoder_category.pkl"))
            self.location_encoder = joblib.load(os.path.join(self.base_path, "encoder_location.pkl"))
            self.scaler = joblib.load(os.path.join(self.base_path, "scaler.pkl"))
            print("✅ Models loaded successfully.")
        except Exception as e:
            print(f"⚠️ Error loading models: {e}")

    def predict(self, data: dict, model_type: str = "rf"):
        """
        Predicts fraud probability.
        Args:
            data (dict): Dictionary containing transaction features.
            model_type (str): "rf" (Random Forest) or "lr" (Logistic Regression)
        Returns:
            dict: {is_fraud: bool, probability: float, model: str}
        """
        if not self.rf_model: 
            self.load_models()
            if not self.rf_model:
                raise Exception("Models failed to load.")

        # DataFrame conversion
        df = pd.DataFrame([data])

        # Preprocessing
        try:
            # Handle unknown categories safely
            if data['category'] in self.category_encoder.classes_:
                df['category'] = self.category_encoder.transform(df['category'])
            else:
                df['category'] = 0 # Default/Unknown
            
            if data['location'] in self.location_encoder.classes_:
                df['location'] = self.location_encoder.transform(df['location'])
            else:
                df['location'] = 0

            # Scale numericals
            numericals = ['amount', 'time', 'age', 'previous_trans']
            df[numericals] = self.scaler.transform(df[numericals])
            
        except Exception as e:
            raise ValueError(f"Preprocessing Error: {e}")

        # Prediction
        model = self.rf_model if model_type == 'rf' else self.lr_model
        prob = model.predict_proba(df)[0][1]
        prediction = int(prob > 0.5)

        return {
            "is_fraud": bool(prediction),
            "probability": round(float(prob), 4),
            "model_used": "Random Forest" if model_type == 'rf' else "Logistic Regression"
        }

# Global Instance
inference_engine = ModelInference()
