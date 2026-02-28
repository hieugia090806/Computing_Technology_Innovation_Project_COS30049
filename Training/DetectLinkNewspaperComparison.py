import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from DetectLinknewspaperSVM import detect_newspaper_link_svm_model
from DetectLinkNewspaperRandomForest import detect_newspaper_link_random_forest
from DetectLinkNewspaperLogisticsRegression import detect_newspaper_link_logistic_regression

df = pd.read_csv("../Data/LinksDataset01.csv")

print("Columns found:", df.columns.tolist())
url_col = None
for col in df.columns:
    if df[col].dtype == "object":
        if df[col].str.contains("http", na=False).sum() > 0:
            url_col = col
            break

if url_col is None:
    raise Exception("❌ Not found URL Column")

label_col = None
for col in df.columns:
    if col != url_col:
        if df[col].nunique() <= 5:  # thường binary
            label_col = col
            break

if label_col is None:
    raise Exception("❌ Không tìm thấy cột label")

print("Detected URL column:", url_col)
print("Detected Label column:", label_col)
#--Prepare data--#
X = df[url_col]
y = df[label_col]

vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2,4))
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)
#--Compare Model--#
print("\n===== Model Comparison =====")

print("Logistic:", round(detect_newspaper_link_logistic_regression(X_train, X_test, y_train, y_test), 4))
print("SVM:", round(detect_newspaper_link_svm_model(X_train, X_test, y_train, y_test), 4))
print("Random Forest:", round(detect_newspaper_link_random_forest(X_train, X_test, y_train, y_test), 4))
