from sklearn.svm import SVR
from sklearn.svm import SVC

def SVR_model(X_train, y_train, kernel='rbf', C=1.0, epsilon=0.1):
    svr = SVR(kernel=kernel, C=C, epsilon=epsilon)
    svr.fit(X_train, y_train)
    return svr

def SVC_model(X_train, y_train, kernel='rbf', C=1.0):
    svc = SVC(kernel=kernel, C=C)
    svc.fit(X_train, y_train)
    return svc