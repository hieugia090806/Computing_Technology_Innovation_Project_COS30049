#-- Import crucial libraries. --#
import pandas as pd
#-- Loader def. --#
class Loader:
    @staticmethod
    def get_category(file_path):
        df = pd.read_csv(file_path, encoding='latin-1', nrows=5)
        cols = [c.upper() for c in df.columns]
        
        if 'URL' in cols or 'TITLE' in cols: 
            return "NEWSPAPER"
        if 'TEXT' in cols or 'CONTENT' in cols or 'SMS' in cols: 
            return "SPAM"
        
        return "MALWARE"