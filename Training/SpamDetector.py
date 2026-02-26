#--Import libraries--#
import time
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from LoadData import load_data
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
#--Setup and Data Loading--#
file_path = '../Data/SpamHamMail03.csv'
X, Y = load_data(file_path)

if X is None:
    print(f"❌ Error: Could not load data from {file_path}. Check your path or LoadData.py logic.")
    exit()
#--ADVANCED DATA PREVIEW (Full Content Separation)--#
df_full = pd.DataFrame({'Label': Y, 'Content': X})
df_spam = df_full[df_full['Label'] == 'SPAM']
df_ham = df_full[df_full['Label'] == 'HAM']
#--Print Spam Table--#
print("\n" + "="*100)
print(f"{'FIGURE 1: FULL SPAM MAIL CONTENT':^100}")
print("="*100)
print(f"{'INDEX':<6} | {'LABEL':<10} | {'MESSAGE CONTENT'}")
print("-" * 100)
for idx, row in df_spam.head(20).iterrows(): # Using .head(20) for terminal readability
    print(f"{idx:<6} | {row['Label']:<10} | {str(row['Content'])[:85].replace('\n', ' ')}...")
#--Print Ham Table--#
print("\n" + "="*100)
print(f"{'FIGURE 2: FULL HAM MAIL CONTENT':^100}")
print("="*100)
print(f"{'INDEX':<6} | {'LABEL':<10} | {'MESSAGE CONTENT'}")
print("-" * 100)
for idx, row in df_ham.head(20).iterrows(): # Using .head(20) for terminal readability
    print(f"{idx:<6} | {row['Label']:<10} | {str(row['Content'])[:85].replace('\n', ' ')}...")
#--Dataset Split--#
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
print("\nClassification Detail:")
print(classification_report(Y_test, Y_pred))
#--Visualize Confusion Matrix--#
plt.figure(figsize=(8, 6))
cm = confusion_matrix(Y_test, Y_pred, labels=['HAM', 'SPAM'])
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Predicted HAM', 'Predicted SPAM'],
            yticklabels=['Actual HAM', 'Actual SPAM'])

plt.title(f'Spam Detection Confusion Matrix\nAccuracy: {accuracy:.2%}')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()