from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier

def random_forest_regressor_model(X_train, y_train):
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    return rf

def random_forest_classifier_model(X_train, y_train, n_estimators=100):
    rc = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    rc.fit(X_train, y_train)
    
    return rc