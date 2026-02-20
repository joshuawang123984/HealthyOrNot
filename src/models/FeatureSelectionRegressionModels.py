from sklearn.linear_model import Ridge, Lasso

def ridge_model(X_train, y_train, alpha):
    ridge = Ridge(alpha=alpha) 
    ridge.fit(X_train, y_train)
    return ridge

def lasso_model(X_train, y_train, alpha):
    lasso = Lasso(alpha=alpha) 
    lasso.fit(X_train, y_train)
    return lasso