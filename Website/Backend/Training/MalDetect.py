#-- Import crucial libraries. --#
import os
import joblib
import pandas as pd
from sklearn.svm import LinearSVC 
from sklearn.metrics import accuracy_score
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
#-- MalwareDetector def for extracting data, learning from datasets, and predicting. --#
class MalwareDetector:
    def __init__(self):
        self.model = LinearSVC(dual=False, random_state=42)
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 3), max_features=5000)
        self.model_path = os.path.join("Backend", "Results", "malware_model.pkl")

    def train_and_report(self, root):
        if os.path.exists(self.model_path):
            data = joblib.load(self.model_path)
            self.model, self.vectorizer = data['model'], data['vectorizer']
            return data['results']

        datasets_dir = os.path.join(root, "Backend", "Datasets")
        all_dfs = [pd.read_csv(os.path.join(datasets_dir, f"Dataset{str(i).zfill(2)}.csv"), encoding='latin-1') 
                   for i in range(5, 16) if os.path.exists(os.path.join(datasets_dir, f"Dataset{str(i).zfill(2)}.csv"))]
        
        full_df = pd.concat(all_dfs, ignore_index=True)
        y = full_df.iloc[:, -1].apply(lambda x: 1 if str(x).strip() in ['1', '1.0', 'malware'] else 0).values
        X_vec = self.vectorizer.fit_transform(full_df.iloc[:, 0].astype(str))
        
        self.model.fit(X_vec, y)
        svd = TruncatedSVD(n_components=2)
        results = {
            "accuracy": accuracy_score(y, self.model.predict(X_vec)),
            "y_test": y, "y_pred": self.model.predict(X_vec),
            "cluster_data": (svd.fit_transform(X_vec), y)
        }
        
        joblib.dump({'model': self.model, 'vectorizer': self.vectorizer, 'results': results}, self.model_path)
        return results

    def predict(self, text):
        X_vec = self.vectorizer.transform([str(text)])
        res = self.model.predict(X_vec)[0]
        return "MALICIOUS" if res == 1 else "SAFE"