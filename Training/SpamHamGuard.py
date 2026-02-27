#--For Spam and Ham Detect, my team uses the Mltimonial Naive Bayes--#
#--Import libraries--#
import time
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from LoadSpamHamData import load_spam_ham_data 
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
#--Setup and Data Loading--#
file_path = '../Data/SpamHamDataset03.csv'
df = load_spam_ham_data(file_path)

if df is None:
    exit()  
#--Separate SPAM and HAM for Advanced Analysis--#
df_spam = df[df['label'] == 'SPAM']
df_ham = df[df['label'] == 'HAM']
#--ADVANCED PREVIEW TABLE (FIGURE 1 & 2 Combined into Professional View)--#
#--Function to Print Advanced Table--#
def print_advanced_table(target_df, title):
    print("\n" + "═"*135)
    print(f"║ {title:^131} ║")
    print("═"*135)
    print(f"║ {'ID':<6} ║ {'LABEL':<10} ║ {'SUMMARY (SUBJECT OR CONTENT)':<45} ║ {'DATE':<15} ║ {'TARGET':<20} ║")
    print("-" * 135)
    
    for _, row in target_df.head(15).iterrows():
        # Lấy Subject làm tóm tắt, nếu N/A thì lấy nội dung Content
        summary = str(row['subject']) if row['subject'] != "N/A" else str(row['content'])[:42].replace('\n', ' ') + "..."
        if len(summary) > 45: summary = summary[:42] + "..."
        
        date_str = str(row['date'])
        # Giả lập Target (Người nhận)
        target = "Security Quarantine" if row['label'] == 'SPAM' else "User Inbox"
        
        print(f"║ {str(row['id']):<6} ║ {row['label']:<10} ║ {summary:<45} ║ {date_str:<15} ║ {target:<20} ║")
    print("═"*135)

print_advanced_table(df_spam, "FIGURE 1: ADVANCED SPAM METADATA ANALYSIS")
print_advanced_table(df_ham, "FIGURE 2: ADVANCED HAM METADATA ANALYSIS")
#--Dataset Split--#
X = df['content']
Y = df['label']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

print("\n" + "="*45)
print(f"{'DATASET SHOWCASE':^45}")
print("="*45)
print(f"{'Category':<20} | {'Number':<20}")
print("-" * 45)
print(f"{'Training (80%)':<20} | {len(Y_train):<20}") 
print(f"{'Testing (20%)':<20} | {len(Y_test):<20}")  
print("-" * 45)
print(f"{'Total Processed':<20} | {len(Y):<20}")      
print("="*45)

#--Training Model--#
print("\n🚀 Training Multinomial Naive Bayes model...")
model = make_pipeline(CountVectorizer(), MultinomialNB())

start_time = time.time()
model.fit(X_train, Y_train)
train_duration = time.time() - start_time

#--PERFORMANCE REPORT--#
Y_pred = model.predict(X_test)
accuracy = accuracy_score(Y_test, Y_pred)

print("\n" + "="*45)
print(f"{'FINAL PERFORMANCE REPORT':^45}")
print("="*45)
print(f"Overall Accuracy: {accuracy:.2%}")
print(f"Training Time:    {train_duration:.4f}s")
print("="*45)

print("\nDetailed Classification Report:")
print(classification_report(Y_test, Y_pred))

#--Visualize Confusion Matrix--#
plt.figure(figsize=(8, 6))
cm = confusion_matrix(Y_test, Y_pred, labels=['HAM', 'SPAM'])
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Predicted HAM', 'Predicted SPAM'],
            yticklabels=['Actual HAM', 'Actual SPAM'])

plt.title(f'Spam Detection Results (Accuracy: {accuracy:.2%})')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()