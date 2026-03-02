from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

def decision_tree_classifier(X_train, y_train):
    dtc = DecisionTreeClassifier(random_state=42)
    dtc.fit(X_train, y_train)
    return dtc

def decision_tree_regressor(X_train, y_train):
    dtr = DecisionTreeRegressor(random_state=42)
    dtr.fit(X_train, y_train)

    return dtr