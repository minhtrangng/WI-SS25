import numpy as np
from utils.print_results import Utils
from utils.simulate import Simulate
from algorithm.backward_dp import BackwardDP

# Define parameters
actions = ["SW", "SB", "E"]
hours = list(range(10, 21))  # From 10:00 to 20:00 -> 11 time steps
T = len(hours)      # max_time
gamma = 1.0  # No discounting
max_sb = 7
max_sw = 7

# Success probabilities by hour (index 0 corresponds to 10:00)
swim_success = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.3, 0.25, 0.2, 0.15]
sun_success = [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15]

# Rewards
reward = {
    "SW": 10,
    "SB": 5,
    "E": 5
}

# State: (t, sw_done, sb_done)
# Value function: V[t][sw][sb]
V = np.zeros((T + 1, max_sw + 1, max_sb + 1))  # Maximum 8 successful actions to track, safe upper bound
                            # Limit is set to 8 is because each action sw and sb need to be successfully done at least 2 times (11 - 2 = 9)
                            # During the day, action eat is done 2 time (9 - 2 = 7)

# Terminal condition
for sw in range(max_sw + 1):
    for sb in range(max_sb + 1):
        if sw >= 2 and sb >= 2:
            V[T][sw][sb] = 0
        else:
            V[T][sw][sb] = -100

# Backward DP
policy = np.empty((T, max_sw + 1, max_sb + 1), dtype=object)

# for t in reversed(range(T)):    # t: 10 → 0
#     # print(f"\n+ At {20 - t} o'clock ({t} time steps remaining): ")
#     for sw in range(max_sw + 1):
#         for sb in range(max_sb + 1):
#             best_val = -float('inf')
#             best_act = None
#             for a in actions:
#                 if a == "SW":
#                     p_succ = swim_success[t]
#                     r = reward["SW"]
#                     sw_next = min(sw + 1, max_sw)
#                     val = (
#                         p_succ * (r + V[t + 1][sw_next][sb]) +
#                         (1 - p_succ) * V[t + 1][sw][sb]
#                     )
#                 elif a == "SB":
#                     p_succ = sun_success[t]
#                     r = reward["SB"]
#                     sb_next = min(sb + 1, max_sb)
#                     val = (
#                         p_succ * (r + V[t + 1][sw][sb_next]) +
#                         (1 - p_succ) * V[t + 1][sw][sb]
#                 )
#                 else:  # Eat
#                     r = reward["E"]
#                     val = r + V[t + 1][sw][sb]
#                 # print('\n')
#                 # print('Calculated reward: ' +  str(val) + '  for action ' + a)
#                 if val > best_val:
#                     best_val = val
#                     best_act = a
#             V[t][sw][sb] = best_val
#             policy[t][sw][sb] = best_act
#             # print("\n")
#     # print("t = " + str(t) + '; sw = ' + str(sw) + '; sb = ' + str(sb))
#     # print("V_best = ", V[t][sw][sb])
#     # print("Policy_best = ", policy[t][sw][sb])
#     # print("\n")
#             # print('++++++Best action to do at time t = ' + str(t) + ': ' + policy[t])

backward_alg = BackwardDP(actions, policy, V, reward, T, swim_success, sun_success, max_sw, max_sb)

backward_alg.compute_value_functions()

# (a)**** The optimal policy
print("------------------------------------------")
print("OPTIMAL POLICY:")
print_result = Utils(policy=policy, V=V, max_time=T, max_sw=max_sw, max_sb=max_sb, swim_success_prob=swim_success, sunbathing_success_prob=sun_success)
print_result.print_optimal_policy_deterministic()

# (b)**** V_pi* [0][0][0]: Value function of optimal policy at start (t = 0, sw = 0, sb = 0)
print("------------------------------------------")
print("V_pi* at start V_pi*[0][0][0]: ", V[0][0][0])

# (c)**** Possibility of having a perfect day at the beach when follow the optimal policy
print("------------------------------------------")
test_optimal_policy = Simulate(policy=policy, V=V, max_time=T, swim_success=swim_success, sunb_success=sun_success, num_runs=10_000)
test_optimal_policy.simulate()

# Utils.print_optimal_policy_randomly(policy, V, T, swim_success, sun_success)
# print("\n----------------Simulate perfect day applying random approach------------------")
# Simulate.simulate(policy, V, T, swim_success, sun_success, 1000)

