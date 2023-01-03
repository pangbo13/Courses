import numpy as np
class SGD:
    def __init__(self, model):
        self.model = model
        self.detUk = [None for _ in range(model.layers_nr)]
        self.detVk = [None for _ in range(model.layers_nr)]
        self.detBk = [None for _ in range(model.layers_nr)]
        for layer_id in range(model.layers_nr-1,0,-1):
            self.detUk[layer_id] = np.zeros_like(model.Uk[layer_id])
            self.detVk[layer_id] = np.zeros_like(model.Vk[layer_id])
            self.detBk[layer_id] = np.zeros_like(model.Bk[layer_id])

    def reset(self):
        pass

    def update(self, lr = 0.01, *args, **kwargs):
        model = self.model
        for layer_id in range(1,model.layers_nr):
            self.detUk[layer_id] = np.square(model.Yk[layer_id-1]).T * model.DeltaK[layer_id]
            self.detVk[layer_id] = model.Yk[layer_id-1].T * model.DeltaK[layer_id]
            self.detBk[layer_id] = model.DeltaK[layer_id]
            model.Uk[layer_id] -= lr*self.detUk[layer_id]
            model.Vk[layer_id] -= lr*self.detVk[layer_id]
            model.Bk[layer_id] -= lr*self.detBk[layer_id]

class SGDM:
    def __init__(self, model):
        self.model = model
        self.detUk = [None for _ in range(model.layers_nr)]
        self.detVk = [None for _ in range(model.layers_nr)]
        self.detBk = [None for _ in range(model.layers_nr)]
        for layer_id in range(model.layers_nr-1,0,-1):
            self.detUk[layer_id] = np.zeros_like(model.Uk[layer_id])
            self.detVk[layer_id] = np.zeros_like(model.Vk[layer_id])
            self.detBk[layer_id] = np.zeros_like(model.Bk[layer_id])

    def reset(self):
        model = self.model
        for layer_id in range(model.layers_nr-1,0,-1):
            self.detUk[layer_id] = np.zeros_like(model.Uk[layer_id])
            self.detVk[layer_id] = np.zeros_like(model.Vk[layer_id])
            self.detBk[layer_id] = np.zeros_like(model.Bk[layer_id])

    def update(self, lr = 0.1, lr2 = 0.2, momentum = 0.9):
        model = self.model
        for layer_id in range(1,model.layers_nr):
            self.detUk[layer_id] = lr2*model.DeltaK[layer_id] * np.square(model.Yk[layer_id-1].T) + momentum*self.detUk[layer_id]
            self.detVk[layer_id] = lr*model.DeltaK[layer_id] * model.Yk[layer_id-1].T + momentum*self.detVk[layer_id]
            self.detBk[layer_id] = lr*model.DeltaK[layer_id] + momentum*self.detBk[layer_id]
            model.Uk[layer_id] -= self.detUk[layer_id]
            model.Vk[layer_id] -= self.detVk[layer_id]
            model.Bk[layer_id] -= self.detBk[layer_id]