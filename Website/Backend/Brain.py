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
#-- Brain def. --#
class Brain:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.results_dir = os.path.join(self.data_dir, "Backend", "Results")
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def train_system_by_category(self, category):
        global current_detector
        if category == "SPAM": current_detector = SpamHamDetector()
        elif category == "MALWARE": current_detector = MalwareDetector()
        elif category == "NEWSPAPER": current_detector = NewspaperLinkDetector()
        
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

def get_file_category(file_path):
    return Loader.get_category(file_path)

def train_system_by_category(category, file_path, website_root):
    brain = Brain(website_root)
    return brain.train_system_by_category(category)

def run_analysis(content, category):
    global current_detector
    if current_detector and hasattr(current_detector, 'predict'):
        return current_detector.predict(content)
    return "UNKNOWN"