#-- INFORMATION: Central Brain with Grid Table and IMAGE Matrix output. --#
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
#-- Import Experts --#
from SpamHamDetect import SpamHamDetector
from MalDetect import MalwareDetector
from NewspaperLinkDetect import NewspaperLinkDetector

def print_final_grid_and_image_matrix(file_path, acc, t_time, y_test, y_pred, dtype):
    """Hàm in Grid Table và VẼ BIỂU ĐỒ Matrix sang file ảnh"""
    # 1. Đếm dữ liệu thực tế
    df = pd.read_csv(file_path, encoding='latin-1').dropna(axis=1, how='all')
    label_col = df.nunique().idxmin()
    counts = df[label_col].value_counts()
    
    # 2. Tính toán Confusion Matrix 2x2
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0,0,0,len(y_test))

    # --- IN GRID TABLE TRONG TERMINAL ---
    top = "╔" + "═"*50 + "╗"
    mid = "╠" + "═"*24 + "╦" + "═"*25 + "╣"
    bot = "╚" + "═"*24 + "╩" + "═"*25 + "╝"

    print("\n" + top)
    print(f"║ {'SYSTEM ANALYSIS REPORT':^48} ║")
    print(mid)
    for label, count in counts.items():
        print(f"║ {str(label).upper():<22} ║ {count:<23} ║")
    print(mid)
    print(f"║ {'ACCURACY':<22} ║ {acc*100:>22.2f}% ║")
    print(f"║ {'TIME':<22} ║ {t_time:>21.4f}s ║")
    print(bot + "\n")

    # --- VẼ VÀ LƯU BIỂU ĐỒ CÔNFUSION MATRIX (IMAGE) ---
    print(f"[!] Drawing Confusion Matrix image for {file_path}...")
    
    # Tạo nhãn đẹp hơn cho biểu đồ ảnh (ví dụ: Ham vs Spam)
    if dtype == "Spam/Ham":
        class_names = ['Ham (0)', 'Spam (1)']
    elif dtype == "Malware":
        class_names = ['Benign (0)', 'Malware (1)']
    else: class_names = ['Class 0', 'Class 1']

    # Cấu hình biểu đồ
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=class_names, yticklabels=class_names)
    
    # Thêm tiêu đề và nhãn
    plt.title(f'Confusion Matrix (2x2) - {dtype}\nAccuracy: {acc*100:.2f}%', fontsize=14)
    plt.ylabel('REAL CLASS (Real)', fontsize=12)
    plt.xlabel('DETECTED CLASS (Detect)', fontsize=12)
    
    # Thêm chú thích cho các ô TP, FP, FN, TN
    labels = [f'TN\n{tn}', f'FP\n{fp}', f'FN\n{fn}', f'TP\n{tp}']
    # (Optional: If you want text like "TN" inside, more complex code is needed, simple fmt='d' is used above)
    
    # Tên file ảnh đầu ra (ví dụ: Dataset01_Matrix.png)
    image_name = file_path.replace(".csv", "_Matrix.png")
    plt.savefig(image_name) # LƯU FILE ẢNH
    plt.close() # Đóng plot để tiết kiệm bộ nhớ
    
    print(f"[🥇] Image Confusion Matrix saved as: {image_name}")

def main():
    file_path = "../Data/Dataset06.csv" # Đổi file tại đây
    
    match = re.search(r'\d+', file_path)
    file_num = int(match.group()) if match else 0
    
    print(f"[*] Detecting: {file_path}...")

    # Navigation Logic
    if 1 <= file_num <= 5:
        dtype, expert = "Spam/Ham", SpamHamDetector()
    elif 6 <= file_num <= 14 or file_num == 20:
        dtype, expert = "Malware", MalwareDetector()
    elif 15 <= file_num <= 25:
        dtype, expert = "Newspaper", NewspaperLinkDetector()
    else: return

    print(f"[*] Moved to {dtype} Expert. Training & Testing...")

    # Chạy quy trình và lấy kết quả
    acc, t_time, m_info, y_test, y_pred = expert.train_and_report(file_path)

    # In bảng Grid text và LƯU FILE ẢNH matrix
    print_final_grid_and_image_matrix(file_path, acc, t_time, y_test, y_pred, dtype)

if __name__ == "__main__":
    main()