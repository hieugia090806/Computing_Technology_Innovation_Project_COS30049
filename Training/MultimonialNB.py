#--Multimonial Naive Bayes Model--#
#--Import libraries--#
import time
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
#--Main def--#
def mulmonial_naive_bayes(X_train, X_test, Y_train, Y_test):
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    
    start = time.time()
    model.fit(X_train, Y_train)
    duration = time.time() - start
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(Y_test, y_pred)
    p, r, f1, _ = precision_recall_fscore_support(Y_test, y_pred, labels=['HAM', 'SPAM'])
    
    return {"acc": acc, "p": p[1], "r": r[1], "f1": f1[1], "time": duration}