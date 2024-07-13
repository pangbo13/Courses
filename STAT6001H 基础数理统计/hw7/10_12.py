import numpy as np
from scipy.stats import norm

lambda_ = 1
n = 20

lower_bound = lambda_ - norm.ppf(1 - 0.05/2) * np.sqrt(lambda_/n)
upper_bound = lambda_ + norm.ppf(1 - 0.05/2) * np.sqrt(lambda_/n)

# poisson distribution
X = np.random.poisson(lambda_, (100000,n))

lambda_hat = np.mean(X, axis=1)

error_rate = np.mean((lambda_hat < lower_bound) | (lambda_hat > upper_bound))

print(error_rate)