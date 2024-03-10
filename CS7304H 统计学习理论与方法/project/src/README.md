# README

## 文件目录

```
│  demo.ipynb
|  demo.py
│  README.md
│
└─modules
    │  logistic_regression.py
    │  logistic_regression_cuda.py
    │  model_selection.py
    │  nn.py
    │  pca.py
    │  svm.py
```

## 文件说明

demo.ipynb: 用于演示的notebook文件。

算法实现位于`modules`目录下：

* logistic_regression.py：逻辑回归算法实现，包含LogisticRegression类
* logistic_regression_cuda.py：逻辑回归算法CUDA实现，包含LogisticRegression类
* nn.py：神经网络算法实现，包含NNEstimator类
* svm.py：支持向量机算法实现，包含SVM与MultiClassSVM类
* pca.py：主成分分析算法实现，包含PCA类
* model_selection.py：模型选择算法实现，包含CrossValidate、BootStrap类用于模型评估，GridSearch类用于模型参数搜索