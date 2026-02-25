#--This file is for loading data for training and testing--#
#--Stép 1: Import Libarary--#
import pandas as pd
#--Stép 2: Load Data--#
def load_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding='latin-1', usecols=[0, 1], header=0, names=['col_a', 'col_b'])
        #--encoding='latin-1" is used to specifies the character encoding of the file ot avoid UnicodeDecodeError--#
        #--usecols=[0,1] means only reads the first two columns (column index 0 and 1)--#
        #--header=0 indicates that the first row of the CSV file contains column headers==#
        #--names=['col_a', 'col_b'] renames the selected columns to: 'col_a' and 'col_b'--#
        df = df.dropna() #--dropna(): Removes all rows that contain missing values (NaN) in any column--#

        sample = str(df['col_a'].iloc[0]).lower().strip()
        if sample in ['ham', 'spam', '0', '1', '0.0', '1.0', 'malware']:
            y_raw, x_raw = df['col_a'], df['col_b']
        else:
            y_raw, x_raw = df['col_b'], df['col_a']

        def unify(val):
            v = str(val).lower().strip()
            if v in ['1', '1.0', 'spam', 'malware']: return 'SPAM'
            return 'HAM'

        X = x_raw.astype(str)
        Y = y_raw.apply(unify)
        
    except Exception as e:
        print(f"❌ Lỗi đọc file {file_path}: {e}")
        return None, None