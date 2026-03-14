#-- Import crucial libraries. --#
import os
import joblib
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
#-- Main NewspaperLinkDetector def for extracting data, learning, and predicting. --#
class NewspaperLinkDetector:
    def __init__(self):
        self.model = LinearSVC(dual=False, random_state=42)
        self.vectorizer = TfidfVectorizer(max_features=2000, stop_words='english')
        self.label_map = None
        self.model_path = os.path.join("Backend", "Results", "newspaper_model.pkl")

    def train_and_report(self, root):
        if os.path.exists(self.model_path):
            data = joblib.load(self.model_path)
            self.model, self.vectorizer, self.label_map = data['model'], data['vectorizer'], data['label_map']
            return data['results']

        datasets_dir = os.path.join(root, "Backend", "Datasets")
        all_dfs = []
        for i in range(16, 27):
            p = os.path.join(datasets_dir, f"Dataset{str(i).zfill(2)}.csv")
            if os.path.exists(p):
                all_dfs.append(pd.read_csv(p, encoding='latin-1'))
        
        full_df = pd.concat(all_dfs, ignore_index=True)
        text_col = next((c for c in full_df.columns if c.upper() in ['URL', 'TITLE']), full_df.columns[0])
        label_col = next((c for c in full_df.columns if c.upper() in ['EXPECTED_LABEL', 'CATEGORY']), full_df.columns[-1])

        y, self.label_map = pd.factorize(full_df[label_col])
        X_vec = self.vectorizer.fit_transform(full_df[text_col].astype(str))
        self.model.fit(X_vec, y)
        
        svd = TruncatedSVD(n_components=2)
        results = {
            "accuracy": accuracy_score(y, self.model.predict(X_vec)),
            "y_test": y, "y_pred": self.model.predict(X_vec),
            "cluster_data": (svd.fit_transform(X_vec), y)
        }
        
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({'model': self.model, 'vectorizer': self.vectorizer, 'label_map': self.label_map, 'results': results}, self.model_path)
        return results

    def predict(self, text):
        X_vec = self.vectorizer.transform([str(text)])
        idx = self.model.predict(X_vec)[0]
        return str(self.label_map[idx]).upper()