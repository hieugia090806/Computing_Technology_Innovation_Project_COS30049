#-- Import crucial libraries. --#
import os
import seaborn as sns
from Loader import Loader
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from Training.MalDetect import MalwareDetector
from Training.SpamHamDetect import SpamHamDetector
from Training.NewspaperLinkDetect import NewspaperLinkDetector

current_detector = None
current_cat = None 

class Brain:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.results_dir = os.path.join(self.data_dir, "Backend", "Results")
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def train_system_by_category(self, category):
        global current_detector, current_cat 
        category = category.upper()
        
        if category == "SPAM": current_detector = SpamHamDetector()
        elif category == "MALWARE": current_detector = MalwareDetector()
        elif category == "NEWSPAPER": current_detector = NewspaperLinkDetector()
        
        current_cat = category
        
        if current_detector:
            results = current_detector.train_and_report(self.data_dir)
            if results:
                self.save_visuals(category, results)
            return results
        return None

    def save_visuals(self, category, results):
        if 'cluster_data' in results:
            X_2d, y = results['cluster_data']
            plt.figure(figsize=(8, 6))
            plt.scatter(X_2d[:, 0], X_2d[:, 1], c=y, cmap='coolwarm', alpha=0.6)
            plt.title(f"Cluster Map - {category}")
            plt.savefig(os.path.join(self.results_dir, f"{category}_cluster.png"))
            plt.close()

        if 'y_test' in results and 'y_pred' in results:
            cm = confusion_matrix(results['y_test'], results['y_pred'])
            plt.figure(figsize=(6, 5))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
            plt.title(f"Confusion Matrix - {category}")
            plt.savefig(os.path.join(self.results_dir, f"{category}_confusion_matrix.png"))
            plt.close()

def heuristic_security_check(content):
    c = str(content).lower().strip()
    
    phishing_sigs = [
        ".xyz", ".top", ".tk", ".online", "bit.ly", "tinyurl.com",
        "nhan-qua", "quatang", "dang-nhap", "secure-news", "account-verification"
    ]
    
    tech_sigs = ["eicar", "eval(", "drop table", "<script>", "nc -lvp"]

    for sig in (phishing_sigs + tech_sigs):
        if sig in c:
            return "THREAT (Heuristic Match)"
    return None

def get_file_category(file_path):
    return Loader.get_category(file_path)

def train_system_by_category(category, file_path, website_root):
    brain = Brain(website_root)
    return brain.train_system_by_category(category)

def run_analysis(content, category, website_root=None):
    global current_detector, current_cat # PHẢI CÓ DÒNG NÀY ĐỂ TRUY CẬP BIẾN TOÀN CỤC
    
    h_res = heuristic_security_check(content)
    if h_res: return h_res

    if current_detector is None and website_root:
        temp_brain = Brain(website_root)
        temp_brain.train_system_by_category(category)

    #-- Run AI. --#
    if current_detector and hasattr(current_detector, 'predict'):
        try:
            prediction = current_detector.predict(content)
            p_val = str(prediction).lower()
            if any(x in p_val for x in ["1", "spam", "threat", "fake", "malicious"]):
                return "THREAT/FAKE"
            return "SAFE/REAL"
        except Exception as e:
            return f"Error: {str(e)}"
            
    return "UNKNOWN: Please Train Model First"