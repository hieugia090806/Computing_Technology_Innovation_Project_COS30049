import os
from Loader import Loader
from Training.MalDetect import MalwareDetector
from Training.SpamHamDetect import SpamHamDetector

# Biến toàn cục để lưu detector
current_detector = None

def train_system_by_category(category_name, file_path, website_root):
    global current_detector
    c = category_name.upper()
    if c == "MALWARE":
        current_detector = MalwareDetector()
    elif c in ["SPAM", "HAM"]:
        current_detector = SpamHamDetector()
    
    if current_detector:
        return current_detector.train_and_report(website_root)
    return None

def run_analysis(content, *args): 
    # Dùng *args để dù ông truyền 'cat' hay 'category' vào nó cũng không báo lỗi
    global current_detector
    
    # 1. Luật cứng: Nếu thấy lệnh hệ thống thì auto MALWARE
    c_low = str(content).lower()
    if any(sig in c_low for sig in ["rm -rf", "nc -e", "powershell", "python -c", "curl"]):
        return "MALWARE"

    # 2. AI Predict
    if current_detector and hasattr(current_detector, 'predict'):
        res = current_detector.predict(content)
        # Nếu detector hiện tại là MalwareDetector thì ép nhãn về MALWARE/SAFE
        if isinstance(current_detector, MalwareDetector):
            return "MALWARE" if res != "SAFE" else "SAFE"
        return res
        
    return "SAFE"

def get_file_category(file_path):
    return Loader.get_category(file_path)