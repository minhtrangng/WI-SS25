class Utils:
    def print_optimal_day(policy, V, max_time):
        # sw = 1
        # sb = 1
        # print("Optimal day plan:")
        for sw in range(5):
            for sb in range(5):
                print("\n------------------------------------------------------")
                print(f"Optimal day plan when sw={sw} and sb={sb}:")
                for t in range(max_time):
                    action = policy[t][sw][sb]
                    print(f"Hour {10 + t}: {action.upper()} (sw={sw}, sb={sb}, V={V[t][sw][sb]:.2f})")

                    # Simulate what would happen if the action succeeds
                    if action == 'sw':
                        if sw < 4:  # just a safety check
                            sw += 1  # assume success
                    elif action == 'sb':
                        if sb < 4:
                            sb += 1  # assume success
                    # for 'eat', nothing changes in sw/sb

                print(f"\nFinal state: sw={sw}, sb={sb}")
                if sw >= 2 and sb >= 2:
                    print("✅ Perfect day achieved!")
                else:
                    print("❌ Failed to achieve a perfect day.")
