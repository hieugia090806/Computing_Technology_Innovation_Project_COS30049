#-- INFORMATION: Learning, training, and testing for Spam/Ham. --#
#-- Import crucial libraries. --#
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
#-- class SpamHamDetector. --#
class SpamHamDetector:
    #-- __init__(self) def --#
    def __init__(self):
        self.model = SVC(kernel='linear')
        self.vectorizer = TfidfVectorizer(max_features=3000)
    #-- train_and_report def. --#
    def train_and_report(self, file_path):
        start_time = time.time()
        df = pd.read_csv(file_path, encoding='latin-1').dropna(axis=1, how='all')
        
        text_col = df.astype(str).apply(lambda x: x.str.len().mean()).idxmax()
        label_col = next(c for c in df.columns if df[c].nunique() == 2)
        
        X = self.vectorizer.fit_transform(df[text_col].astype(str))
        y = df[label_col].apply(lambda x: 1 if str(x).lower().strip() in ['spam', '1'] else 0)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        duration = time.time() - start_time
        
        return acc, duration, "SVM", y_test, y_pred