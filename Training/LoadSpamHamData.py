#--This file is for loading the data of SPAM and HAM--#
#--Import library--#
import pandas as pd
#--Main def--#
def load_spam_ham_data(file_path):
    try:
        #--Raed CSV file--#
        df = pd.read_csv(file_path, encoding='latin-1')
        #--Standardize column names--#
        df.columns = [str(c).lower().strip() for c in df.columns]
        #--Identify label and content columns--#
        x_col = next((c for c in ['message', 'v2', 'text', 'content'] if c in df.columns), None)
        y_col = next((c for c in ['spam/ham', 'v1', 'label', 'spam'] if c in df.columns), None)

        if not x_col or not y_col:
            print("❌ Error: Missing core columns!")
            return None
        #--Dataframe Generation--#
        processed_df = pd.DataFrame()
        #--Basic columns--#
        processed_df['content'] = df[x_col].astype(str)
        processed_df['label'] = df[y_col].astype(str).str.upper().map(
            lambda x: 'SPAM' if any(s in x.lower() for s in ['spam', '1', 'positive']) else 'HAM'
        )
        #--Additional metadata (if available)--#
        processed_df['id'] = df['message id'] if 'message id' in df.columns else df.index
        processed_df['subject'] = df['subject'] if 'subject' in df.columns else "N/A"
        processed_df['date'] = df['date'] if 'date' in df.columns else "Unknown Date"

        print(f"✅ Data Loaded: {len(processed_df)} rows.")
        return processed_df
    except Exception as e:
        print(f"❌ Load Error: {e}")
        return None