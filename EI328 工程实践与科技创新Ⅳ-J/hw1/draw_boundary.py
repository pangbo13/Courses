from MLQP import  MLQP
import matplotlib.pyplot as plt
import numpy as np
from dataloader import load_data

def draw_boundary(ax,model,train_data,test_data,resolution = 200,title = ""):
    X, Y = np.meshgrid(np.linspace(-1, 1, resolution), np.linspace(-1, 1, resolution))
    Z = np.apply_along_axis(lambda x:model.predict(x),2,np.concatenate((X[:,:,None],Y[:,:,None]),axis=2))
    ax.set_facecolor('grey')
    ax.set_xticks(np.linspace(0, resolution - 1, 13))
    ax.set_yticks(np.linspace(0, resolution - 1, 13))
    ax.set_xticklabels(np.arange(-6, 7, 1))
    ax.set_yticklabels(np.arange(6, -7, -1))
    ax.set_xlim(0, resolution)
    ax.set_ylim(0, resolution)
    ax.imshow(Z,cmap=plt.cm.gray)
    ax.set_title(title,y=-0.2)
    if test_data is not None:
        for sample in test_data:
            if sample[-1] == 1:
                color = 'red'
            else:
                color = 'blue'
            ax.scatter(*(sample[:2]*resolution/2+resolution/2), c=color, s=10)

def draw_single_boundary(model,train_data,test_data,title = ""):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    draw_boundary(ax,model,train_data,test_data,title = title)
    plt.show()

def draw_multi_boundary(models,train_data,test_data,titles,figsize=(20,8)):
    # fig = plt.figure()
    fig = plt.figure(figsize=figsize, dpi=80)
    for i in range(len(models)):
        ax = plt.subplot(1,len(models),i+1)
        draw_boundary(ax,models[i],train_data,test_data,title = titles[i])
    plt.show()

if __name__ == '__main__':
    train_data,test_data = load_data('data/two_spiral_train_data.txt','data/two_spiral_test_data.txt')
    models = [MLQP.load(f'model_{i*500}.npz') for i in range(1,5)]
    titles = [f'{i*500} Epochs' for i in range(1,5)]
    draw_multi_boundary(models,train_data,test_data,titles)
# # fig = plt.gcf()
# fig = plt.figure(figsize=(20,8), dpi=80)
# for i in range(1,5):
#     model = MLQP.load(f'model_{i*500}.npz')
#     ax = plt.subplot(1,4,i)
#     draw_boundary(ax,model,train_data,test_data,title=f'{i*500} Epochs')

# plt.show()

