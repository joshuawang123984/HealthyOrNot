from sklearn.svm import SVR

def SVR_model(X_train, y_train, kernel='rbf', C=1.0, epsilon=0.1):
    svr = SVR(kernel=kernel, C=C, epsilon=epsilon)
    svr.fit(X_train, y_train)
    return svr