#-- INFORMATION: This central script coordinates AI Experts and returns results --#
import re
import os
import sys
import matplotlib
matplotlib.use('Agg') # Required for Flask to prevent threading crashes
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import confusion_matrix

#-- Import custom expert modules --#
from SpamHamDetect import SpamHamDetector
from MalDetect import MalwareDetector
from NewspaperLinkDetect import NewspaperLinkDetector

def run_analysis(file_path):
    """Hybrid function for Terminal and Web usage"""
    # Extract file number from path
    match = re.search(r'\d+', os.path.basename(file_path))
    file_num = int(match.group()) if match else 0
    
    # Navigation Logic
    if 1 <= file_num <= 5:
        dtype, expert = "Spam/Ham", SpamHamDetector()
    elif 6 <= file_num <= 14 or file_num == 20:
        dtype, expert = "Malware", MalwareDetector()
    elif 15 <= file_num <= 25:
        dtype, expert = "Newspaper", NewspaperLinkDetector()
    else: 
        return None

    # Run AI training and get results
    acc, t_time, m_info, y_test, y_pred = expert.train_and_report(file_path)
    
    # Save image to the Results folder
    # Assuming file_path is like ".../Data/Dataset14.csv"
    # We save as ".../Results/Dataset14_Matrix.png"
    base_name = os.path.basename(file_path).replace(".csv", "_Matrix.png")
    # Go up one level from Training to Backend, then into Results
    save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Results", base_name)
    
    save_confusion_matrix(y_test, y_pred, dtype, acc, save_path)
    
    return {
        "accuracy": f"{acc*100:.2f}%",
        "duration": f"{t_time:.4f}s",
        "type": dtype,
        "model_info": m_info,
        "matrix_path": base_name # Just the filename for the URL
    }

def save_confusion_matrix(y_test, y_pred, dtype, acc, save_path):
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Analysis: {dtype} (Acc: {acc*100:.2f}%)')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()