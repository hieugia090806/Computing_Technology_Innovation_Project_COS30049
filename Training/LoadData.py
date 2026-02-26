#--This file is for loading data for training and testing--#
#--Stép 1: Import Libarary--#
import pandas as pd
import csv

def unify(val):
    v = str(val).lower().strip()
    if v in ['1', '1.0', 'spam', 'malware', 'positive']: 
        return 'SPAM'
    return 'HAM'

#--Stép 2: Load Data--#
def load_data(file_path):
    try:
        df = pd.read_csv(file_path, 
                         encoding='latin-1', 
                         engine='python',
                         on_bad_lines='skip',
                         quoting=csv.QUOTE_MINIMAL)
        
        df = df.dropna()

        df.columns = [col.lower().strip() for col in df.columns]
        
        if 'spam' in df.columns and 'text' in df.columns:
            y_raw = df['spam']
            x_raw = df['text']
        elif 'v1' in df.columns:
            y_raw = df['v1']
            x_raw = df['v2']
        else:
            y_raw = df.iloc[:, -1] 
            x_raw = df.iloc[:, 0]

        X = x_raw.astype(str)
        Y = y_raw.apply(unify)
        
        print(f"✅ Loaded successfully: {len(X)} rows from {file_path}")
        return X, Y

    except Exception as e:
        print(f"❌ Critical Error: {e}")
        return None, None