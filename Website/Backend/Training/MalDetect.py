import time
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

class MalwareDetector:
    def __init__(self):
        self.model = SVC(kernel='linear')
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4))

    def train_and_report(self, data_dir='Data'):
        start_time = time.time()
        all_dfs = []
        
        # Quét Dataset 05 đến 14
        for i in range(5, 15):
            file_name = f"../Data/Dataset{str(i).zfill(2)}.csv"
            file_path = os.path.join(data_dir, file_name)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path, encoding='latin-1').dropna(axis=1, how='all')
                all_dfs.append(df)
        
        full_df = pd.concat(all_dfs, ignore_index=True)
        
        text_col = full_df.astype(str).apply(lambda x: x.str.len().mean()).idxmax()
        label_col = full_df.nunique().idxmin()
        
        bad_keys = ['phishing', 'malware', 'defacement', 'bad', '1', 1]
        y_all = full_df[label_col].apply(lambda x: 1 if str(x).lower().strip() in [str(k) for k in bad_keys] else 0)
        
        X = self.vectorizer.fit_transform(full_df[text_col].astype(str))
        X_train, X_test, y_train, y_test = train_test_split(X, y_all, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        return acc, (time.time() - start_time), "SVM (Malware Collective)", y_test, y_pred