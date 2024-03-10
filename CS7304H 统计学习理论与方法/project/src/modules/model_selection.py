import numpy as np
from copy import deepcopy
import itertools

class BaseModelAssessment:
    def __init__(self, estimator, n_folds=5):
        self.estimator = estimator
        self.n_folds = n_folds
    
    def split_data(self, X, y):
        raise NotImplementedError
    
    def fit(self, X, y, **kwargs):
        self.estimators_result = []
        for X_train, X_test, y_train, y_test in self.split_data(X, y):
            estimator = deepcopy(self.estimator)
            estimator.fit(X_train, y_train, **kwargs)
            self.estimators_result.append((estimator.predict(X_test)==y_test).mean())
        return self
    
    def get_result(self):
        return self.estimators_result

class CrossValidate(BaseModelAssessment):
    def split_data(self, X, y):
        indices = np.arange(len(X))
        np.random.shuffle(indices)
        indices = np.array_split(indices, self.n_folds)
        for i in range(self.n_folds):
            train_indices = np.concatenate(indices[:i] + indices[i+1:])
            test_indices = indices[i]
            yield X[train_indices], X[test_indices], y[train_indices], y[test_indices]

class BootStrap(BaseModelAssessment):
    def split_data(self, X, y):
        indices = np.arange(len(X))
        for i in range(self.n_folds):
            train_indices = np.random.choice(indices, int(len(indices) * (1-1/self.n_folds)))
            test_indices = np.setdiff1d(indices, train_indices)
            yield X[train_indices], X[test_indices], y[train_indices], y[test_indices]

class GridSearch:
    def __init__(self, estimator, param_grid, n_folds=5):
        self.estimator = estimator
        self.param_grid = param_grid
        self.param_names = list(param_grid.keys())
        self.n_folds = n_folds
    
    def get_params_product(self):
        for params in itertools.product(*self.param_grid.values()):
            yield dict(zip(self.param_names, params))

    def set_params(self, estimator, params):
        for param_name, param_value in params.items():
            assert hasattr(estimator, param_name), f"Estimator has no attribute {param_name}"
            setattr(estimator, param_name, param_value)

    def fit(self, X, y, **kwargs):
        self.results = []
        for params in self.get_params_product():
            estimator = deepcopy(self.estimator)
            self.set_params(estimator, params)
            cv = CrossValidate(estimator, self.n_folds)
            cv.fit(X, y, **kwargs)
            self.results.append((params, np.mean(cv.estimators_result)))
        self.best_params, self.best_score = max(self.results, key=lambda x: x[1])
        return self.best_params
