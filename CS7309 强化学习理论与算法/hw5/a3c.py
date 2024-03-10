import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.multiprocessing as multiprocessing
import gym
import math, os
import numpy as np
os.environ["OMP_NUM_THREADS"] = "1"

UPDATE_GLOBAL_ITER = 5
GAMMA = 0.9
MAX_EP = 3000
MAX_EP_STEP = 200

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(3, 128)
        self.mu = nn.Linear(128, 1)
        self.sigma = nn.Linear(128, 1)
        self.fc2 = nn.Linear(3, 64)
        self.v = nn.Linear(64, 1)

    def forward(self, x):
        a1 = torch.relu(self.fc1(x))
        mu = 2 * torch.tanh(self.mu(a1))
        sigma = F.softplus(self.sigma(a1)) + 0.001
        c1 = torch.relu(self.fc2(x))
        values = self.v(c1)
        return mu, sigma, values

    def choose_action(self, s):
        self.training = False
        mu, sigma, _ = self.forward(s)
        m = torch.distributions.Normal(mu.view(1, ).data, sigma.view(1, ).data)
        return m.sample().numpy()


class Worker(multiprocessing.Process):
    def __init__(self, gnet, opt, global_ep, global_ep_r, res_queue, name):
        super(Worker, self).__init__()
        self.name = f'w{name}'
        self.g_ep, self.g_ep_r, self.res_queue = global_ep, global_ep_r, res_queue
        self.gnet, self.opt = gnet, opt
        self.lnet = Net()
        self.env = gym.make('Pendulum-v1')

    def run(self):
        total_step = 1
        while self.g_ep.value < MAX_EP:
            s = self.env.reset()
            buffer_s, buffer_a, buffer_r = [], [], []
            ep_r = 0.
            done = False
            while not done:
                if self.name == 'w0':
                    self.env.render()
                a = self.lnet.choose_action(torch.Tensor(s[None, :]))
                s_, r, done, _ = self.env.step(a.clip(-2, 2))
                ep_r += r
                buffer_a.append(a)
                buffer_s.append(s)
                buffer_r.append((r+8.1)/8.1)

                if total_step % UPDATE_GLOBAL_ITER == 0 or done:  
                    if done:
                        v_s_ = 0.
                    else:
                        v_s_ = self.lnet.forward(torch.Tensor(s_[None, :]))[-1].data.numpy()[0, 0]

                    buffer_v_target = []
                    for r in buffer_r[::-1]:    # reverse buffer r
                        v_s_ = r + GAMMA * v_s_
                        buffer_v_target.append(v_s_)
                    buffer_v_target.reverse()

                    loss = loss_func(
                        self.lnet,
                        torch.Tensor(np.vstack(buffer_s)),
                        torch.Tensor(np.vstack(buffer_a)),
                        torch.Tensor(np.array(buffer_v_target)[:, None]))

                    # 将本地梯度应用给全局模型
                    self.opt.zero_grad()
                    loss.backward()
                    for lp, gp in zip(self.lnet.parameters(), self.gnet.parameters()):
                        gp._grad = lp.grad
                    self.opt.step()

                    # 同步全局模型
                    self.lnet.load_state_dict(self.gnet.state_dict())

                    buffer_s, buffer_a, buffer_r = [], [], []

                    if done:
                        record(self.g_ep, self.g_ep_r, ep_r, self.res_queue, self.name)
                        break
                s = s_
                total_step += 1

        self.res_queue.put(None)

def loss_func(model, s, a, v_t):
    model.train()
    mu, sigma, values = model(s)
    td = v_t - values
    c_loss = td ** 2

    m = torch.distributions.Normal(mu, sigma)
    log_prob = m.log_prob(a)
    entropy = 0.5 + 0.5 * math.log(2 * math.pi) + torch.log(m.scale)
    exp_v = log_prob * td.detach() + 0.005 * entropy
    a_loss = -exp_v
    total_loss = (a_loss + c_loss).mean()
    return total_loss

def record(global_ep, global_ep_r, ep_r, res_queue, name):
    with global_ep.get_lock():
        global_ep.value += 1
    with global_ep_r.get_lock():
        if global_ep_r.value == 0.:
            global_ep_r.value = ep_r
        else:
            global_ep_r.value = global_ep_r.value * 0.99 + ep_r * 0.01
    res_queue.put(global_ep_r.value)
    print(name,global_ep.value,global_ep_r.value)

if __name__ == "__main__":
    gnet = Net()
    gnet.share_memory()
    opt = torch.optim.Adam(gnet.parameters(), lr=1e-4)
    global_ep, global_ep_r, res_queue = multiprocessing.Value('i', 0), multiprocessing.Value('d', 0.), multiprocessing.Queue()

    # 初始化workers
    workers = [Worker(gnet, opt, global_ep, global_ep_r, res_queue, i) for i in range(multiprocessing.cpu_count())]
    [w.start() for w in workers]
    res = []
    while True:
        r = res_queue.get()
        if r is not None:
            res.append(r)
        else:
            break
    [w.join() for w in workers]

    # 画图
    import matplotlib.pyplot as plt
    plt.plot(res)
    plt.ylabel('reward')
    plt.xlabel('Step')
    plt.show()