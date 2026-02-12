import joblib
import pandas as pd
import os
import json

class ModelInference:
    def __init__(self):
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models")
        self.unified_model = None
        self.feature_list = None
        self.rf_model = None
        self.lr_model = None
        self.category_encoder = None
        self.location_encoder = None
        self.scaler = None
        self.load_models()

    def load_models(self):
        try:
            # Check for Unified Colab Model first (Phase 5)
            unified_path = os.path.join(self.base_path, "fraud_model.pkl")
            features_path = os.path.join(self.base_path, "features.json")
            
            if os.path.exists(unified_path) and os.path.exists(features_path):
                self.unified_model = joblib.load(unified_path)
                with open(features_path, "r") as f:
                    self.feature_list = json.load(f)
                print("✅ Unified Colab Model loaded successfully.")
                return

            # Fallback to local separate models
            self.rf_model = joblib.load(os.path.join(self.base_path, "random_forest.pkl"))
            self.lr_model = joblib.load(os.path.join(self.base_path, "logistic.pkl"))
            self.category_encoder = joblib.load(os.path.join(self.base_path, "encoder_category.pkl"))
            self.location_encoder = joblib.load(os.path.join(self.base_path, "encoder_location.pkl"))
            self.scaler = joblib.load(os.path.join(self.base_path, "scaler.pkl"))
            print("✅ Local models loaded successfully.")
        except Exception as e:
            print(f"⚠️ Error loading models: {e}")

    def predict(self, data: dict, model_type: str = "rf"):
        """
        Predicts fraud probability.
        Args:
            data (dict): Dictionary containing transaction features.
            model_type (str): "rf" (Random Forest) or "lr" (Logistic Regression)
        Returns:
            dict: {is_fraud: bool, probability: float, model_used: str}
        """
        # If unified model exists, use it exclusively (Phase 5)
        if self.unified_model and self.feature_list:
            try:
                # Construct feature vector based on saved order
                X = [data.get(f, 0) for f in self.feature_list]
                
                # Check if model has predict_proba
                if hasattr(self.unified_model, "predict_proba"):
                    prob = self.unified_model.predict_proba([X])[0][1]
                else:
                    prob = float(self.unified_model.predict([X])[0])
                
                prediction = int(prob > 0.5)
                return {
                    "is_fraud": bool(prediction),
                    "probability": round(float(prob), 4),
                    "model_used": "Colab Classifier"
                }
            except Exception as e:
                print(f"⚠️ Unified Inference Error: {e}")
                # Fallback to local if possible...

        if not self.rf_model: 
            self.load_models()
            if not (self.rf_model or self.unified_model):
                raise Exception("Models failed to load.")

        # Local Model Inference (Legacy/Fallback)
        df = pd.DataFrame([data])
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
