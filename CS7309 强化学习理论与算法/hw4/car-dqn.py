import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
from torch.nn import functional
import gym
from collections import deque
import random
import numpy as np

class Model(nn.Module):
    def __init__(self, input_features, output_values):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(in_features=input_features, out_features=32)
        self.fc2 = nn.Linear(in_features=32, out_features=32)
        self.fc3 = nn.Linear(in_features=32, out_features=output_values)

    def forward(self, x):
        x = functional.selu(self.fc1(x))
        x = functional.selu(self.fc2(x))
        x = self.fc3(x)
        return x

use_cuda = True
episode_limit = 100
target_update_delay = 2
test_delay = 10
learning_rate = 0.001
epsilon = 1.00  # initial epsilon
min_epsilon = 0.1
epsilon_decay = 0.05
gamma = 0.99
memory_len = 10000

env = gym.make('MountainCar-v0')
env.seed(42)
n_features = 2
n_actions = env.action_space.n

memory = deque(maxlen=memory_len)

device = torch.device("cuda" if use_cuda and torch.cuda.is_available() else "cpu")
criterion = nn.MSELoss()
policy_net = Model(n_features, n_actions).to(device)
target_net = Model(n_features, n_actions).to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()


def get_states_tensor(sample, states_idx):
    sample_len = len(sample)
    states_tensor = torch.empty((sample_len, n_features), dtype=torch.float32, requires_grad=False)

    features_range = range(n_features)
    for i in range(sample_len):
        for j in features_range:
            states_tensor[i, j] = sample[i][states_idx][j].item()

    return states_tensor

def get_action(state, e=min_epsilon):
    if random.random() < e:
        # explore
        action = random.randrange(0, n_actions)
    else:
        state = torch.tensor(state, dtype=torch.float32, device=device)
        action = policy_net(state).argmax().item()
    return action

def fit(model, inputs, labels):
    inputs = inputs.to(device)
    labels = labels.to(device)
    train_ds = TensorDataset(inputs, labels)
    train_dl = DataLoader(train_ds, batch_size=5)

    optimizer = torch.optim.Adam(params=model.parameters(), lr=learning_rate)
    model.train()
    total_loss = 0.0

    for x, y in train_dl:
        out = model(x)
        loss = criterion(out, y)
        total_loss += loss.item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    model.eval()

    return total_loss / len(inputs)


def optimize_model(train_batch_size=256):
    train_batch_size = min(train_batch_size, len(memory))
    train_sample = random.sample(memory, train_batch_size)

    state = get_states_tensor(train_sample, 0)
    next_state = get_states_tensor(train_sample, 3)

    q_estimates = policy_net(state.to(device)).detach()
    next_state_q_estimates = target_net(next_state.to(device)).detach()

    for i in range(len(train_sample)):
        q_estimates[i][train_sample[i][1]] = ( train_sample[i][2] +
                                              gamma * next_state_q_estimates[i].max())

    fit(policy_net, state, q_estimates)


def train_one_episode():
    global epsilon
    current_state = env.reset()
    done = False
    score = 0
    step = 0
    while not done:
        action = get_action(current_state, epsilon)
        next_state, env_reward, done, info = env.step(action)
        # done = terminated or truncated
        # print("y=",np.sin(3 * next_state[0]) * 0.45 + 0.55,"speed=",abs(next_state[1]))
        state_reward = next_state[0]**2 + abs(next_state[1]) * 50
        if next_state[0] >= 0.5:
            state_reward += 100 + 4 * (200 - step)
        reward = env_reward + state_reward
        memory.append((current_state, action, reward, next_state))
        current_state = next_state
        score += reward
        step += 1
        env.render()

    for _ in range(40):
        optimize_model(256)
    epsilon -= epsilon_decay
    return step,score

def main():
    for i in range(episode_limit):
        step,score = train_one_episode()
        print(f'Episode {i + 1}: step: {step},score: {score}')
        if i % target_update_delay == 0:
            target_net.load_state_dict(policy_net.state_dict())
            target_net.eval()
    env.close()


if __name__ == '__main__':
    main()