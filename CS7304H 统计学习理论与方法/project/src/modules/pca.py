import numpy as np

class PCA:
    def __init__(self, n_components):
        self.n_components = n_components
        self.components = None
        self.mean = None

    def fit(self, X):
        self.mean = np.mean(X, axis=0)
        X = X - self.mean
        cov = np.cov(X.T)

        eigenvalues, eigenvectors = np.linalg.eig(cov)

        idx = np.argsort(eigenvalues)[::-1]
        eigenvectors = eigenvectors[:,idx]

        self.components = eigenvectors[0:self.n_components].real

    def transform(self, X):
        X = X - self.mean
        return np.dot(X, self.components.T)