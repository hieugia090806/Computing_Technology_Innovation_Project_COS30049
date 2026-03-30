#-- Import crucial libraries. --#
import os, pandas as pd
from sklearn.svm import SVC
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
#-- Main SpamHamDetector def for extracting data, learning, and predicting. --#
class SpamHamDetector:
    def __init__(self):
        self.model = SVC(kernel='linear')
        self.vectorizer = TfidfVectorizer(max_features=3000)

    def train_and_report(self, website_root):
        datasets_dir = os.path.join(website_root, "Backend", "Datasets")
        path = os.path.join(datasets_dir, "Dataset_Spam.csv")
        
        if not os.path.exists(path):
            path = os.path.join(website_root, "Backend", "TestData", "Test01.csv")

        df = pd.read_csv(path, encoding='latin-1')
        X_raw = df.iloc[:, 0].astype(str)
        y = df.iloc[:, 1].str.lower().str.strip().apply(lambda x: 1 if x == 'spam' else 0).values

        X_vec = self.vectorizer.fit_transform(X_raw)
        X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)

        # Dữ liệu vẽ biểu đồ
        svd = TruncatedSVD(n_components=2)
        X_2d = svd.fit_transform(X_vec)

        return {
            "accuracy": accuracy_score(y_test, y_pred),
            "y_test": y_test,
            "y_pred": y_pred,
            "cluster_data": (X_2d, y)
        }

    def predict(self, text):
        X_vec = self.vectorizer.transform([str(text)])
        val = self.model.predict(X_vec)[0]
        return "SPAM" if val == 1 else "HAM"