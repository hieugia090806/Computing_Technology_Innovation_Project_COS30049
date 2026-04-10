import os
import numpy as np
import pandas as pd
import joblib
import traceback

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'Model')


class ModelsHandler:
    def __init__(self):
        self.models = {}
        self.vectorizers = {}
        self.load_all_components()

    def load_all_components(self):
        components = {
            'news': ('NewsModel.pkl', 'NewsVectorizer.pkl'),
            'spam': ('SpamScanner.pkl', 'SpamScannervectorizer.pkl'),
            'malware': ('MalwareModel.pkl', 'MalwareVectorizer.pkl')
        }

        for key, (m_file, v_file) in components.items():
            try:
                model_path = os.path.join(MODEL_DIR, m_file)
                vector_path = os.path.join(MODEL_DIR, v_file)

                # 🔥 Load bằng joblib
                self.models[key] = joblib.load(model_path)
                self.vectorizers[key] = joblib.load(vector_path)

                print(f"✅ Loaded: {key}")

            except Exception:
                print(f"❌ Error loading {key}")
                traceback.print_exc()

    def get_realtime_metrics(self, key, user_input, labels):

        # 🛑 tránh crash nếu model lỗi
        if key not in self.models or key not in self.vectorizers:
            return {"error": f"{key} model not loaded"}

        try:
            text = str(user_input).lower()

            X_vec = self.vectorizers[key].transform([text])

            proba = self.models[key].predict_proba(X_vec)[0]
            pred_id = self.models[key].predict(X_vec)[0]

            return {
                "prediction": labels[pred_id],
                "confidence_score": round(np.max(proba) * 100, 2),
                "risk_score": round(proba[1] * 100, 2),
                "distribution": {
                    labels[0]: round(proba[0] * 100, 2),
                    labels[1]: round(proba[1] * 100, 2)
                },
                "status": "DANGER" if pred_id == 1 else "SAFE",
                "recommendation": (
                    "Do not click or share this content."
                    if pred_id == 1 else
                    "This content appears safe to use."
                )
            }

        except Exception as e:
            return {
                "error": "Prediction failed",
                "details": str(e)
            }

    def predict_newspaper(self, url):
        return self.get_realtime_metrics('news', url, ["Real", "Fake"])

    def predict_spam(self, text):
        return self.get_realtime_metrics('spam', text, ["Ham", "Spam"])

    def predict_malware_text(self, text):
        return self.get_realtime_metrics('malware', text, ["Safe", "Malicious"])


handler = ModelsHandler()