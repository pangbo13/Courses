import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def F_hat(X):
    return np.max(X)

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

real_X = np.random.uniform(0, 1, (50,))
F_hat_ = bootstrap(real_X)
print(np.std(F_hat_))
print(np.mean(F_hat_))
print(norm_interval(F_hat_))
print(percentile_interval(F_hat_))
print(pivot_interval(F_hat_))

def plot_intervals(F_hat_, interval_func: callable):
    interval_upper = []
    interval_lower = []
    for end in range(50, 10000, 50):
        upper, lower = interval_func(F_hat_[:end])
        interval_upper.append(upper)
        interval_lower.append(lower)
    plt.fill_between(range(50, 10000, 50), interval_upper, interval_lower, alpha=0.3, label=interval_func.__name__)

def plot_mean(F_hat_):
    mean = []
    for end in range(50, 10000, 50):
        mean.append(np.mean(F_hat_[:end]))
    plt.plot(range(50, 10000, 50), mean, label='mean')

def plot_se(F_hat_):
    se = []
    for end in range(50, 10000, 50):
        se.append(np.std(F_hat_[:end]))
    plt.plot(range(50, 10000, 50), se, label='se')

plot_intervals(F_hat_, norm_interval)
plot_intervals(F_hat_, percentile_interval)
plot_intervals(F_hat_, pivot_interval)
plot_mean(F_hat_)
# plot_se(F_hat_)

plt.legend()
# plt.ylim(0, 4)
plt.show()

plt.hist(F_hat_, bins=50, range=(0.5,1), alpha=0.3, label='bootstrap')
plt.hist(
    np.random.uniform(0, 1, (50,10000)).max(axis=0),
    bins=50, range=(0.5,1) , alpha=0.3, label='real')
plt.legend()
plt.show()