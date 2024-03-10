
import numpy as np
from sklearn.base import ClassifierMixin,BaseEstimator
from torch.optim import Adam
from torch.utils.data import DataLoader, TensorDataset
import torch
import torch.nn as nn

class Net(nn.Module):
    def __init__(self, input_size, output_size, hidden_size=128, drop_rate=0.5):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.dropout = nn.Dropout(drop_rate)

    def forward(self, x):
        x = self.fc1(x)
        x = self.dropout(x)
        x = torch.relu(x)
        x = self.fc2(x)
        return x

def test(model, test_features, test_labels):
    test_feature_tensor = torch.from_numpy(test_features).float()
    test_label_tensor = torch.from_numpy(test_labels).long()

    if torch.cuda.is_available():
        test_feature_tensor = test_feature_tensor.cuda()
        test_label_tensor = test_label_tensor.cuda()
        model = model.cuda()

    model.eval()
    with torch.no_grad():
        test_output = model(test_feature_tensor)
        _, predicted_labels = torch.max(test_output, 1)

    predicted_labels = predicted_labels.cpu().numpy()

    accuracy = (predicted_labels == test_labels).mean()
    return accuracy



def train(model, train_feature, train_label, test_feature = None, test_label = None, weight_decay=0.0, lr=0.001, epoch_num = 10):
    optimizer = Adam(model.parameters(), lr=0.001, weight_decay=weight_decay)
    criterion = nn.CrossEntropyLoss()

    train_feature_tensor = torch.from_numpy(train_feature).float()
    train_label_tensor = torch.from_numpy(train_label).long()

    dataset = TensorDataset(train_feature_tensor, train_label_tensor)

    batch_size = 256
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = model.cuda().train()

    for epoch in range(epoch_num):
        for batch_features, batch_labels in dataloader:
            batch_features = batch_features.cuda()
            batch_labels = batch_labels.cuda()
            optimizer.zero_grad()
            output = model(batch_features)
            loss = criterion(output, batch_labels)
            loss.backward()
            optimizer.step()

class NNEstimator(ClassifierMixin, BaseEstimator):
    def __init__(self, weight_decay=0.0, hidden_size=128, drop_rate=0.0, lr = 0.001, epoch_num = 10):
        super(NNEstimator, self).__init__()
        self.model = None
        self.hidden_size = hidden_size
        self.drop_rate = drop_rate
        self.weight_decay = weight_decay
        self.lr = lr
        self.epoch_num = epoch_num

    def fit(self, X, y):
        input_size = X.shape[1]
        output_size = len(np.unique(y))
        self.model = Net(input_size, output_size, hidden_size=self.hidden_size, drop_rate=self.drop_rate)
        self.model.train().cuda()
        train(self.model, X, y, weight_decay=self.weight_decay, lr=self.lr, epoch_num=self.epoch_num)
        self.model.cpu()

    def predict(self, X):
        test_feature_tensor = torch.from_numpy(X).float().cuda()
        self.model.eval()
        self.model.cuda()
        with torch.no_grad():
            test_output = self.model(test_feature_tensor)
            _, predicted_labels = torch.max(test_output, 1)
        self.model.cpu()
        predicted_labels = predicted_labels.cpu().numpy()
        return predicted_labels

