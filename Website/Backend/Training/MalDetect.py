#-- INFORMATION: This file is for learning, training, and testing Malware Detection. --#
import time
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
#-- Class MalwareDetector. --#
class MalwareDetector:
    #-- __init__(self) def --#
    def __init__(self):
        self.model = SVC(kernel='linear')
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4))
    #-- train_and_report def. --#
    def train_and_report(self, file_path):
        start_time = time.time()
        #-- Read file. --#
        df = pd.read_csv(file_path, encoding='latin-1').dropna(axis=1, how='all')
        
        #-- Find label and text column. --#
        text_col = df.astype(str).apply(lambda x: x.str.len().mean()).idxmax()
        label_col = df.nunique().idxmin()
        
        #-- Standardize Labels. --#
        bad_keys = ['phishing', 'malware', 'defacement', 'bad', '1', 1]
        y_all = df[label_col].apply(lambda x: 1 if str(x).lower().strip() in [str(k) for k in bad_keys] else 0)
        
        if len(y_all.unique()) < 2:
            duration = time.time() - start_time
            return 1.0, duration, "SVM (Single Label)", y_all, y_all

        X = self.vectorizer.fit_transform(df[text_col].astype(str))

        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_all, test_size=0.2, random_state=42, stratify=y_all
            )
        except:
            X_train, X_test, y_train, y_test = train_test_split(X, y_all, test_size=0.2, random_state=42)

        #-- Train Model --#
        self.model.fit(X_train, y_train)
        
        #-- Predict for Matrix --#
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        #-- Return results. --#
        return acc, (time.time() - start_time), "SVM (Char-level)", y_test, y_pred