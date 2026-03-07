#-- INFORMATION: This file is for data loading and intelligent dataset classification. --#
#-- Part A: Import libraries. --#
import pandas as pd
import numpy as np
#-- Part B: Def data_fingerprinting(). --#
def dataset_fingerprinting(file_path):
    try:
        df = pd.read_csv(file_path, encoding='latin-1', nrows=100)
        #-- EXPLAINATION: Take 100 samples from the dataset. --#
    except Exception as e:
        return f"Error when loading file {file_path}"
    #-- Convert the entire 100-row sample into one single string for fast scanning. --#
    #-- Prepare analysis strings. --#
    sample_content = " ".join(df.astype(str).values.flatten()).lower()
    column_names = " ".join(df.columns).lower()
    #-- Identify data types (The "Skeleton"). --#
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    total_cols = len(df.columns)
    num_ratio = len(numeric_cols) / total_cols if total_cols > 0 else 0
    #--- NEWSPAPER DETECTION. ---#
    # Logic: Look for Publisher/Author AND presence of URLs
    news_indicators = ['author', 'publisher', 'article', 'headline', 'title']
    has_news_header = any(ind in column_names for ind in news_indicators)
    has_links = any(link in sample_content for link in ['http', 'www.', '.com'])
    
    if has_news_header and has_links:
        return "Newspaper"

    #-- MALWARE DETECTION. --#
    #-- Logic A: Professional labels. --#
    if 'phishing' in sample_content or 'benign' in sample_content:
        return "Malware"
    #-- Logic B: Structural. --#
    # If the file has many columns and they are almost 100% numbers
    if total_cols > 10 and num_ratio > 0.8:
        return "Malware"

    #-- SPAM AND HAM MAIL DETECTION. --#
    if 'spam' in sample_content or 'ham' in sample_content:
        return "Spam and Ham Email"

    return "Unknown dataset"

def load_and_clean(file_path, dataset_type):
    df = pd.read_csv(file_path, encoding='latin-1') 
    
    # DISCOVER LABEL: Look for binary columns (0/1 or 2 unique values)
    label_col = next((c for c in df.columns if df[c].nunique() == 2), None)
    
    if label_col:
        dangerous_keys = ['spam', 'phishing', 'malware', 'bad', '1', 1, 'defacement']
        df['label'] = df[label_col].apply(
            lambda x: 1 if str(x).lower().strip() in [str(k) for k in dangerous_keys] else 0
        )
    else:
        #-- If no 2-value column found, default to 0 to prevent KeyErro3. --#
        df['label'] = 0

    if dataset_type == "Malware":
        #-- Return all numeric columns as features. --#
        final_df = df.select_dtypes(include=[np.number]).copy()
        return final_df
    else:
        #-- Extract the longest text column as content. --#
        text_cols = df.select_dtypes(include=['object'])
        if not text_cols.empty:
            content_col = text_cols.apply(lambda x: x.astype(str).str.len().mean()).idxmax()
            clean_df = df[[content_col, 'label']].copy()
            clean_df.columns = ['content', 'label']
            return clean_df
            
    return df