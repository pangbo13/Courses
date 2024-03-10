# %%
import numpy as np
import pandas as pd
import pickle

from modules.logistic_regression_cuda import LogisticRegression
from modules.nn import NNEstimator
from modules.svm import MultiClassSVM
from modules.pca import PCA
from modules.model_selection import CrossValidate, GridSearch, BootStrap

# %%
# load data
with open('../data/train_feature.pkl', 'rb') as f:
    dataset_feature = pickle.load(f)
    dataset_feature = np.array(dataset_feature.todense()) # (11314, 10000)
dataset_label = np.load('../data/train_labels.npy') # (11314,)

with open('../data/test_feature.pkl', 'rb') as f:
    test_feature = pickle.load(f)
    test_feature = np.array(test_feature.todense()) # (7532, 10000)

# %% [markdown]
# ## SVM

# %%
lambda_ = 1 / 1e7
svm = MultiClassSVM(C=1/lambda_, lr=lambda_)
svm.fit(dataset_feature, dataset_label, n_jobs=20)

# %%
svm_pred = svm.predict(test_feature)
pd.DataFrame({'ID': np.arange(0, len(svm_pred)), 'label': svm_pred}).to_csv('submit_SVM.csv', index=False)

# %% [markdown]
# ## Logistic Regression
# 
#     We use CUDA to accelerate the training process by default. If CUDA is not available, use `from modules.logistic_regression import LogisticRegression` instead.

# %%
# if cuda is not available:
# from modules.logistic_regression import LogisticRegression

lr = LogisticRegression(lr=100, n_iters=1000)
lr.fit(dataset_feature, dataset_label)
print("train accuracy: ", lr.score(dataset_feature, dataset_label))

# %%
lr_pred = lr.predict(test_feature)
pd.DataFrame({'ID': np.arange(0, len(lr_pred)), 'label': lr_pred}).to_csv('submit_LR.csv', index=False)

# %% [markdown]
# ## Nerual Network
# 

# %%
nn_net = NNEstimator(weight_decay=1e-7,hidden_size=1024,drop_rate=0.9,lr=1e-3,epoch_num=20) 
nn_net.fit(dataset_feature, dataset_label)
print("train accuracy: ", nn_net.score(dataset_feature, dataset_label))

# %%
nn_pred = nn_net.predict(test_feature)
pd.DataFrame({'ID': np.arange(0, len(nn_pred)), 'label': nn_pred}).to_csv('submit_NN.csv', index=False)

# %% [markdown]
# ## Model Selection

# %%
## Cross Validate

cv = CrossValidate(LogisticRegression(lr=100, n_iters=1000),n_folds=5)
cv.fit(dataset_feature, dataset_label)
print(cv.get_result())

# %%
## BootStrap

bs = BootStrap(LogisticRegression(lr=100, n_iters=1000),n_folds=5)
bs.fit(dataset_feature, dataset_label)
print(bs.get_result())

# %% [markdown]
# ## Model Search

# %%
param_grid = {
    'lr':[1e-4,1e-5,1e-6,1e-7],
    'C':[1e4,1e5,1e6,1e7],
}
gs_svm = GridSearch(MultiClassSVM(), param_grid, 5)
gs_svm.fit(dataset_feature, dataset_label, n_jobs=20)
gs_svm_results_df = pd.DataFrame(columns=list(param_grid.keys())+['score'])
for params, score in gs_svm.results:
    gs_svm_results_df = gs_svm_results_df.append(pd.Series({**params, 'score': score}), ignore_index=True)
gs_svm_results_df

# %%
param_grid = {
    'lr': [1e-3],
    'drop_rate':[0.7,0.8,0.9],
    'hidden_size':[1024, 1024+512, 2048,],
    'epoch_num':[15,20,25], 
    'weight_decay':[0,1e-7,1e-6,1e-5]
}
gs_nn = GridSearch(NNEstimator(), param_grid, 5)
gs_nn.fit(dataset_feature, dataset_label)
gs_nn_results_df = pd.DataFrame(columns=list(param_grid.keys())+['score'])
for params, score in gs_nn.results:
    gs_nn_results_df = gs_nn_results_df.append(pd.Series({**params, 'score': score}), ignore_index=True)
gs_nn_results_df


# %%
param_grid = {
    'lr': [0.1, 1, 10, 100, 1000],
    'n_iters': [1000, 2000],
}
gs_lr = GridSearch(LogisticRegression(), param_grid, 5)
gs_lr.fit(dataset_feature, dataset_label)
gs_lr_results_df = pd.DataFrame(columns=list(param_grid.keys())+['score'])
for params, score in gs_lr.results:
    gs_lr_results_df = gs_lr_results_df.append(pd.Series({**params, 'score': score}), ignore_index=True)
gs_lr_results_df

# %% [markdown]
# ## PCA

# %%
pca = PCA(n_components=5000)
pca.fit(dataset_feature)

# %%
dataset_feature_pca = pca.transform(dataset_feature)
test_feature_pca = pca.transform(test_feature)

# %%
lr_pca = LogisticRegression(lr=100, n_iters=1000)
lr_pca.fit(dataset_feature_pca, dataset_label)
print("train accuracy: ", lr_pca.score(dataset_feature_pca, dataset_label))
lr_pred_pca = lr_pca.predict(test_feature_pca)
pd.DataFrame({'ID': np.arange(0, len(lr_pred_pca)), 'label': lr_pred_pca}).to_csv('submit_LR_pca.csv', index=False)

# %%
svm_pca = MultiClassSVM(C=1e5, lr=1e-7)
svm_pca.fit(dataset_feature_pca, dataset_label, n_jobs=20)
print("train accuracy: ", svm_pca.score(dataset_feature_pca, dataset_label))
svm_pred_pca = svm_pca.predict(test_feature_pca)
pd.DataFrame({'ID': np.arange(0, len(svm_pred_pca)), 'label': svm_pred_pca}).to_csv('submit_SVM_pca.csv', index=False)

# %%
nn_pca = NNEstimator(weight_decay=1e-7,hidden_size=1024,drop_rate=0.9,lr=1e-3,epoch_num=20)
nn_pca.fit(dataset_feature_pca, dataset_label)
print("train accuracy: ", nn_pca.score(dataset_feature_pca, dataset_label))
nn_pred_pca = nn_pca.predict(test_feature_pca)
pd.DataFrame({'ID': np.arange(0, len(nn_pred_pca)), 'label': nn_pred_pca}).to_csv('submit_NN_pca.csv', index=False)


