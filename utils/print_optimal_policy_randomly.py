import numpy as np
class Utils:
    def print_optimal_policy_randomly(policy, V, max_time, swim_success_prob, sunbathing_success_prob):
        sw, sb = 0, 0
        for t in range(max_time):
            act = policy[t][sw][sb]
            print(f"Hour {10 + t}: Do action {act}, (sw={sw}, sb={sb}) → V = {V[t][sw][sb]:.2f}")
            if act == "SW":
                if np.random.rand() < swim_success_prob[t]:
                    sw = min(sw + 1, 4)
            elif act == "SB":
                if np.random.rand() < sunbathing_success_prob[t]:
                    sb = min(sb + 1, 4)
            # "E" does not change state
        print(f"End of day state: SW={sw}, SB={sb}")
        if sw >= 2 and sb >= 2:
            print("🎉 Perfect day achieved!")
        # else:
        #     print("❌ Imperfect day. Penalty applied.")