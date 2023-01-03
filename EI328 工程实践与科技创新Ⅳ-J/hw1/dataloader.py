import numpy as np

def load_axis_splited_data(path_train,path_test):
    train_data, test_data = load_data(path_train,path_test)
    class_1 = train_data[train_data[:,-1]==1]
    class_2 = train_data[train_data[:,-1]==0]

    class_1_yp = class_1[class_1[:,1] > 0]
    class_1_yn = class_1[class_1[:,1] < 0]
    class_2_yp = class_2[class_2[:,1] > 0]
    class_2_yn = class_2[class_2[:,1] < 0]

    data_1p2p = np.concatenate((class_1_yp,class_2_yp),axis=0)
    data_1p2n = np.concatenate((class_1_yp,class_2_yn),axis=0)
    data_1n2p = np.concatenate((class_1_yn,class_2_yp),axis=0)
    data_1n2n = np.concatenate((class_1_yn,class_2_yn),axis=0)
    np.random.shuffle(data_1p2p)
    np.random.shuffle(data_1p2n)
    np.random.shuffle(data_1n2p)
    np.random.shuffle(data_1n2n)
    return (data_1p2p,data_1p2n,data_1n2p,data_1n2n),test_data

def load_random_splited_data(path_train,path_test):
    train_data, test_data = load_data(path_train,path_test)
    np.random.shuffle(train_data)

    class_1 = train_data[train_data[:,-1]==1]
    class_2 = train_data[train_data[:,-1]==0]
    class_1_yp = class_1[:len(class_1)//2]
    class_1_yn = class_1[len(class_1)//2:]
    class_2_yp = class_2[:len(class_2)//2]
    class_2_yn = class_2[len(class_2)//2:] 

    data_1p2p = np.concatenate((class_1_yp,class_2_yp),axis=0)
    data_1p2n = np.concatenate((class_1_yp,class_2_yn),axis=0)
    data_1n2p = np.concatenate((class_1_yn,class_2_yp),axis=0)
    data_1n2n = np.concatenate((class_1_yn,class_2_yn),axis=0)
    np.random.shuffle(data_1p2p)
    np.random.shuffle(data_1p2n)
    np.random.shuffle(data_1n2p)
    np.random.shuffle(data_1n2n)
    return (data_1p2p,data_1p2n,data_1n2p,data_1n2n),test_data

def load_data(path_train,path_test):
    train_data = load_raw_data(path_train)
    test_data = load_raw_data(path_test)
    train_data[:,0:2]/=6
    test_data[:,0:2]/=6
    return train_data,test_data

def load_raw_data(path):
    with open(path, 'r') as f:
        data = np.array([tuple(map(float, line.strip().split())) for line in f])
    return data
