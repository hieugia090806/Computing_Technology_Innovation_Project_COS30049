import os
import pandas as pd
# Import các hàm từ Brain.py
from Brain import get_file_category, train_system_by_category, run_analysis

def main():
    # Xác định đường dẫn chính xác
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_dir = os.path.join(current_dir, "TestData")
    website_root = os.path.dirname(current_dir)

    while True:
        print("\n" + "="*80)
        print(" TRUTHGUARD SECURITY SYSTEM ".center(80, "="))
        print("1. Select Test File (.csv) | 2. Exit")
        choice = input("Your Choice: ").strip()

        if choice == '2': break
        if choice == '1':
            # Liệt kê file trong TestData
            files = sorted([f for f in os.listdir(test_data_dir) if f.endswith('.csv')])
            for i, f in enumerate(files):
                print(f"{i+1}. {f}")

            try:
                f_idx = int(input("\nChọn số file: ")) - 1
                selected_file = files[f_idx]
                full_path = os.path.join(test_data_dir, selected_file)

                # 1. Nhận diện loại file (Malware/Spam)
                # Tui đặt tên biến là 'category' cho chuẩn
                category = get_file_category(full_path)
                print(f"[INFO] Hệ thống nhận diện đây là loại: {category.upper()}")

                # 2. Huấn luyện dựa trên loại file
                train_system_by_category(category, full_path, website_root)

                # 3. In bảng kết quả
                print(f"\nKẾT QUẢ KIỂM TRA: {selected_file}")
                print("-" * 110)
                print(f"{'NỘI DUNG':<55} | {'DỰ ĐOÁN':<12} | {'THỰC TẾ':<10} | {'TRẠNG THÁI'}")
                print("-" * 110)

                df = pd.read_csv(full_path, encoding='latin-1')
                for _, row in df.iterrows():
                    content = str(row.iloc[0])
                    label_goc = str(row.iloc[1]).strip().upper()

                    # Đồng bộ nhãn thực tế để so sánh
                    if category.upper() == "MALWARE":
                        actual = "MALWARE" if label_goc in ["1", "1.0", "MALWARE"] else "SAFE"
                    else:
                        actual = "SPAM" if label_goc in ["SPAM", "1"] else "SAFE"

                    # GỌI HÀM PHÂN TÍCH (Truyền đúng biến 'category' vào)
                    prediction = run_analysis(content, category)

                    status = "✅ OK" if prediction == actual else "❌ FAIL"
                    preview = (content[:52] + '..') if len(content) > 52 else content.ljust(54)
                    print(f"{preview:<55} | {prediction:<12} | {actual:<10} | {status}")

            except Exception as e:
                print(f"[!] Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    main()