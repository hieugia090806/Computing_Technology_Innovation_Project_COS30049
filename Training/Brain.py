#-- Brain.py: Central Hub for Dataset Identification, Training, and Evaluation --#
#-- Powered by Random Forest for Malware and SVM for Text Classification --#

import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from Loader import dataset_fingerprinting, load_and_clean

class Brain:
    #-- Construction def. --#
    def __init__(self, sig_path='../Data/MalSigs.txt'):
        self.sig_path = sig_path
        # FIXED: Correct parameter 'n_estimators' and unified name
        self.malware_rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.spam_svm_model = SVC(kernel='linear')
        self.news_svm_model = SVC(kernel='linear')
        self.vectorizer = TfidfVectorizer(max_features=2500)
        self.dtype = None
        self.df = None
    
    #-- Identification dataset type. --#
    def dataset_type(self, file_path):
        print(f"\n[*] Brain is analyzing: {file_path}...")
        self.dtype = dataset_fingerprinting(file_path)
        
        # Deep signature scan using the pattern file 
        try:
            with open(self.sig_path, 'r', encoding='utf-8') as f:
                sigs = [l.strip().lower() for l in f if l.strip() and not l.startswith('#')]
            
            df_check = pd.read_csv(file_path, nrows=100, encoding='latin-1')
            sample_str = " ".join(df_check.astype(str).values.flatten()).lower()
            
            if any(sig in sample_str for sig in sigs):
                self.dtype = "Malware"
        except:
            pass

        results = {
            "Spam/Ham Email": "Spam and Ham Mail Dataset.",
            "Malware": "Malware/Malicious Dataset.",
            "Newspaper": "Newspaper Detection Dataset."
        }
        print(f">>> Result: This is a {results.get(self.dtype, self.dtype)}")
        return self.dtype
    
    #-- Model for Malware. --#
    def train_malware_model(self):
        print("[*] Training Module: RANDOM FOREST (Optimized for Malware)")
        
        # Select numeric features and ensure it's not empty
        X = self.df.select_dtypes(include=['number'])
        if 'label' in X.columns:
            X = X.drop(columns=['label'])
        y = self.df['label']

        if X.empty:
            print("[!] Error: No numeric features found for Malware training. Check Loader.py.")
            return
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Fit using the unified model name
        self.malware_rf_model.fit(X_train, y_train)
        acc = accuracy_score(y_test, self.malware_rf_model.predict(X_test))
        print(f"[*] Training Complete. Accuracy: {acc*100:.2f}%")

    #-- Model for Spam/Ham --#
    def train_spam_model(self):
        print("[*] Training Module: SVM (Optimized for Spam/Ham Text)")
        X = self.vectorizer.fit_transform(self.df['content'])
        y = self.df['label']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.spam_svm_model.fit(X_train, y_train)
        acc = accuracy_score(y_test, self.spam_svm_model.predict(X_test))
        print(f"[*] Training Complete. Accuracy: {acc*100:.2f}%")

    #-- Model for Newspaper --#
    def train_newspaper_model(self):
        print("[*] Training Module: SVM (Optimized for Newspaper Articles)")
        X = self.vectorizer.fit_transform(self.df['content'])
        y = self.df['label']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.news_svm_model.fit(X_train, y_train)
        acc = accuracy_score(y_test, self.news_svm_model.predict(X_test))
        print(f"[*] Training Complete. Accuracy: {acc*100:.2f}%")

#-- Execution logic --#
def main():
    file_path = "../Data/Dataset03.csv" 
    brain = Brain(sig_path='../Data/MalSigs.txt')
    
    dtype = brain.dataset_type(file_path)
    if "Unknown" not in dtype:
        brain.df = load_and_clean(file_path, dtype)
        if brain.df is not None and not brain.df.empty:
            print(f"[*] Data Loaded: {brain.df.shape[0]} rows.")
            if dtype == "Malware":
                brain.train_malware_model()
            elif dtype == "Spam/Ham Email":
                brain.train_spam_model()
            elif dtype == "Newspaper":
                brain.train_newspaper_model()
        else:
            print("[!] Error: Data could not be processed by Loader.py")

if __name__ == "__main__":
    main()