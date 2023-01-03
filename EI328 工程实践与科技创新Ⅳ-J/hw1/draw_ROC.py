from MLQP import MLQP
import numpy as np
from dataloader import load_data
import matplotlib.pyplot as plt

def calc_ROC(test_data,model):
    label = test_data[:,2].astype(np.bool)
    pred = np.apply_along_axis(lambda x:model.predict_prob(x),1,test_data[:,:2]).reshape(-1)
    X = np.zeros(101)
    Y = np.zeros_like(X)
    for i in range(101):
        threshold = 0+0.01*i
        true_pred = pred > threshold
        TP = np.count_nonzero(true_pred & label)
        FP = np.count_nonzero(true_pred & ~label)
        FN = np.count_nonzero(~true_pred & label)
        TN = np.count_nonzero(~true_pred & ~label)
        X[i] = FP/(FP+TN)
        Y[i] = TP/(TP+FN)
    return X,Y


# Y = [None for _ in range(4)]
def draw_multi_ROC(test_data,models,labels,title="",legend = True):
    for e in range(len(models)):
        model = models[e]
        X,Y = calc_ROC(test_data,model)
        plt.plot(X,Y,label=labels[e])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(title)
    if legend:
        plt.legend()
    plt.show()

def draw_single_ROC(test_data,model,label="",title=""):
    draw_multi_ROC(test_data,[model],[label],title,legend = False)

if __name__ == "__main__":
    train_data,test_data = load_data("data/two_spiral_train_data.txt","data/two_spiral_test_data.txt")
    del train_data
    # models = [MLQP.load(f"data/models/MSE/model_{e*250}.npz") for e in range(1,9)]
    models = [MLQP.load(f"model_{e*250}.npz") for e in range(1,9)]
    labels = [f"{e*250} Epochs" for e in range(1,9)]
    draw_multi_ROC(test_data,models,labels,"ROC Curves (CrossEntropy)")