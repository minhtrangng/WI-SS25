class BackwardDP:
    def __init__(self, actions, policy, V, rewards, max_time, swim_success, sunbath_success, max_sw, max_sb):
        self.actions = actions
        self.policy = policy
        self.V = V
        self.rewards = rewards
        self.max_time = max_time
        self.swim_success = swim_success
        self.sunbath_success = sunbath_success
        self.max_sw = max_sw
        self.max_sb = max_sb

    def compute_value_functions(self):
        for t in reversed(range(self.max_time)):
            # print(f"\n+ At {20 - t} o'clock ({t} time steps remaining): ")
            for sw in range(self.max_sw):
                for sb in range(self.max_sb):
                    best_value = -float('inf')
                    best_action = None
                    for a in self.actions:
                        if a == "SW":
                            p_succ = self.swim_success[t]
                            r = self.rewards["SW"]
                            sw_next = min(sw + 1, self.max_sw)
                            value = (
                                p_succ * (r + self.V[t + 1][sw_next][sb]) +
                                (1 - p_succ) * self.V[t + 1][sw][sb]
                            )
                            # self.V[t][sw][sb] = (
                            #         p_succ * (r + self.V[t + 1][sw_next][sb]) +
                            #         (1 - p_succ) * self.V[t + 1][sw][sb]
                            # )
                            # self.policy[t][sw][sb] = "SW"

                        elif a == "SB":
                            p_succ = self.sunbath_success[t]
                            r = self.rewards["SB"]
                            sb_next = min(sb + 1, self.max_sb)
                            value = (
                                p_succ * (r + self.V[t + 1][sw][sb_next]) +
                                (1 - p_succ) * self.V[t + 1][sw][sb]
                            )
                            # self.V[t][sw][sb] = (
                            #         p_succ * (r + self.V[t + 1][sw][sb_next]) +
                            #         (1 - p_succ) * self.V[t + 1][sw][sb]
                            # )
                            # self.policy[t][sw][sb] = "SB"

                        else:   # EAT
                            r = self.rewards["E"]
                            value = r + self.V[t + 1][sw][sb]
                            # self.V[t][sw][sb] = r + self.V[t + 1][sw][sb]
                            # self.policy[t][sw][sb] = "E"

                        print('Calculated reward: ' +  str(value) + '  for action ' + a)

                        if value > best_value:
                            best_value = value
                            best_action = a

                    self.V[t][sw][sb] = best_value
                    self.policy[t][sw][sb] = best_action
                    # print("t = " + str(t) + '; sw = ' + str(sw) + '; sb = ' + str(sb))
                    print(f"t = {t}; sw = {sw}; sb = {sb}")
                    print("V_best = ", self.V[t][sw][sb])
                    print("Policy_best = ", self.policy[t][sw][sb])
                    # print('++++++Best action to do at time t = ' + str(t) + ': ' + self.policy[t])
                    print(f"Best action to do at time {t} = {self.policy[t][sw][sb]}")
                    print("\n")