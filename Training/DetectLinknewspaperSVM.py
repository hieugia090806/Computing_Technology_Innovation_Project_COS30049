#--Detect Newspaper Link by using svm model--#
#--Import libraries--#
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
#--Main def--#
def detect_newspaper_link_svm_model(X_train, X_test, y_train, y_test):
    model = LinearSVC()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)
    return acc