#-- Brain.py --#
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

from Training.SpamHamDetect import SpamHamDetector
from Training.MalDetect import MalwareDetector
from Training.NewspaperLinkDetect import NewspaperLinkDetector

# Khởi tạo Experts
experts = {
    'email': SpamHamDetector(),
    'file': MalwareDetector(),
    'url': NewspaperLinkDetector()
}

def run_analysis(user_input, mode):
    expert = experts.get(mode)
    if not expert:
        return {"error": "Invalid Mode"}

    # 1. Xác định Category dựa trên Mode
    category_map = {
        'email': 'Category: Spam / Ham Detection',
        'file': 'Category: Malware / Virus Analysis',
        'url': 'Category: News Credibility Audit'
    }
    data_category = category_map.get(mode)

    # 2. Train/Load kiến thức từ Dataset tương ứng
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data")
    acc, t_time, m_info, y_test, y_pred = expert.train_and_report(data_dir)

    # 3. FIX LỖI "No Threats": Dùng AI thật để dự đoán user_input
    # Chuyển văn bản user nhập thành vector mà AI hiểu được
    input_vector = expert.vectorizer.transform([user_input])
    prediction_result = expert.model.predict(input_vector)[0]

    # Mapping kết quả dựa trên Mode
    if mode == 'email':
        final_decision = "SPAM DETECTED" if prediction_result == 1 else "HAM (SAFE)"
    elif mode == 'file':
        final_decision = "MALICIOUS (THREAT)" if prediction_result == 1 else "CLEAN (SAFE)"
    else: # url
        final_decision = "GENUINE NEWS" if prediction_result == 1 else "FAKE / SUSPICIOUS"

    # 4. Lưu Confusion Matrix
    matrix_filename = f"{mode}_matrix.png"
    save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Results", matrix_filename)
    save_confusion_matrix(y_test, y_pred, data_category, acc, save_path)

    return {
        "prediction": final_decision,
        "data_type": data_category, # Thông tin bạn muốn in ra thêm
        "accuracy": f"{acc*100:.2f}%",
        "duration": f"{t_time:.4f}s",
        "model_info": m_info,
        "matrix_path": matrix_filename
    }

def save_confusion_matrix(y_test, y_pred, title, acc, save_path):
    plt.figure(figsize=(6, 5))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'{title}\nAccuracy: {acc*100:.2f}%')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()