import numpy as np

class Simulate:
    def __init__(self, policy, V, max_time, swim_success, sunb_success, num_runs):
        self.policy = policy
        self.V = V
        self.max_time = max_time
        self.swim_success = swim_success
        self.sunb_success = sunb_success
        self.num_runs = num_runs

    def simulate(self):
        perfect_days = 0
        for _ in range(self.num_runs):
            sw = sb = 0
            t = 0
            while t < self.max_time:
                action = self.policy[t][sw][sb]
                # print(f"Hour {10 + t}: Do action {action}, (sw={sw}, sb={sb}) → V = {V[t][sw][sb]:.2f}")
                if action == 'SW':
                    if np.random.rand() < self.swim_success[t]:
                        sw += 1
                elif action == 'SB':
                    if np.random.rand() < self.sunb_success[t]:
                        sb += 1
                t += 1
            # print(f"End of day state: SW={sw}, SB={sb}")
            if sw >= 2 and sb >= 2:
                # print("🎉 Perfect day achieved/\n")
                perfect_days += 1
            # else:
            #     print("❌ Imperfect day. Penalty applied.\n")
        print(f"\nPerfect days: {perfect_days} out of {self.num_runs}")
        print(f"The possibility of having a perfect day if follow the policy is {perfect_days / self.num_runs}")