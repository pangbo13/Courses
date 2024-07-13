import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def F_hat(X):
    return (np.percentile(X, 0.75) - np.percentile(X, 0.25))/1.34

def bootstrap(real_X, B=10000):
    F_hat_ = np.zeros(B)
    for b in range(B):
        X = np.random.choice(real_X, len(real_X), replace=True)
        F_hat_[b] = F_hat(X)
    return F_hat_

def norm_interval(F_hat_, alpha=0.05):
    se = np.std(F_hat_)
    mean = np.mean(F_hat_)
    z = norm.ppf(1-alpha/2)
    return mean - z*se, mean + z*se

def percentile_interval(F_hat, alpha=0.05):
    return np.percentile(F_hat, 100*alpha/2), np.percentile(F_hat, 100*(1-alpha/2))

def pivot_interval(F_hat_, alpha=0.05):
    return 2*np.mean(F_hat_) - np.percentile(F_hat_, 100*(1-alpha/2)), 2*np.mean(F_hat_) - np.percentile(F_hat_, 100*alpha/2)

real_X = np.random.standard_t(3, (25,))
F_hat_ = bootstrap(real_X)

print(np.mean(F_hat_))
print(norm_interval(F_hat_))
print(pivot_interval(F_hat_))
print(percentile_interval(F_hat_))

def plot_intervals(interval_func: callable):
    interval_upper = []
    interval_lower = []
    for end in range(50, 10000, 50):
        upper, lower = interval_func(F_hat_[:end])
        interval_upper.append(upper)
        interval_lower.append(lower)
    plt.fill_between(range(50, 10000, 50), interval_upper, interval_lower, alpha=0.3, label=interval_func.__name__)

def plot_mean():
    mean = []
    for end in range(50, 10000, 50):
        mean.append(np.mean(F_hat_[:end]))
    plt.plot(range(50, 10000, 50), mean, label='mean')

plot_intervals(norm_interval)
plot_intervals(percentile_interval)
plot_intervals(pivot_interval)
plot_mean()

plt.legend()
# plt.ylim(0, 4)
plt.show()