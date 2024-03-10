
import numpy as np
import torch
from sklearn.base import ClassifierMixin,BaseEstimator

class LogisticRegression(ClassifierMixin,BaseEstimator):
    def __init__(self, lr=0.01, n_iters=1000):
        self.lr = lr
        self.n_iters = n_iters
    
    def to_one_hot(self, y):
        n_classes = len(np.unique(y))
        m = y.shape[0]
        one_hot = np.zeros((m, n_classes))
        one_hot[np.arange(m), y] = 1
        return one_hot
    
    @torch.no_grad()
    def fit(self, X, y):
        y = self.to_one_hot(y)

        X = torch.from_numpy(X).type(torch.float32).cuda()
        y = torch.from_numpy(y).type(torch.int32).cuda()
        
        self.beta = torch.zeros((X.shape[1], y.shape[1]), requires_grad=False, device='cuda')
        self.bias = torch.zeros((1, y.shape[1]), requires_grad=False, device='cuda')
        
        for i in range(self.n_iters):
            z = torch.mm(X, self.beta) + self.bias
            h = torch.softmax(z, dim=1)
            gradient = torch.mm(X.T,(h - y)) / y.size(0)
            self.beta -= self.lr * gradient
            self.bias -= self.lr * torch.mean(h - y, dim=0)
        
        self.beta = self.beta.cpu()
        self.bias = self.bias.cpu()
    
    @torch.no_grad()
    def predict_prob(self, X):
        X = torch.from_numpy(X).type(torch.float32)
        return torch.softmax(torch.mm(X,self.beta) + self.bias, dim=1).numpy()
    
    @torch.no_grad()
    def predict(self, X):
        return np.argmax(self.predict_prob(X), axis=1)
