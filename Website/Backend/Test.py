#-- Import crucial libraries. --#
import os, pandas as pd
from Brain import get_file_category, train_system_by_category, run_analysis
#-- main def. --#
def main():
    website_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_data_dir = os.path.join(website_root, "Backend", "TestData")

    while True:
        print("\n" + "="*50 + "\n1. Select Test File\n2. Quit\n" + "="*50)
        choice = input("Choice: ").strip()
        if choice == '2': break
        if choice == '1':
            files = sorted([f for f in os.listdir(test_data_dir) if f.endswith('.csv')])
            for i, f in enumerate(files): print(f"{i+1}. {f}")
            
            try:
                f_idx = input("\nFile number: ")
                selected_file = files[int(f_idx)-1]
                file_path = os.path.join(test_data_dir, selected_file)
                
                cat = get_file_category(file_path)
                print(f"\n[STEP 1] Detected Category: {cat.upper()}")
                
                train_system_by_category(cat, file_path, website_root)

                print(f"\n[STEP 2] Results for {selected_file}:")
                print("-" * 75)
                df = pd.read_csv(file_path, encoding='latin-1')
                for i, row in df.iterrows():
                    content = str(row.iloc[0])
                    res = run_analysis(content, cat)
                    print(f"Row {i+1}: {res.ljust(12)} | {content[:60]}...")
                print("-" * 75)
                input("\nDone! Press Enter to return...")
            except:
                print("\n[!] Error processing selection.")

if __name__ == "__main__":
    main()