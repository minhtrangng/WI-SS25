class Utils:
    def print_optimal_day(policy, V, max_time):
        sw = 0
        sb = 0
        print("Optimal day plan:")
        for t in range(max_time):
            print(f"\nHour {t}:")
            best_val_func = -float('inf')
            best_t = 0
            best_sw = 0
            best_sb = 0
            for sw in range(5):
                for sb in range(5):
                    # print("------------------------------------------------------")
                    if (V[t][sw][sb] > best_val_func):
                        best_val_func = V[t][sw][sb]
                        best_t = t
                        best_sw = sw
                        best_sb = sb
                    best_policy = policy[best_t][best_sw][best_sb]

            print("\t+ Best value function: ", best_val_func)
            print("\t+ Best policy: ", best_policy)
