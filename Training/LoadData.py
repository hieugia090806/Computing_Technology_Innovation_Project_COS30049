#--This file is for loading data for training and testing--#
#--Stép 1: Import Libarary--#
import pandas as pd
import csv

def unify(val):
    v = str(val).lower().strip()
    if v in ['1', '1.0', 'spam', 'malware', 'positive', 'bad']: 
        return 'SPAM'
    return 'HAM'
#--Step 2: Load Data--#
def load_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding='latin-1', engine='python', on_bad_lines='skip')
        df = df.dropna()
        #--Malware Mail--#
        if 'classification' in df.columns:
            Y = df['classification'].apply(unify)
            # Extract features by dropping non-feature columns (like 'hash' and 'classification')
            X = df.drop(columns=['hash', 'classification'], errors='ignore')
            print(f"✅ Malware Data Loaded: {len(X)} rows (Numerical Features)")
        #--Spam Ham Mail--#
        else:
            df.columns = [col.lower().strip() for col in df.columns]
            Y = df.iloc[:, -1].apply(unify)
            X = df.iloc[:, 0].astype(str)

        print(f"✅ Data Loaded: {len(X)} rows.")
        return X, Y
    except Exception as e:
        print(f"❌ LoadData Error: {e}")
        return None, None
       
        