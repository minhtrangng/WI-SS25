from itertools import product

# Task definition: (reward, success_prob)
tasks = {
    0: (4, 0.1),
    1: (1, 0.8),
    2: (3, 0.3),
    3: (2, 0.5),
}

num_tasks = len(tasks)
max_time = 5
passing_score = 4

# Generate all 2^4 task-completion states: tuples like (0,1,1,0)
all_states = list(product([0, 1], repeat=num_tasks))

print("All states: ", all_states)

# Helper to calculate score from state
def score(state):
    return sum(state[i] * tasks[i][0] for i in range(num_tasks))

# DP table: V[time][state] = expected cost
V = [{} for _ in range(max_time + 1)]
policy = [{} for _ in range(max_time + 1)]

# Terminal values at time = max_time
for state in all_states:
    V[max_time][state] = 0 if score(state) >= passing_score else 10
    # print('V[5][state] with state = ' + str(state) + ' is ' + str(V[max_time][state]))

# Backward DP
for t in reversed(range(max_time)):
    for state in all_states:
        # If all tasks already solved, keep cost same
        if sum(state) == num_tasks:
            V[t][state] = V[t + 1][state]
            policy[t][state] = None
            continue

        min_cost = float('inf')
        best_task = None

        for i in range(num_tasks):
            if state[i] == 1:
                continue  # already solved

            r_i, p_i = tasks[i]
            # Build next state with task i marked as solved
            next_state = list(state)
            next_state[i] = 1
            next_state = tuple(next_state)

            # Expected cost
            cost = (
                p_i * V[t + 1][next_state] +
                (1 - p_i) * V[t + 1][state]
            )

            if cost < min_cost:
                min_cost = cost
                best_task = i

        V[t][state] = min_cost
        policy[t][state] = best_task

# Initial state: nothing solved
start_state = (0, 0, 0, 0)
print("Expected cost from start:", V[0][start_state])
print("Best first action:", policy[0][start_state])