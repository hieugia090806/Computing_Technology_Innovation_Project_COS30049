#--Import crucial libraries--#
import os
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
#--oad and Prepare Data--#
df = pd.read_csv('../Data/spam.csv', encoding='latin-1')
#--Data selection: v1 is the label, v2 is the message--#
X = df['v2']
Y = df['v1']
#--Split data into training and testing sets--#
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
#Training anf Predict
model = make_pipeline(CountVectorizer(), MultinomialNB())
model.fit(X_train, Y_train)
Y_pred = model.predict(X_test)
#--Showcase by using graph--#
cm = confusion_matrix(Y_test, Y_pred)
plt.figure(figsize=(7, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='YlGnBu', 
            xticklabels=['Ham', 'Spam'], 
            yticklabels=['Ham', 'Spam'])

plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('CONFUSION MATRIX: SPAM DETECTION SHOWCASE')
plt.show()
#--4. Professional Report Showcase--#
print("\n" + "="*40)
print("FINAL TRAINING RESULTS")
print("="*40)
print(f"Overall Accuracy: {accuracy_score(Y_test, Y_pred):.2%}")
print("-" * 40)
print("Detailed Metrics (Precision & Recall):")
print(classification_report(Y_test, Y_pred))
#--Add function to figure characeristics of spam and ham mail--#
def get_feature_words(text_series, top_n=15):
    all_words = []
    for text in text_series:
        words = re.findall(r'\b\w+\b', str(text).lower())
        all_words.extend(words)
    
    ignored = {'to', 'i', 'the', 'you', 'a', 'u', 'and', 'is', 'in', 'me', 'my', 'for', 'your', 'it', 'of', 'have'}
    filtered = [w for w in all_words if w not in ignored and len(w) > 2]
    return Counter(filtered).most_common(top_n)

spam_features = get_feature_words(df[df['v1'] == 'spam']['v2'])
ham_features = get_feature_words(df[df['v1'] == 'ham']['v2'])

print("Table 1: Statistical Analysis of Spam and Ham Content Features")
print("\n" + "="*50)
print(f"{'SPAM FEATURES':<25} | {'HAM FEATURES':<25}")
print("="*50)

for i in range(15):
    s_feat = f"{spam_features[i][0]} ({spam_features[i][1]})"
    h_feat = f"{ham_features[i][0]} ({ham_features[i][1]})"
    print(f"{s_feat:<25} | {h_feat:<25}")

print("="*50)