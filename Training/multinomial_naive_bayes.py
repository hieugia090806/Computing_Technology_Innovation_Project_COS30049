#--Import crucial libraries--#
import os
import re
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
#--oad and Prepare Data--#
file_path = '../Data/SHTest04.csv' 
df = pd.read_csv(file_path, encoding='latin-1')
#--Upgrade this part--#
#--2. Smart Column Detection--#
text_cols = ['v2', 'email_text', 'origin', 'text', 'message', 'content']
label_cols = ['v1', 'label', 'class', 'target']

col_x = next((c for c in text_cols if c in df.columns), None)
col_y = next((c for c in label_cols if c in df.columns), None)

if not col_x or not col_y:
    raise ValueError("Error: Could not find data columns in the CSV file!")

X = df[col_x].astype(str)
Y_raw = df[col_y]

#--3. Universal Label Mapping (Handles spam/ham and 0/1)--#
def map_labels(val):
    val = str(val).lower().strip()
    if val in ['1', '1.0', 'spam']: return 'spam'
    if val in ['0', '0.0', 'ham']: return 'ham'
    return val

Y = Y_raw.apply(map_labels)

print(f"--- SUCCESS: Processing file [{file_path}] ---")
print(f"Detected Content Column: '{col_x}'")
print(f"Detected Label Column: '{col_y}'")
#--Table 1: Showcase quantity--#
counts = Y.value_counts()
print("\n" + "="*35)
print(f"{'Table 1: DATASET DISTRIBUTION':^35}")
print("="*35)
print(f"{'CATEGORY':<15} | {'QUANTITY':<10}")
print("-" * 35)
for label, count in counts.items():
    print(f"{label.capitalize():<15} | {count:<10}")
print("="*35)
print(f"Total Messages: {len(df)}")

#--Split data--#
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

#--Training and Predict (với đo lường thời gian)--#
model = make_pipeline(CountVectorizer(), MultinomialNB())

start_train = time.time()
model.fit(X_train, Y_train)
train_time = time.time() - start_train

start_test = time.time()
Y_pred = model.predict(X_test)
test_time = time.time() - start_test

#--Showcase by using graph--#
cm = confusion_matrix(Y_test, Y_pred)
plt.figure(figsize=(7, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='YlGnBu', 
            xticklabels=['Ham', 'Spam'], 
            yticklabels=['Ham', 'Spam'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title(f'CONFUSION MATRIX: {file_path.split("/")[-1]}')
plt.show()

#--Feature Analysis Function--#
def get_feature_words(text_series, top_n=15):
    all_words = []
    for text in text_series:
        words = re.findall(r'\b\w+\b', str(text).lower())
        all_words.extend(words)
    
    ignored = {'to', 'i', 'the', 'you', 'a', 'u', 'and', 'is', 'in', 'me', 'my', 'for', 'your', 'it', 'of', 'have', 'are', 'this', 'on'}
    filtered = [w for w in all_words if w not in ignored and len(w) > 2]
    return Counter(filtered).most_common(top_n)

# Lấy từ đặc trưng dựa trên cột đã nhận diện được
spam_features = get_feature_words(X[Y == 'spam'])
ham_features = get_feature_words(X[Y == 'ham'])

#--Table 2: Statistical Analysis--#
print("\nTable 2: Statistical Analysis of Spam and Ham Content Features")
print("="*55)
print(f"{'TOP SPAM WORDS':<25} | {'TOP HAM WORDS':<25}")
print("="*55)

# Lấy độ dài tối thiểu để tránh lỗi index
min_len = min(len(spam_features), len(ham_features), 15)
for i in range(min_len):
    s_feat = f"{spam_features[i][0]} ({spam_features[i][1]})"
    h_feat = f"{ham_features[i][0]} ({ham_features[i][1]})"
    print(f"{s_feat:<25} | {h_feat:<25}")
print("="*55)

#--Final Performance Showcase--#
accuracy = accuracy_score(Y_test, Y_pred)
precision = precision_score(Y_test, Y_pred, pos_label='spam', zero_division=0)
recall = recall_score(Y_test, Y_pred, pos_label='spam', zero_division=0)
f1 = f1_score(Y_test, Y_pred, pos_label='spam', zero_division=0)
avg_time_per_msg = test_time / len(X_test)

print("\n" + "="*55)
print(f"{'FINAL PERFORMANCE DATA (MULTINOMIAL NAIVE BAYES)':^55}")
print("="*55)
print(f"{'METRIC TYPE':<25} | {'VALUE':<25}")
print("-" * 55)
print(f"{'1. Overall Accuracy':<25} | {accuracy:.4%}")
print(f"{'2. Precision (Spam)':<25} | {precision:.4f}")
print(f"{'3. Recall (Spam)':<25} | {recall:.4f}")
print(f"{'4. F1-Score (Spam)':<25} | {f1:.4f}")
print("-" * 55)
print(f"{'5. Training Time':<25} | {train_time:.6f} s")
print(f"{'6. Total Testing Time':<25} | {test_time:.6f} s")
print(f"{'7. Avg Time per Msg':<25} | {avg_time_per_msg:.6f} s")
print("="*55)