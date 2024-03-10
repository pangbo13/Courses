import numpy as np
from sklearn.base import ClassifierMixin,BaseEstimator
from multiprocessing import Pool

class SVM(ClassifierMixin,BaseEstimator):
    def __init__(self, lr=0.001, C=1.0, n_iters=100):
        self.lr = lr
        self.C = C
        self.n_iters = n_iters
        self.w = None
        self.b = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        y_ = np.where(y <= 0, -1, 1)
        self.w = np.zeros(n_features)
        self.b = 0

        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                condition = y_[idx] * (np.dot(x_i, self.w) - self.b) >= 1
                if condition:
                    self.w -= self.lr * (2 * self.w)
                else:
                    self.w -= self.lr * (2 * self.w - self.C * np.dot(x_i, y_[idx]))
                    self.b -= self.lr * self.C * y_[idx]

    def predict_prob(self, X):
        linear_output = np.dot(X, self.w) - self.b
        return linear_output
    
    def predict(self, X):
        return np.sign(self.predict_prob(X))

class MultiClassSVM(ClassifierMixin,BaseEstimator):
    def __init__(self, C = 1.0, lr=0.1):
        self.C = C
        self.clfs = []
        self.lr = lr

    def _fit_binary(self, X, y, c):
        y_binary = np.where(y == c, 1, -1)
        clf = SVM(C=self.C, lr=self.lr)
        clf.fit(X, y_binary)
        return clf
    
    def fit(self, X, y, n_jobs=1):
        self.classes = np.unique(y)
        if n_jobs == 1:
            for c in self.classes:
                clf = self._fit_binary(X, y, c)
                self.clfs.append(clf)
        elif n_jobs > 1:
            with Pool(n_jobs) as p:
                data = [(X, y, c) for c in self.classes]
                self.clfs = p.starmap(self._fit_binary, data)

    def predict(self, X):
        predictions = np.zeros((X.shape[0], len(self.classes)))
        for i, clf in enumerate(self.clfs):
            predictions[:, i] = clf.predict_prob(X)
        return self.classes[np.argmax(predictions, axis=1)]
