#-- This file is considered as central file for training and testing --#
#-- Import libraries and files --#
from Loader import dataset_fingerprinting, load_and_clean 
#-- Dataset_type def --#
def dataset_type(file_path): 
    #-- Identification --#
    print(f"\n[*] Brain is analyzing: {file_path}...")

    dtype = dataset_fingerprinting(file_path)
    #-- Print the output based on your specific requirements --#
    if dtype == "Spam and Ham Email":
        print(">>> Result: This is a Spam and Ham Mail Dataset.")
    elif dtype == "Malware":
        print(">>> Result: This is a Malware/Malicious Dataset.")
    elif dtype == "Newspaper":
        print(">>> Result: This is a Newspaper Detection Dataset.")
    else:
        print(f">>> Result: {dtype}")
    return dtype

#-- Main def() --#
def main():
    file_path = "../Data/Dataset08.csv"
    dtype = dataset_type(file_path)
    if "Unknown" not in dtype:
        df = load_and_clean(file_path, dtype)
        print(f"[*] Data loaded successfully. Ready for training.")
    
#-- Run the program --#
if __name__ == "__main__":
    main()