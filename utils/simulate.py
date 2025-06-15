import numpy as np

class Simulate:
    def simulate(policy, V, max_time, swim_success, sunb_success, num_runs):
        perfect_days = 0
        for _ in range(num_runs):
            sw = sb = 0
            t = 0
            while t < max_time:
                action = policy[t][sw][sb]
                # print(f"Hour {10 + t}: Do action {action}, (sw={sw}, sb={sb}) → V = {V[t][sw][sb]:.2f}")
                if action == 'SW':
                    if np.random.rand() < swim_success[t]:
                        sw += 1
                elif action == 'SB':
                    if np.random.rand() < sunb_success[t]:
                        sb += 1
                t += 1
            # print(f"End of day state: SW={sw}, SB={sb}")
            if sw >= 2 and sb >= 2:
                # print("🎉 Perfect day achieved/\n")
                perfect_days += 1
            # else:
            #     print("❌ Imperfect day. Penalty applied.\n")
        print(f"\nPerfect days: {perfect_days} out of {num_runs}")
        print(f"The possibility of having a perfect day if follow the policy is {perfect_days / num_runs}")