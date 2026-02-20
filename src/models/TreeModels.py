from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

def decision_tree_model(X_train, y_train):
    dt = DecisionTreeClassifier()
    dt.fit(X_train, y_train)
    return dt

def random_tree_model(X_train, y_train):
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(X_train, y_train)
    return rf