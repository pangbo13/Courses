import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
import gymnasium as gym
from collections import deque
import random
import numpy as np
import os
import datetime
from tqdm import tqdm
import shutil
import copy
import warnings
import torch.nn.functional as F
from matplotlib import pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# env wrapper to normalize observations
# unit8[0,255] -> float32[-1.,1.)
class NormWrapper(gym.ObservationWrapper):
    def observation(self, observation):
        return np.array(observation,dtype=np.float32) / 128.0 - 1.0

class ReplayBuffer:
    def __init__(self, capacity, 
                 muilti_step=0, gamma=0.99, 
                 priority=False, init_priority=1.0):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)
        self.muilti_step = muilti_step
        self.append_count = 0
        self.gamma = gamma
        self.priority = priority
        self.init_priority = init_priority
        if muilti_step > 1:
            self.muilti_step_buffer = deque(maxlen=muilti_step+1)
        if priority:
            self.priority_buffer = deque(maxlen=capacity)
    
    def __len__(self):
        return len(self.buffer)
    
    def calc_muilti_step_reward(self, step = None):
        current_state_, action_, reward_, next_state_, done_ = self.muilti_step_buffer.popleft()
        step = len(self.muilti_step_buffer) if step is None else step
        for i in range(step):
            reward_ += self.muilti_step_buffer[i][2] * (self.gamma ** (i+1))

        next_state_ = self.muilti_step_buffer[-1][3]

        self.buffer.append((current_state_, action_, reward_, next_state_, done_))
        if self.priority:
            self.priority_buffer.append(self.init_priority)

    def append(self, current_state, action, reward, next_state, done = False):
        self.append_count += 1

        if self.muilti_step > 1:
            self.muilti_step_buffer.append((current_state, action, reward, next_state, done))
            if len(self.muilti_step_buffer) >= self.muilti_step:
                self.calc_muilti_step_reward()
            if done:
                while len(self.muilti_step_buffer) > 0:
                    self.calc_muilti_step_reward()
        else:
            self.buffer.append((current_state, action, reward, next_state, done))
            if self.priority:
                self.priority_buffer.append(self.init_priority)

    def clear(self):
        self.append_count = 0
        self.buffer.clear()
        if self.muilti_step_reward is not None:
            self.muilti_step_reward.clear()
        if self.priority:
            self.priority_buffer.clear()

    def update_priority(self, idx, priority):
        assert self.priority, "Not priority buffer"
        for i, p in zip(idx, priority):
            self.priority_buffer[i] = p

    def sample(self, batch_size, priority=False):
        if not priority:
            samples = random.sample(self.buffer, batch_size)
            current_state, action, reward, next_state, done = map(np.stack, zip(*samples))
            return current_state, action, reward, next_state, done
        else:
            priority_buffer = np.array(self.priority_buffer)
            idx = np.random.choice(np.arange(len(self.priority_buffer)), 
                    p=priority_buffer/np.sum(priority_buffer), size=batch_size, replace=False)
            current_state, action, reward, next_state, done = map(
                np.stack, zip(*[self.buffer[i] for i in idx]))
            return current_state, action, reward, next_state, done, idx
    
    def get_all(self):
        current_state, action, reward, next_state, done = map(np.stack, zip(*self.buffer))
        return current_state, action, reward, next_state, done

class Logger:
    def __init__(self, path = None, stdout = True, fig_name = None) -> None:
        self.path = path
        self.stdout = stdout
        self.rewards = []
        self.fig_name = fig_name
        if path is not None:
            self.fp = open(path, 'w')
            self.fp.write('episode,reward\n')
    
    def log(self, episode, reward, epsilon):
        self.rewards.append(reward)
        if self.stdout:
            print(f'Episode {episode}: reward: {reward}, epsilon: {epsilon:.3f}')
        if self.path is not None:
            self.fp.write(f'{episode},{reward}\n')
            if (episode + 1) % 10 == 0:
                self.fp.flush()
        if self.fig_name is not None and episode % 10 == 0:
            plt.plot(self.rewards)
            plt.ylabel('reward')
            plt.xlabel('Episode')
            plt.savefig(self.fig_name)
            plt.close()


# model definition

class NoisyLinear(nn.Linear):
    """Noisy Layer to replace Epsilon-Greedy Exploration"""

    def __init__(self, in_features, out_features, bias=True, sigma_init=0.017, *args, **kwargs):
        super(NoisyLinear, self).__init__(in_features, out_features, bias=bias, *args, **kwargs)
        self.sigma_weight = nn.Parameter(torch.full((out_features, in_features), sigma_init))
        self.register_buffer("epsilon_weight", torch.zeros(out_features, in_features))
        if bias:
            self.sigma_bias = nn.Parameter(torch.full((out_features,), sigma_init))
            self.register_buffer("epsilon_bias", torch.zeros(out_features))

    def resample(self):
        self.epsilon_weight.normal_()
        if self.bias is not None:
            self.epsilon_bias.normal_()

    def forward(self, x, noise=True):
        bias = self.bias
        if bias is not None:
            bias = bias + self.sigma_bias * self.epsilon_bias
        if noise:
            return F.linear(x, self.weight + self.sigma_weight * self.epsilon_weight, bias)
        else:
            return F.linear(x, self.weight, bias)


# Orignal DQN
class Model(nn.Module):
    def __init__(self, input_features, output_values, noisy=False):
        super(Model, self).__init__()
        self.noisy = noisy
        if noisy:
            Linear = NoisyLinear
        else:
            Linear = nn.Linear
        self.fc1 = Linear(in_features=input_features, out_features=512)
        self.fc2 = Linear(in_features=512, out_features=128)
        self.fc3 = Linear(in_features=128, out_features=output_values)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
    def resample(self):
        if self.noisy:
            for m in self.modules():
                if isinstance(m, NoisyLinear):
                    m.resample()
        else:
            warnings.warn("Model is not Noisy", stacklevel=2)

# Dueling DQN
# https://arxiv.org/pdf/1511.06581.pdf
class Duel_Model(nn.Module):
    def __init__(self, input_features, output_values, noisy=False):
        super(Duel_Model, self).__init__()
        self.noisy = noisy
        if noisy:
            Linear = NoisyLinear
        else:
            Linear = nn.Linear
        self.fc1_adv = Linear(in_features=input_features, out_features=512)
        self.fc2_adv = Linear(in_features=512, out_features=128)
        self.fc3_adv = Linear(in_features=128, out_features=output_values)

        self.fc1_val = Linear(in_features=input_features, out_features=256)
        self.fc2_val = Linear(in_features=256, out_features=32)
        self.fc3_val = Linear(in_features=32, out_features=1)

    def forward(self, x):
        adv = F.relu(self.fc1_adv(x))
        adv = F.relu(self.fc2_adv(adv))
        adv = self.fc3_adv(adv)

        val = F.relu(self.fc1_val(x))
        val = F.relu(self.fc2_val(val))
        val = self.fc3_val(val)

        if adv.dim() == 1:
            q_values = val + adv - adv.mean()
        else:
            q_values = val + adv - adv.mean(dim=1, keepdim=True)
        return q_values
    
    def resample(self):
        if self.noisy:
            for m in self.modules():
                if isinstance(m, NoisyLinear):
                    m.resample()
        else:
            warnings.warn("Model is not Noisy", stacklevel=2)

class Agent():
    def __init__(self, env, net, n_actions,
                 init_epsilon = 1, min_epsilon = 0.1, epsilon_decay = 0.005,
                 replay_buffer_capacity = 400000, train_batch_size = 128,
                 multi_step = 0, gamma = 0.99, learning_rate = 0.00025,
                 target_update_delay = 2, test_delay = 10, init_priority=100.0,
                 noisy = False, target_dqn=False, double_dqn=False, priority=False,
                 render=False):
        self.env = env
        self.n_actions = n_actions
        self.train_times = 0
        self.train_batch_size = train_batch_size
        self.multi_step = multi_step
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.epsilon = init_epsilon
        self.min_epsilon = min_epsilon
        self.epsilon_decay = epsilon_decay
        self.target_update_delay = target_update_delay
        self.test_delay = test_delay
        self.noisy = noisy
        self.priority = priority
        self.render = render

        self.memory = ReplayBuffer(capacity = replay_buffer_capacity, muilti_step = multi_step, gamma=gamma, priority=priority, init_priority=init_priority)

        self.target_dqn = target_dqn
        self.double_dqn = double_dqn

        self.policy_net = net
        self.policy_net_optimizer = torch.optim.Adam(
            params=self.policy_net.parameters(), lr=self.learning_rate)
        if target_dqn or double_dqn:
            self.target_net = copy.deepcopy(net)
        else:
            self.target_net = None

        if double_dqn:
            self.target_net_optimizer = torch.optim.Adam(
                params=self.target_net.parameters(), lr=self.learning_rate)
        else:
            self.target_net_optimizer = None

    def get_action(self, state, e):
        if random.random() < e:
            # explore
            action = random.randrange(0, self.n_actions)
        else:
            state = torch.tensor(state, dtype=torch.float32, device=device)
            action = self.policy_net(state).argmax().item()
        return action

    def fit(self, model: nn.Module, optimizer: torch.optim.Optimizer,
             inputs: np.ndarray, labels: np.ndarray, idx = None):

        inputs = inputs.to(device)
        labels = labels.to(device)

        criterion = nn.MSELoss(reduction='none')
        model.train().to(device)

        out = model(inputs)
        loss = criterion(out, labels)
        mean_loss = loss.mean()
        optimizer.zero_grad()
        mean_loss.backward()
        optimizer.step()

        model.eval()
        if self.priority:
            self.memory.update_priority(idx, loss.mean(dim=1).detach().cpu().numpy())

        return mean_loss.item()


    def optimize_model(self):
        self.train_times += 1
        if self.target_dqn or self.double_dqn:
            target_net = self.target_net
        else: # Orignal DQN
            target_net = self.policy_net

        if not self.priority:
            state, action, env_reward, next_state, done = self.memory.sample(self.train_batch_size)
        else:
            state, action, env_reward, next_state, done, idx = self.memory.sample(self.train_batch_size, priority=True)

        state = torch.from_numpy(state).to(device)
        next_state = torch.from_numpy(next_state).to(device)
        with torch.no_grad():
            target_net.to(device).eval()
            q_estimates = target_net(state).cpu().numpy()
            next_state_q_estimates = target_net(next_state).cpu().numpy()
        del next_state

        # update q_estimates
        q_estimates[np.arange(len(q_estimates)), action] = (env_reward + self.gamma * next_state_q_estimates.max(axis=1))

        if self.priority:
            self.fit(self.policy_net, self.policy_net_optimizer, state, torch.from_numpy(q_estimates), idx)
        else:
            self.fit(self.policy_net, self.policy_net_optimizer, state, torch.from_numpy(q_estimates))


    def train_one_episode(self):
        current_state, info = self.env.reset()
        done = False
        reward = 0
        step = 0
        while not done:
            action = self.get_action(current_state, self.epsilon)
            next_state, env_reward, terminated, truncated, info = self.env.step(action)
            done = terminated or truncated
            self.memory.append(current_state, action, env_reward, next_state)
            current_state = next_state
            reward += env_reward
            if self.render:
                self.env.render()
            step += 1
            if len(self.memory) > self.train_batch_size * 10 and step % 32 == 0:
                self.optimize_model()

        return reward

    def test(self):
        current_state, info = self.env.reset()
        done = False
        reward = 0
        step = 0
        while not done:
            action = self.get_action(current_state, 0.05)
            next_state, env_reward, terminated, truncated, info = self.env.step(action)
            done = terminated or truncated
            current_state = next_state
            reward += env_reward
            step += 1
        return reward
    
    def save_model(self, path):
        if self.double_dqn:
            torch.save([self.policy_net.state_dict(),self.target_net.state_dict()], path)
        else:
            torch.save(self.policy_net.state_dict(), path)

    def train(self,episode_limit=10000,logger=None):
        last_best_episode = 0
        last_best_reward = 0
        for i in range(episode_limit):

            # resample noisy layer
            if self.noisy:
                self.policy_net.resample()
                if self.target_dqn or self.double_dqn:
                    self.target_net.resample()
            
            reward = self.train_one_episode()
            
            if logger is not None:
                logger.log(i + 1, reward, self.epsilon)

            if (i+1) % 10 == 0:
                pass
                # self.save_model(os.path.join(models_dir,f"episode_{i + 1}_{reward}.pt"))

            if self.double_dqn and i % self.target_update_delay == 0:
                # exchange policy_net and target_net
                self.policy_net, self.target_net = self.target_net, self.policy_net
                self.policy_net_optimizer, self.target_net_optimizer = self.target_net_optimizer, self.policy_net_optimizer
            elif self.target_dqn and i % self.target_update_delay == 0:
                self.target_net.load_state_dict(self.policy_net.state_dict())

            if not self.noisy:
                if reward > last_best_reward:
                    last_best_reward = reward
                    last_best_episode = i
                if i - last_best_episode > 10:
                    last_best_episode = i
                    last_best_reward = reward
                    self.epsilon = min(self.epsilon + self.epsilon_decay * 15, 1.0)
                else:
                    self.epsilon -= self.epsilon_decay
                if self.epsilon < self.min_epsilon:
                    self.epsilon = self.min_epsilon
            else:
                self.epsilon = max(self.epsilon - self.epsilon_decay, self.min_epsilon)

            if i % 50 == 0:
                test_reward = self.test()
                print(f'Test Episode {i + 1}: test reward: {test_reward:.3f}')


def main(env_name, 
        episode_limit = 10000,
        result_dir = 'results',
        render = False,
        dueling = True,
        init_epsilon = 1, 
        min_epsilon = 0.1, 
        epsilon_decay = 0.002,
        replay_buffer_capacity = 10000, 
        train_batch_size = 128,
        multi_step = 3, 
        gamma = 0.99, 
        learning_rate = 0.001,
        target_update_delay = 2, 
        test_delay = 10, 
        noisy = True,
        target_dqn=False, 
        double_dqn=True, 
        priority=True):

    result_dir = os.path.join(result_dir, env_name, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    os.makedirs(result_dir, exist_ok=True)

    print("Result directory:", result_dir)

    # Copy the script to result_dir
    script_path = __file__
    script_name = os.path.basename(script_path)
    dest_path = os.path.join(result_dir, script_name)
    shutil.copyfile(script_path, dest_path)

    print("Script copied to:", dest_path)

    if render:
        env = gym.make(env_name, render_mode="human")
    else:
        env = gym.make(env_name,)
    env.unwrapped.seed = 42
    # env.metadata['render_fps'] = 30
    n_features = env.observation_space.shape[0]
    n_actions = env.action_space.n

    print(n_features, n_actions)
    env = NormWrapper(env)
    env.reset()

    if dueling:
        net = Duel_Model(n_features, n_actions, noisy = noisy).to(device)
    else:
        net = Model(n_features, n_actions, noisy = noisy).to(device)

    logger = Logger(os.path.join(result_dir, 'log.csv'), 
                    fig_name = os.path.join(result_dir,'reward.png'))
    agent = Agent(env, net, n_actions, 
                    init_epsilon = init_epsilon, 
                    min_epsilon = min_epsilon, 
                    epsilon_decay = epsilon_decay,
                    replay_buffer_capacity = replay_buffer_capacity, 
                    train_batch_size = train_batch_size,
                    multi_step = multi_step, 
                    gamma = gamma, 
                    learning_rate = learning_rate,
                    target_update_delay = target_update_delay, 
                    test_delay = test_delay, 
                    noisy = noisy,
                    target_dqn = target_dqn, 
                    double_dqn = double_dqn, 
                    priority = priority,
                    render = render)
    agent.train(episode_limit=episode_limit,logger=logger)
    env.close()

if __name__ == '__main__':
    main("Breakout-ramNoFrameskip-v4")