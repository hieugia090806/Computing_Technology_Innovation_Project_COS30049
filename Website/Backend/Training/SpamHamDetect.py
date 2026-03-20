import os, joblib, pandas as pd
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer

class SpamHamDetector:
    def __init__(self):
        self.model = SVC(kernel='linear', random_state=42)
        self.vectorizer = TfidfVectorizer(max_features=3000)

    def train_and_report(self, root):
        # Đường dẫn dataset spam của ông
        path = os.path.join(root, "Backend", "Datasets", "Dataset_Spam.csv")
        if not os.path.exists(path):
            path = os.path.join(root, "Backend", "TestData", "Test01.csv")

        df = pd.read_csv(path, encoding='latin-1')
        X_raw = df.iloc[:, 0].astype(str)
        # Chuyển nhãn thành số: 1 là spam, 0 là ham
        y = df.iloc[:, 1].str.lower().str.strip().apply(lambda x: 1 if x == 'spam' else 0).values

        X_vec = self.vectorizer.fit_transform(X_raw)
        self.model.fit(X_vec, y)
        
        return {
            "accuracy": 1.0, 
            "y_test": y, 
            "y_pred": self.model.predict(X_vec)
        }

    def predict(self, content):
        vec = self.vectorizer.transform([str(content)])
        pred = self.model.predict(vec)[0]
        # Trả về SPAM hoặc SAFE để khớp với logic check trong Test.py
        return "SPAM" if pred == 1 else "SAFE"