# policy: -1 - stop, 0 - left, 1 - right, 2 - up, 3 - down
policy = [-1 for _ in range(16)]
state_value = [0 for _ in range(16)]

def get_state_value(s):
    if s == 0 or s == 15:
        return 0
    else:
        return state_value[s]
    
def value_update(s):
    if s == 0 or s == 15:
        return 0
    new_value = get_state_value(s)
    # left
    if policy[s] == 0:
        if s not in (0,4,8,12):
            new_value = get_state_value(s-1)
    # right
    if policy[s] == 1:
        if s not in (3,7,11,15):
            new_value = get_state_value(s+1)
    # top
    if policy[s] == 2:
        if s not in (0,1,2,3):
            new_value = get_state_value(s-4)
    # bottom
    if policy[s] == 3:
        if s not in (12,13,14,15):
            new_value = get_state_value(s+4)
    return new_value - 1

def value_iteration():
    delta = 0.0
    for s in range(16):
        prev_value = get_state_value(s)
        new_value = value_update(s)
        state_value[s] = new_value
        delta += abs(prev_value - new_value)
    return delta

def policy_update(s):
    if s in (0,15):
        policy[s] = -1
    else:
        max_neighbor_value = get_state_value(s)
        max_neighbor_dir = -1
        # left
        if s not in (0,4,8,12):
            if get_state_value(s-1) > max_neighbor_value:
                max_neighbor_value = get_state_value(s-1)
                max_neighbor_dir = 0
        # right
        if s not in (3,7,11,15):
            if get_state_value(s+1) > max_neighbor_value:
                max_neighbor_value = get_state_value(s+1)
                max_neighbor_dir = 1
        # top
        if s not in (0,1,2,3):
            if get_state_value(s-4) > max_neighbor_value:
                max_neighbor_value = get_state_value(s-4)
                max_neighbor_dir = 2
        # bottom
        if s not in (12,13,14,15):
            if get_state_value(s+4) > max_neighbor_value:
                max_neighbor_value = get_state_value(s+4)
                max_neighbor_dir = 3
        return max_neighbor_dir

def policy_iteration():
    any_change = False
    for s in range(16):
        prev_policy = policy[s]
        new_policy = policy_update(s)
        policy[s] = new_policy
        if prev_policy != new_policy:
            any_change = True
    return any_change

def print_state_value():
    for i in range(16):
        print(f"{state_value[i]}", end=" ")
        if i in (3,7,11,15):
            print()

def print_policy():
    for i in range(16):
        if i in (0,15):
            print("*", end=" ")
        else:
            if policy[i] == -1:
                print("-", end=" ")
            elif policy[i] == 0:
                print("←", end=" ")
            elif policy[i] == 1:
                print("→", end=" ")
            elif policy[i] == 2:
                print("↑", end=" ")
            elif policy[i] == 3:
                print("↓", end=" ")
        if i in (3,7,11,15):
            print()

iter = 0
while True:
    iter += 1
    print(f"iter {iter}" )
    # in case that state value can not converge, limit the maximum iterations
    for i in range(100):
        if value_iteration() < 0.01:
            break
    print_state_value()
    if not policy_iteration():
        break

print("final policy:")
print_policy()

