#-- INFORMATION: Learning, training, and testing for Newspaper Classification. --#
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

class NewspaperLinkDetector:
    def __init__(self):
        self.model = SVC(kernel='linear')
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)

    def train_and_report(self, file_path):
        start_time = time.time()
        df = pd.read_csv(file_path, encoding='latin-1')

        # Đối với Newspaper, ta thường dùng TITLE để phân loại CATEGORY
        # Tui thêm bẫy lỗi nếu file không có cột TITLE/CATEGORY
        text_col = 'TITLE' if 'TITLE' in df.columns else df.columns[0]
        label_col = 'CATEGORY' if 'CATEGORY' in df.columns else df.columns[-1]

        X = self.vectorizer.fit_transform(df[text_col].astype(str))
        y = df[label_col]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        return acc, (time.time() - start_time), "SVM (News Classify)", y_test, y_pred