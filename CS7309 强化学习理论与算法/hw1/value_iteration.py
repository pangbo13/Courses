

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
    if s not in (0,4,8,12):
        new_value = max(new_value, get_state_value(s-1))
    # right
    if s not in (3,7,11,15):
        new_value = max(new_value, get_state_value(s+1))
    # top
    if s not in (0,1,2,3):
        new_value = max(new_value, get_state_value(s-4))
    # bottom
    if s not in (12,13,14,15):
        new_value = max(new_value, get_state_value(s+4))
    return new_value - 1

def value_iteration():
    any_change = False
    for s in range(16):
        prev_value = get_state_value(s)
        new_value = value_update(s)
        state_value[s] = new_value
        if prev_value != new_value:
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
            max_neighbor_value = get_state_value(i)
            max_neighbor_dir = "-"
            # left
            if i not in (0,4,8,12):
                if get_state_value(i-1) > max_neighbor_value:
                    max_neighbor_value = get_state_value(i-1)
                    max_neighbor_dir = "←"
            # right
            if i not in (3,7,11,15):
                if get_state_value(i+1) > max_neighbor_value:
                    max_neighbor_value = get_state_value(i+1)
                    max_neighbor_dir = "→"
            # top
            if i not in (0,1,2,3):
                if get_state_value(i-4) > max_neighbor_value:
                    max_neighbor_value = get_state_value(i-4)
                    max_neighbor_dir = "↑"
            # bottom
            if i not in (12,13,14,15):
                if get_state_value(i+4) > max_neighbor_value:
                    max_neighbor_value = get_state_value(i+4)
                    max_neighbor_dir = "↓"
            print(max_neighbor_dir, end=" ")
        if i in (3,7,11,15):
            print()

iter = 0
while value_iteration():
    iter += 1
    print(f"iter {iter}" )
    print_state_value()

print("final policy:")
print_policy()

