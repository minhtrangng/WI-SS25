import numpy as np

class Utils:
    def __init__(self, policy, V, max_time, max_sw, max_sb, swim_success_prob, sunbathing_success_prob):
        self.policy = policy
        self.V = V
        self.max_time = max_time
        self.max_sw = max_sw
        self.max_sb = max_sb
        self.swim_success_prob = swim_success_prob
        self.sunbathing_success_prob = sunbathing_success_prob

    def print_optimal_policy_deterministic(self ):
        sw, sb = 0, 0
        for t in range(self.max_time):
            act = self.policy[t][sw][sb]
            print(f"{10 + t} o'clock: Do action {act}, (sw={sw}, sb={sb}) → V = {self.V[t][sw][sb]:.2f}")
            if act == "SW":
                sw = min(sw + 1, self.max_sw)
            elif act == "SB":
                sb = min(sb + 1, self.max_sb)
        print(f"End of day state: SW={sw}, SB={sb}")
        if sw >= 2 and sb >= 2:
            print("🎉 Perfect day achieved!")
        else:
            print("❌ Imperfect day. Penalty applied.")

    def print_optimal_policy_v2(self):
        sw, sb = 0, 0
        print("Optimal day plan:")
        for t in range(self.max_time):
            print(f"\nHour {t}:")
            best_val_func = -float('inf')
            best_t = 0
            best_sw = 0
            best_sb = 0
            for sw in range(5):
                for sb in range(5):
                    # print("------------------------------------------------------")
                    if (self.V[t][sw][sb] > best_val_func):
                        best_val_func = self.V[t][sw][sb]
                        best_t = t
                        best_sw = sw
                        best_sb = sb
                    best_policy = self.policy[best_t][best_sw][best_sb]

            print("\t+ Best value function: ", best_val_func)
            print("\t+ Best policy: ", best_policy)

    def print_optimal_policy_randomly(self):
        sw, sb = 0, 0
        for t in range(self.max_time):
            act = self.policy[t][sw][sb]
            print(f"Hour {10 + t}: Do action {act}, (sw={sw}, sb={sb}) → V = {self.V[t][sw][sb]:.2f}")
            if act == "SW":
                if np.random.rand() < self.swim_success_prob[t]:
                    sw = min(sw + 1, 4)
            elif act == "SB":
                if np.random.rand() < self.sunbathing_success_prob[t]:
                    sb = min(sb + 1, 4)
            # "E" does not change state
        print(f"End of day state: SW={sw}, SB={sb}")
        if sw >= 2 and sb >= 2:
            print("🎉 Perfect day achieved!")
        # else:
        #     print("❌ Imperfect day. Penalty applied.")