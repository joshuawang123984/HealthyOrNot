from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

def knn_classifier(X_train, y_train, n_neighbors=5):
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(X_train, y_train)
    
    return model