import numpy as np
from sklearn.base import ClassifierMixin,BaseEstimator

class LogisticRegression(ClassifierMixin,BaseEstimator):
    def __init__(self, lr=0.01, n_iters=100000):
        self.lr = lr
        self.n_iters = n_iters
    
    def softmax(self, z):
        exp = np.exp(z)
        return exp / np.sum(exp, axis=1, keepdims=True)
    
    def to_one_hot(self, y):
        n_classes = len(np.unique(y))
        m = y.shape[0]
        one_hot = np.zeros((m, n_classes))
        one_hot[np.arange(m), y] = 1
        return one_hot
    
    def fit(self, X, y):
        y = self.to_one_hot(y)
        
        self.beta = np.zeros((X.shape[1], y.shape[1]))
        self.bias = np.zeros((1, y.shape[1]))
        
        for i in range(self.n_iters):
            z = np.dot(X, self.beta) + self.bias
            h = self.softmax(z)
            
            gradient = np.dot(X.T, (h - y)) / y.size
            self.beta -= self.lr * gradient
            self.bias -= self.lr * np.mean(h - y)
    
    def predict_prob(self, X):
        return self.softmax(np.dot(X, self.beta) + self.bias)
    
    def predict(self, X):
        return np.argmax(self.predict_prob(X), axis=1)
