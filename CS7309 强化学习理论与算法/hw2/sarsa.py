import numpy as np
from enum import Enum

class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

WORLD_HEIGHT = 4
WORLD_WIDTH = 12
START_STATE = (3, 0)
GOAL_STATE = (3, 11)
CLIFF_STATES = [(3, i) for i in range(1, 11)]
STEP_REWARD = -1
CLIFF_REWARD = -100

q_table = np.zeros((WORLD_HEIGHT, WORLD_WIDTH, len(Action)))

def epsilon_greedy_policy(state, epsilon):
    if np.random.uniform() < epsilon:
        return np.random.choice(list(Action))
    else:
        return Action(np.argmax(q_table[state[0], state[1], :]))

num_episodes = 5000
alpha = 0.5
epsilon = 0.01
gamma = 1.0
for episode in range(num_episodes):
    state = START_STATE
    while state != GOAL_STATE:
        action = epsilon_greedy_policy(state, epsilon)
        next_state = None
        reward = None

        # move
        if action == Action.UP:
            next_state = (max(state[0] - 1, 0), state[1])
        elif action == Action.DOWN:
            next_state = (min(state[0] + 1, WORLD_HEIGHT - 1), state[1])
        elif action == Action.LEFT:
            next_state = (state[0], max(state[1] - 1, 0))
        elif action == Action.RIGHT:
            next_state = (state[0], min(state[1] + 1, WORLD_WIDTH - 1))
        
        # reward
        if next_state in CLIFF_STATES:
            reward = CLIFF_REWARD
            next_state = START_STATE
        elif next_state == GOAL_STATE:
            reward = 0
        else:
            reward = STEP_REWARD
        next_action = epsilon_greedy_policy(next_state, epsilon)
        q_table[state[0], state[1], action.value] += alpha * (reward + gamma * q_table[next_state[0], next_state[1], next_action.value] - q_table[state[0], state[1], action.value])
        state = next_state
        action = next_action

on_shortest_path = np.zeros((WORLD_HEIGHT, WORLD_WIDTH), dtype=bool)
state = START_STATE
while state != GOAL_STATE:
    on_shortest_path[state[0], state[1]] = True
    action = action = epsilon_greedy_policy(state, 0)
    if action == Action.UP:
        state = (max(state[0] - 1, 0), state[1])
    elif action == Action.DOWN:
        state = (min(state[0] + 1, WORLD_HEIGHT - 1), state[1])
    elif action == Action.LEFT:
        state = (state[0], max(state[1] - 1, 0))
    elif action == Action.RIGHT:
        state = (state[0], min(state[1] + 1, WORLD_WIDTH - 1))

for i in range(WORLD_HEIGHT):
    for j in range(WORLD_WIDTH):
        if (i, j) == GOAL_STATE:
            print('G', end='\t')
        elif (i, j) in CLIFF_STATES:
            print('C', end='\t')
        elif on_shortest_path[i, j]:
            action = Action(np.argmax(q_table[i, j, :]))
            if action == Action.UP:
                print('↑', end='\t')
            elif action == Action.DOWN:
                print('↓', end='\t')
            elif action == Action.LEFT:
                print('←', end='\t')
            elif action == Action.RIGHT:
                print('→', end='\t')
        else:
            print('*', end='\t')
    print()
