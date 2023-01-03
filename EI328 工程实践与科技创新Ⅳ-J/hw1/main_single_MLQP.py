from MLQP import MLQP

import optimizer
import numpy as np
from train import train
from callbacks import *
from dataloader import load_data

EPOACHS = 2000

# load dataset
train_data,test_data = load_data('data/two_spiral_train_data.txt','data/two_spiral_test_data.txt')


TRAIN_MODEL = True
if TRAIN_MODEL:
    # create callbacks
    callback_epochs_logging = CallbackEpochsLogging(EPOACHS)
    callback_save_process_model = CallbackSaveProcessModel(250)
    callback_epochs_info_display = CallbackEpochsInfoDisplay()
    # train model
    model = MLQP(2,1,[50],optimizer.SGDM,model_name="model")
    train(model,train_data,test_data,epochs=2000,init_lr=0.1,callbacks=[callback_epochs_logging,callback_epochs_info_display,callback_save_process_model])
    callback_epochs_logging.save('MLQP_logging.mat')
else:
    # load model
    model = MLQP.load('model.npz')

# draw boundary
DRAW_BOUNDARY = True
if DRAW_BOUNDARY:
    from draw_boundary import draw_single_boundary
    draw_single_boundary(model,train_data,test_data)

# draw ROC curve
DRAW_ROC = True
if DRAW_ROC:
    from draw_ROC import draw_multi_ROC
    models = [MLQP.load(f"model_{e*250}.npz") for e in range(1,9)]
    labels = [f"{e*250} Epochs" for e in range(1,9)]
    draw_multi_ROC(test_data,models,labels,"ROC Curves (CrossEntropy)")

# draw Logging plot
DRAW_LOGGING = True
if DRAW_LOGGING:
    from draw_plot import draw_single_logging_plot
    draw_single_logging_plot("MLQP_logging.mat")

# draw process model boundary
DRAW_PROCESS_MODEL = True
if DRAW_PROCESS_MODEL:
    from draw_boundary import draw_multi_boundary
    models = [MLQP.load(f'model_{i*500}.npz') for i in range(1,5)]
    titles = [f'{i*500} Epochs' for i in range(1,5)]
    draw_multi_boundary(models,train_data,test_data,titles)
