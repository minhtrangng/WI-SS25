class Utils:
    def print_optimal_policy_deterministic(policy, V, max_time):
        sw, sb = 0, 0
        for t in range(max_time):
            act = policy[t][sw][sb]
            print(f"{10 + t} o'clock: Do action {act}, (sw={sw}, sb={sb}) → V = {V[t][sw][sb]:.2f}")
            if act == "SW":
                sw = min(sw + 1, 4)
            elif act == "SB":
                sb = min(sb + 1, 4)
        print(f"End of day state: SW={sw}, SB={sb}")
        if sw >= 2 and sb >= 2:
            print("🎉 Perfect day achieved!")
        else:
            print("❌ Imperfect day. Penalty applied.")
