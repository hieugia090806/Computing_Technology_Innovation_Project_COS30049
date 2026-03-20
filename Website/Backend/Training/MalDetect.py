import os
import joblib
import pandas as pd
from sklearn.svm import LinearSVC 
from sklearn.metrics import accuracy_score
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

class MalwareDetector:
    def __init__(self):
        # Khởi tạo model và vectorizer
        self.model = LinearSVC(dual=False, random_state=42)
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 3), max_features=5000)

    def train_and_report(self, root):
        """Hàm này bắt buộc phải có để Brain.py gọi"""
        datasets_dir = os.path.join(root, "Backend", "Datasets")
        all_dfs = []
        # Đọc các file dataset từ 05 đến 15
        for i in range(5, 16):
            p = os.path.join(datasets_dir, f"Dataset{str(i).zfill(2)}.csv")
            if os.path.exists(p):
                all_dfs.append(pd.read_csv(p, encoding='latin-1'))
        
        if not all_dfs: 
            print("[!] Không tìm thấy dataset trong:", datasets_dir)
            return None
            
        full_df = pd.concat(all_dfs, ignore_index=True)
        y = full_df.iloc[:, -1].apply(lambda x: 1 if str(x).strip() in ['1', '1.0', 'malware'] else 0).values
        X_vec = self.vectorizer.fit_transform(full_df.iloc[:, 0].astype(str).fillna(''))
        
        self.model.fit(X_vec, y)
        y_pred = self.model.predict(X_vec)
        
        # Dữ liệu để vẽ Cluster (nếu cần)
        svd = TruncatedSVD(n_components=2)
        cluster_data = svd.fit_transform(X_vec)
        
        return {
            "accuracy": accuracy_score(y, y_pred),
            "y_test": y,
            "y_pred": y_pred,
            "cluster_data": cluster_data
        }

    def predict(self, content):
        """Hàm dự đoán nhãn"""
        vec = self.vectorizer.transform([str(content)])
        pred = self.model.predict(vec)[0]
        return "MALWARE" if pred == 1 else "SAFE"