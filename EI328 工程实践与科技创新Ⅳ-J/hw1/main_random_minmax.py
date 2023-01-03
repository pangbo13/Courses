import MLQP
import optimizer
import numpy as np
from train import train
from callbacks import *
from dataloader import load_random_splited_data
from MinMaxMLQP import MinMaxMLQPPredictor

EPOACHS = 2000

train_data,test_data = load_random_splited_data('data/two_spiral_train_data.txt','data/two_spiral_test_data.txt')
data_1p2p,data_1p2n,data_1n2p,data_1n2n = train_data

model_dataset_name = ["1p2p","1p2n","1n2p","1n2n"]
TRAIN_MODEL = True
if TRAIN_MODEL:
    models = [MLQP.MLQP(2,1,[32],optimizer.SGDM,model_name=f"model_random_minmax_{model_dataset_name[i]}") for i in range(4)]

    for i in range(len(models)):
        print(f"Training model {model_dataset_name[i]}")
        callback_epochs_logging = CallbackEpochsLogging(EPOACHS)
        callback_epochs_info_display = CallbackEpochsInfoDisplay(100)
        train(models[i],train_data[i],None,epochs=EPOACHS,callbacks=[callback_epochs_logging,callback_epochs_info_display])
        callback_epochs_logging.save(f"logging_random_minmax_{model_dataset_name[i]}.mat")

    minmax_model = MinMaxMLQPPredictor(*models)
else:
    models = [MLQP.MLQP.load(f"model_random_minmax_{model_dataset_name[i]}.npz") for i in range(4)]
    minmax_model = MinMaxMLQPPredictor(*models)
# draw boundary
DRAW_BOUNDARY = True
if DRAW_BOUNDARY:
    from draw_boundary import draw_single_boundary
    draw_single_boundary(minmax_model,train_data,test_data)

# draw ROC curve
DRAW_ROC = True
if DRAW_ROC:
    from draw_ROC import draw_single_ROC
    draw_single_ROC(test_data,minmax_model,title="ROC Curves")

# draw Logging plot
DRAW_LOGGING = True
if DRAW_LOGGING:
    from draw_plot import draw_multi_logging_plot
    draw_multi_logging_plot(["logging_random_minmax_"+dname+".mat" for dname in model_dataset_name])

# draw process model boundary
DRAW_EACH_MODEL_BOUNDARY = True
if DRAW_EACH_MODEL_BOUNDARY:
    from draw_boundary import draw_multi_boundary
    draw_multi_boundary(models,None,None,model_dataset_name)