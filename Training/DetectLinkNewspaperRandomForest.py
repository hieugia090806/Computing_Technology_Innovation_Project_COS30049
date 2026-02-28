#--Import libraries--#
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
#--Main def--#
def detect_newspaper_link_random_forest(X_train, X_test, y_train, y_test):
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)
    return acc