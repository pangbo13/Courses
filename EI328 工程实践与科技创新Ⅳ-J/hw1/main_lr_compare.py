from MLQP import MLQP
from dataloader import load_data
import optimizer
import numpy as np
from train import train
from callbacks import *
import scipy.io

EPOACHS = 1000

# load dataset
train_data,test_data = load_data('data/two_spiral_train_data.txt','data/two_spiral_test_data.txt')

lrs = [0.1,0.01,0.001]

TRAIN_MODEL = True
if TRAIN_MODEL:
    models = [MLQP(2,1,[50],optimizer.SGDM,model_name=f"model_lr_{lrs[i]}") for i in range(len(lrs))]
    for i in range(len(lrs)):
        print(f"Current lr = {lrs[i]}")
        # create callbacks
        callback_epochs_logging = CallbackEpochsLogging(EPOACHS)
        callback_epochs_info_display = CallbackEpochsInfoDisplay(100)
        # train model
        train(models[i],train_data,test_data,epochs=EPOACHS,init_lr=lrs[i],callbacks=[callback_epochs_logging,callback_epochs_info_display],lr_decrese_rate=1)
        callback_epochs_logging.save(f'MLQP_logging_lr{lrs[i]}.mat')
else:
    # load model
    models = [MLQP.load('model_lr_{lrs[i]}.npz') for i in range(len(lrs))]

# draw boundary
DRAW_BOUNDARY = True
if DRAW_BOUNDARY:
    from draw_boundary import draw_multi_boundary
    draw_multi_boundary(models,train_data,test_data,[f"lr={lr}" for lr in lrs])

# draw Logging plot
DRAW_LOGGING = True
if DRAW_LOGGING:
    from draw_plot import draw_multi_logging_plot
    draw_multi_logging_plot([f"MLQP_logging_lr{lrs[i]}.mat" for i in range(len(lrs))])

