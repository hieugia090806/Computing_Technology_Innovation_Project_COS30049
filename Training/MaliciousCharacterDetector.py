import os

def load_malicious_signatures(file_path):
    signatures_db = {}
    current_category = "General Threat"
    
    if not os.path.exists(file_path):
        print(f"[-] Error: Database file '{file_path}' not found.")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Identify Category Headers like #--Category Name--#
            if line.startswith("#--") and line.endswith("--#"):
                current_category = line.replace("#--", "").replace("--#", "").strip()
                signatures_db[current_category] = []
            
            # Add keywords (ignore lines starting with # which are comments)
            elif not line.startswith("#"):
                # Clean keyword if it contains placeholders like <base64_string>
                clean_keyword = line.split('<')[0].strip() if '<' in line else line
                if clean_keyword:
                    signatures_db[current_category].append(clean_keyword)
                    
    return signatures_db

def run_malware_scan(target_file, db):
    print("="*70)
    print(f"🛡️  MALWARE SIGNATURE SCANNER v1.0")
    print(f"[*] Target File: {target_file}")
    print("="*70)

    if not os.path.exists(target_file):
        print(f"[-] Error: Target file '{target_file}' not found.")
        return

    # Read the content of the malicious test file
    with open(target_file, 'r', encoding='utf-8', errors='ignore') as f:
        file_content = f.read().lower()

    malicious_found = False
    
    # Iterate through categories and keywords
    for category, keywords in db.items():
        # List comprehension to find matches
        matches = [key for key in keywords if key.lower() in file_content]
        
        if matches:
            malicious_found = True
            print(f"\n[!] THREAT DETECTED: [{category.upper()}]")
            for m in matches:
                print(f"    -> Signature Match: {m}")
            print("-" * 40)

    print("\n" + "="*70)
    if malicious_found:
        print("🚩 FINAL VERDICT: MALICIOUS CONTENT DETECTED")
        print("[!] Warning: This file contains signatures associated with known malware.")
    else:
        print("✅ FINAL VERDICT: SAFE / CLEAN")
        print("[*] No known malicious signatures were found in the file content.")
    print("="*70)

if __name__ == "__main__":
    # Define file names
    SIGNATURE_DB_FILE = "../Data/MaliciousCharacterList.txt"
    TEST_FILE = "../Data/MaliciousCodeTest02.txt"

    # Step 1: Initialize Database
    signatures = load_malicious_signatures(SIGNATURE_DB_FILE)
    
    # Step 2: Perform Scan
    if signatures:
        run_malware_scan(TEST_FILE, signatures)