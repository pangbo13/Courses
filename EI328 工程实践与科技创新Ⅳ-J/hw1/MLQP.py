import numpy as np
import optimizer
import copy

np.random.seed(42)
class MLQP():
    @staticmethod
    def sigmoid(z):
        try:
            return 1/(1 + np.exp(-z))
        except:
            print(z)

    def __init__(self,in_dim,out_dim,hidden_layer_dims = [],_optimizer = optimizer.SGD, model_name = "model"):
        self.checkpoint = None
        self.dims = [in_dim]+list(hidden_layer_dims)+[out_dim]
        self.layers_nr = len(self.dims)
        self.model_name = model_name

        #Xavier Initialization: https://zhuanlan.zhihu.com/p/64464584
        self.Uk = [None for _ in range(self.layers_nr)]
        self.Vk = [None for _ in range(self.layers_nr)]
        self.Bk = [None for _ in range(self.layers_nr)]
        for layer_id in range(self.layers_nr-1,0,-1):
            self.Uk[layer_id] = np.random.normal(0,2/(self.dims[layer_id]+self.dims[0]),(self.dims[layer_id],self.dims[layer_id-1]))
            self.Vk[layer_id] = np.random.normal(0,2/(self.dims[layer_id]+self.dims[0]),(self.dims[layer_id],self.dims[layer_id-1]))
            self.Bk[layer_id] = np.random.normal(0,2/(self.dims[layer_id]+self.dims[0]),(self.dims[layer_id],1))
        
        self.Yk = [None for _ in range(self.layers_nr)]
        self.Tk = [None for _ in range(self.layers_nr)]
        for layer_id in range(self.layers_nr):
            self.Yk[layer_id] = np.zeros((self.dims[layer_id],1))
            self.Tk[layer_id] = np.zeros((self.dims[layer_id],1))

        self.DeltaK = [None for _ in range(self.layers_nr)]
        for layer_id in range(self.layers_nr):
            self.DeltaK[layer_id] = np.zeros((self.dims[layer_id],1))
        
        self.tag = np.zeros((self.dims[-1],1))

        self.optimizer = _optimizer(self)

    def forward(self):
        for layer_id in range(1,self.layers_nr):
            self.Tk[layer_id] = np.matmul(self.Uk[layer_id],np.square(self.Yk[layer_id-1])) + np.matmul(self.Vk[layer_id],self.Yk[layer_id-1]) + self.Bk[layer_id]
            self.Yk[layer_id] = self.sigmoid(self.Tk[layer_id])

    def backward(self):
        # 输出层参数梯度
        # sigmoid'(x) = sigmoid(x)[1-sigmoid(x)]

        # MSE损失函数
        # self.DeltaK[-1] = (self.Yk[-1] - self.tag) * self.Yk[-1] * (np.ones_like(self.Yk[-1])-self.Yk[-1])

        # 交叉熵损失函数
        # if self.tag[0] > 0.5:
        #     self.DeltaK[-1] = -1 / np.clip(self.Yk[-1],1e-12,1-1e-12)  * self.Yk[-1] * (np.ones_like(self.Yk[-1])-self.Yk[-1])
        # else:
        #     self.DeltaK[-1] = 1 / np.clip((1 - self.Yk[-1]),1e-12,1-1e-12) * self.Yk[-1] * (np.ones_like(self.Yk[-1])-self.Yk[-1])

        # 交叉熵优化版本，利用临时变量缓存减少指数运算
        # 因为这里输出层维度低，所以没降低多少复杂度
        self.DeltaK[-1] = self.Yk[-1] - self.tag

        for layer_id in range(self.layers_nr-2,0,-1):
            self.DeltaK[layer_id] = np.matmul((self.Uk[layer_id+1].T*self.Yk[layer_id]*2+self.Vk[layer_id+1].T),self.DeltaK[layer_id+1]) \
                * self.Yk[layer_id] \
                * (np.ones_like(self.Yk[layer_id])-self.Yk[layer_id])
            
    def update(self,lr = 0.001,*args,**argv):
        self.optimizer.update(lr,*args,**argv)


    def __set_input_layer(self,_input_vector):
        self.Yk[0][:,0] =  np.array(_input_vector).reshape((self.dims[0],1))[:,0]

    def __set_tag(self,_tag):
        self.tag[:,0]  = np.array(_tag).reshape((self.dims[-1],1))[:,0]

    def __get_output_layer(self):
        return self.Yk[-1][:,0]
    
    def input_sample(self,_input_vector,_tag):
        self.__set_tag(_tag)
        self.__set_input_layer(_input_vector)
    
    def output_prediction(self):
        return self.__get_output_layer()
    
    def loss(self):
        return -np.mean(self.Yk[-1]*np.log(np.clip(self.tag,1e-10,1-1e-10))\
            + ( 1 - self.Yk[-1])*np.log(np.clip(1 - self.tag,1e-10,1-1e-10)))
        # return 0.5*np.sum(np.square(self.Yk[-1]-self.tag))

    def save(self,path = None):
        if path is None:
            path = self.model_name + ".npz"
        argv = {}
        argv['model_name'] = np.array(self.model_name)
        argv["dims"] = np.array(self.dims,dtype=np.int32)
        for layer_id in range(1,self.layers_nr):
            argv["Uk"+str(layer_id)] = self.Uk[layer_id]
            argv["Vk"+str(layer_id)] = self.Vk[layer_id]
            argv["Bk"+str(layer_id)] = self.Bk[layer_id]
        np.savez(path,**argv)
        print(f"Model saved to {path}")
    
    def predict_prob(self,input_vector):
        self.__set_input_layer(input_vector)
        self.forward()
        return self.__get_output_layer()

    def predict(self,input_vector):
        if np.average(self.predict_prob(input_vector)) > 0.5:
            return 1
        else:
            return 0

    def create_checkpoint(self):
        self.checkpoint = {}
        self.checkpoint["Uk"] = copy.deepcopy(self.Uk)
        self.checkpoint["Vk"] = copy.deepcopy(self.Vk)
        self.checkpoint["Bk"] = copy.deepcopy(self.Bk)

    def restore_checkpoint(self):
        if self.checkpoint is not None:
            self.Uk = copy.deepcopy(self.checkpoint["Uk"])
            self.Vk = copy.deepcopy(self.checkpoint["Vk"])
            self.Bk = copy.deepcopy(self.checkpoint["Bk"])

    @classmethod
    def load(cls,path):
        argv = np.load(path)
        model = cls(argv["dims"][0],argv["dims"][-1],argv["dims"][1:-1],
            model_name = argv["model_name"].tostring().decode() if "model_name" in argv else "model")
        for layer_id in range(1,model.layers_nr):
            model.Uk[layer_id] = argv["Uk"+str(layer_id)]
            model.Vk[layer_id] = argv["Vk"+str(layer_id)]
            model.Bk[layer_id] = argv["Bk"+str(layer_id)]
        return model

if __name__ == "__main__":
    m = MLQP(2,1,[16,32,16])
    m.input_sample([1,2],1)
    m.forward()
    print(m.output_prediction())
    for _ in range(1000):
        m.backward()
        m.update()
        m.forward()
        if not _%10:
            print(m.output_prediction())
    print(m.output_prediction())
    m.save("model.npz")