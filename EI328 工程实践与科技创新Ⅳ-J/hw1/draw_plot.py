import scipy.io
import numpy as np
import matplotlib.pyplot as plt

def draw_logging_plot(ax1,epochs,loss,train_acc,val_acc):
    # 参考自matplotlib官方文档，https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html
    ax1.set_xlabel('epochs')
    ax1.set_ylabel('acc')
    ax1.plot(epochs, train_acc,'r',linewidth=0.5)
    ax1.plot(epochs, val_acc,'b',linewidth=0.5)
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    ax2.set_ylabel('loss')  # we already handled the x-label with ax1
    ax2.plot(epochs, loss,'k',linewidth=0.5)
    ax2.tick_params(axis='y')

def draw_single_logging_plot(datapath):
    epochs,loss,train_acc,val_acc = load_logging_data(datapath)
    fig, ax1 = plt.subplots()
    fig.set_size_inches(16,8)
    fig.set_dpi(80)
    draw_logging_plot(ax1,epochs,loss,train_acc,val_acc)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

def draw_multi_logging_plot(datapaths):
    fig = plt.figure(figsize=(10,40), dpi=80)
    plots_nr = len(datapaths)
    for i in range(plots_nr):
        epochs,loss,train_acc,val_acc = load_logging_data(datapaths[i])
        ax1 = plt.subplot(plots_nr,1,i+1)
        draw_logging_plot(ax1,epochs,loss,train_acc,val_acc)
    fig.tight_layout(h_pad=4)
    fig.subplots_adjust(bottom=0.03)
    # plt.tight_layout()
    plt.show()

def load_logging_data(path):
    logging_data = scipy.io.loadmat(path)
    epochs = logging_data['epochs'].reshape(-1)
    loss = logging_data['loss'].reshape(-1)
    train_acc = logging_data['train_acc'].reshape(-1)
    val_acc = logging_data['val_acc'].reshape(-1)
    return epochs,loss,train_acc,val_acc


# draw_single_logging_plot('logging.mat')
# draw_multi_logging_plot(['logging.mat']*4)
if __name__ == '__main__':
    draw_multi_logging_plot(["logging_axis_minmax_"+dname+".mat" for dname in ["1p2p","1p2n","1n2p","1n2n"]])
    