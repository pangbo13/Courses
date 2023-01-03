import scipy.io
import numpy as np

class CallbackEpochsLogging(object):
    def __init__(self,epochs):
        self.epochs = epochs
        self.epochs_loggings = np.zeros((epochs,3),dtype=np.float32)
    def __call__(self,epoch_id,loss,train_acc,val_acc,**kwargs):
        self.epochs_loggings[epoch_id,0] = loss
        self.epochs_loggings[epoch_id,1] = train_acc
        self.epochs_loggings[epoch_id,2] = val_acc
    def save(self,path):
        logs_data = {
            'epochs':np.arange(self.epochs),
            'loss':self.epochs_loggings[:,0],
            'train_acc':self.epochs_loggings[:,1],
            'val_acc':self.epochs_loggings[:,2]
        }
        scipy.io.savemat(path,logs_data)

class CallbackSaveProcessModel(object):
    def __init__(self,interval = 500):
        self.interval = interval
    def __call__(self,epoch_id,model,**kwargs):
        if not (epoch_id+1) % self.interval:
            model.save(f"model_{epoch_id+1}.npz")

class CallbackEpochsInfoDisplay(object):
    def __init__(self,interval=1):
        self.interval = interval
    def __call__(self,epoch_id,lr,epoach_since_best,train_acc,val_acc,loss,**kwargs):
        if (epoch_id+1) % self.interval:
            return
        if val_acc is not None:
            print(f"epochs={epoch_id+1},train_acc={train_acc:.2f},test acc={val_acc:.2f},loss={loss:.4f},lr={lr:.4f},since best:{epoach_since_best}")
        else:
            print(f"epochs={epoch_id+1},train_acc={train_acc:.2f},loss={loss:.4f},lr={lr:.4f},since best:{epoach_since_best}")
