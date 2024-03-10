import random
import gymnasium as gym
import numpy as np
from tqdm import tqdm
import torch
from torch import nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
from collections import deque
import datetime
import os
import shutil
import matplotlib.pyplot as plt
from copy import deepcopy

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

class Logger:
    def __init__(self, path = None, stdout = True, fig_name = None) -> None:
        self.path = path
        self.stdout = stdout
        self.rewards = []
        self.fig_name = fig_name
        if path is not None:
            self.fp = open(path, 'w')
            self.fp.write('episode,reward\n')
    
    def log(self, episode, reward, epsilon = None):
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

class ReplayBuffer:
    def __init__(self, capacity, muilti_step=0, gamma=0.99):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)
        self.muilti_step = muilti_step
        self.append_count = 0
        self.gamma = gamma
        if muilti_step > 0:
            self.muilti_step_buffer = deque(maxlen=muilti_step+1)
        else:
            self.muilti_step_reward = None
    
    def __len__(self):
        return len(self.buffer)
    
    def calc_muilti_step_reward(self, step = None):
        assert False, "Not implemented"
        current_state_, action_, reward_, next_state_ = self.muilti_step_buffer.popleft()
        step = len(self.muilti_step_buffer) if step is None else step
        for i in range(step):
            reward_ += self.muilti_step_buffer[i][2] * (self.gamma ** (i+1))

        next_state_ = self.muilti_step_buffer[-1][3]

        self.buffer.append((current_state_, action_, reward_, next_state_))

    def append(self, current_state, action, reward, next_state, done = False):
        self.append_count += 1

        if self.muilti_step > 0:
            assert False, "Not implemented"
            self.muilti_step_buffer.append((current_state, action, reward, next_state))
            if len(self.muilti_step_buffer) >= self.muilti_step:
                self.calc_muilti_step_reward()
            if done:
                while len(self.muilti_step_buffer) > 0:
                    self.calc_muilti_step_reward()
        else:
            self.buffer.append((current_state, action, reward, next_state, done))

    def clear(self):
        self.append_count = 0
        self.buffer.clear()
        if self.muilti_step_reward is not None:
            self.muilti_step_reward.clear()

    def sample(self, batch_size):
        samples = random.sample(self.buffer, batch_size)
        current_state, action, reward, next_state, done = map(np.stack, zip(*samples))
        return current_state, action, reward, next_state, done

    def get_all(self):
        current_state, action, reward, next_state, done = map(np.stack, zip(*self.buffer))
        return current_state, action, reward, next_state, done

class PolicyNet(torch.nn.Module):
    def __init__(self, state_dim, hidden_dim, action_dim, action_bound):
        super(PolicyNet, self).__init__()
        self.fc1 = torch.nn.Linear(state_dim, hidden_dim)
        self.fc2 = torch.nn.Linear(hidden_dim, action_dim)
        self.action_bound = action_bound

    def forward(self, x):
        x = F.relu(self.fc1(x))
        return torch.tanh(self.fc2(x)) * self.action_bound

class QValueNet(torch.nn.Module):
    def __init__(self, state_dim, hidden_dim, action_dim):
        super(QValueNet, self).__init__()
        self.fc1 = torch.nn.Linear(state_dim + action_dim, hidden_dim)
        self.fc2 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.fc_out = torch.nn.Linear(hidden_dim, 1)

    def forward(self, x, a):
        cat = torch.cat([x, a], dim=1)
        x = F.relu(self.fc1(cat))
        x = F.relu(self.fc2(x))
        return self.fc_out(x)
    
class DDPG:
    def __init__(self, env, actor, critic, action_dim, logger, 
                 sigma=0.01, actor_lr=3e-4, critic_lr=3e-3, 
                 tau=0.005, gamma=0.98, 
                 batch_size = 128, minimal_size = 1000,
                 replay_buffer_capacity=10000, render=False):
        self.env = env
        self.actor = actor
        self.critic = critic
        self.target_actor = deepcopy(actor)
        self.target_critic = deepcopy(critic)

        self.actor_optimizer = torch.optim.Adam(self.actor.parameters(), lr=actor_lr)
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters(), lr=critic_lr)
        self.gamma = gamma
        self.sigma = sigma
        self.tau = tau
        self.action_dim = action_dim
        self.batch_size = batch_size
        self.minimal_size = minimal_size
        self.logger = logger
        self.replay_buffer = ReplayBuffer(replay_buffer_capacity)
        self.render = render

    def get_action(self, state, sigma = 0.0):
        state = torch.tensor(state, dtype=torch.float).to(device)
        action = self.actor(state).detach().cpu().numpy()
        action = action + sigma * np.random.randn(self.action_dim)
        return action

    def soft_update(self, net, target_net):
        for param_target, param in zip(target_net.parameters(), net.parameters()):
            param_target.data.copy_(param_target.data * (1.0 - self.tau) + param.data * self.tau)

    def optimize_model(self):
        state, action, reward, next_state, done = self.replay_buffer.sample(self.batch_size)

        states = torch.tensor(state, dtype=torch.float).to(device)
        actions = torch.tensor(action, dtype=torch.float).to(device)
        rewards = torch.tensor(reward, dtype=torch.float).view(-1, 1).to(device)
        next_states = torch.tensor(next_state, dtype=torch.float).to(device)
        dones = torch.tensor(done, dtype=torch.float).view(-1, 1).to(device)

        self.target_critic.eval()
        self.target_actor.eval()

        self.critic_optimizer.zero_grad()
        next_q_values = self.target_critic(next_states, self.target_actor(next_states)).detach()
        q_targets = rewards + self.gamma * next_q_values * (1 - dones)
        critic_loss = torch.mean(F.mse_loss(self.critic(states, actions), q_targets))
        critic_loss.backward()
        self.critic_optimizer.step()

        self.actor_optimizer.zero_grad()
        actor_loss = -torch.mean(self.critic(states, self.actor(states)))
        actor_loss.backward()
        self.actor_optimizer.step()

        self.soft_update(self.actor, self.target_actor) 
        self.soft_update(self.critic, self.target_critic)

    def train_one_episode(self):
        total_reward = 0
        state, info = self.env.reset()
        done = False
        while not done:
            if self.render:
                self.env.render()
            action = self.get_action(state, self.sigma)
            next_state, reward, terminated, truncated, info = self.env.step(action)
            done = terminated or truncated
            self.replay_buffer.append(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            if len(self.replay_buffer) > self.minimal_size:
                self.optimize_model()
        return total_reward
    
    def train(self, num_episodes):
        episode = 0
        for i in range(100):
            with tqdm(total=int(num_episodes/100), desc=f'Iteration {i}') as pbar:
                for _ in range(int(num_episodes/100)):
                    episode += 1
                    episode_return = self.train_one_episode()
                    self.logger.log(episode, episode_return)
                    pbar.set_postfix({'episode': f'{episode}', 'return': f'{episode_return:.3f}'})
                    pbar.update(1)
                    # if episode % 20 == 0:
                    #     torch.save(self.actor.state_dict(), os.path.join(models_dir, f'actor_{episode}.pth'))
                    #     torch.save(self.critic.state_dict(), os.path.join(models_dir, f'critic_{episode}.pth'))

def main(
        env_name,
        result_dir = 'results',
        replay_buffer_capacity=10000,
        train_batch_size=128,
        episode_limit=1000,
        render=False,
        tau=0.005,
        sigma=0.01,
        actor_lr=3e-4,
        critic_lr=3e-3,
        gamma=0.98,
    ):

    result_dir = os.path.join(result_dir, env_name, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    os.makedirs(result_dir, exist_ok=True)

    print("Result directory:", result_dir)

    # Copy the script to result_dir
    script_path = __file__
    script_name = os.path.basename(script_path)
    dest_path = os.path.join(result_dir, script_name)
    shutil.copyfile(script_path, dest_path)

    if render:
        env = gym.make(env_name, render_mode="human")
    else:
        env = gym.make(env_name,)

    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]
    action_bound = env.action_space.high[0]
    logger = Logger(os.path.join(result_dir, 'log.csv'), stdout=False, fig_name=os.path.join(result_dir, 'reward.png'))

    hidden_dim = 64

    actor = PolicyNet(state_dim, hidden_dim, action_dim, action_bound).to(device)
    critic = QValueNet(state_dim, hidden_dim, action_dim).to(device)

    agent = DDPG(
        env, actor, critic, action_dim, logger,
        sigma=sigma, 
        actor_lr=actor_lr, 
        critic_lr=critic_lr, 
        tau=tau, 
        gamma=gamma, 
        batch_size = train_batch_size,
        replay_buffer_capacity=replay_buffer_capacity,
        render = render,)

    agent.train(episode_limit)


