#--For detecting link newspaper, may use the Linear Regression model--#
#--Import libraries--#
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
#--Main def--#
def detect_newspaper_link_logistic_regression(X_train, X_test, y_train, y_test):
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)
    return acc