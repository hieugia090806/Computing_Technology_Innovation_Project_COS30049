import time
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

class NewspaperLinkDetector:
    def __init__(self):
        self.model = SVC(kernel='linear')
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)

    def train_and_report(self, data_dir='Data'):
        start_time = time.time()
        all_dfs = []
        
        # Quét Dataset 15 đến 25
        for i in range(15, 26):
            file_name = f"../Data/Dataset{str(i).zfill(2)}.csv"
            file_path = os.path.join(data_dir, file_name)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path, encoding='latin-1')
                all_dfs.append(df)
        
        full_df = pd.concat(all_dfs, ignore_index=True)

        text_col = 'TITLE' if 'TITLE' in full_df.columns else full_df.columns[0]
        label_col = 'CATEGORY' if 'CATEGORY' in full_df.columns else full_df.columns[-1]

        X = self.vectorizer.fit_transform(full_df[text_col].astype(str))
        y = full_df[label_col]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        return acc, (time.time() - start_time), "SVM (News Aggregator)", y_test, y_pred