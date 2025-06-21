from graphviz import Digraph

class IllustratePolicy:
    def __init__(self, policy):
        self.policy = policy

    def visualize_policy_tree(self, max_depth, max_sw, max_sb):
        dot = Digraph()
        visited = set()

        def add_node(t, sw, sb, path=''):
            if t >= len(self.policy) or sw > max_depth or sb > max_depth or len(path) > max_depth:
                return

            node_id = f"{t}_{sw}_{sb}"
            if node_id in visited:
                return
            visited.add(node_id)

            label = f"t={t}\nsw={sw}\nsb={sb}\n→ {self.policy[t][sw][sb]}"
            dot.node(node_id, label)

            action = self.policy[t][sw][sb]

            if action == "SW":
                add_node(t+1, min(sw+1, max_sw), sb, path + "S")
                dot.edge(node_id, f"{t+1}_{min(sw+1, max_sw)}_{sb}", label="✅")
                add_node(t+1, sw, sb, path + "s")
                # dot.edge(node_id, f"{t+1}_{sw}_{sb}", label=r"fail")
                dot.edge(node_id, f"{t + 1}_{sw}_{sb}", label="❌")

            elif action == "SB":
                add_node(t + 1, sw, min(sb + 1, max_sb), path + "B")
                dot.edge(node_id, f"{t + 1}_{sw}_{min(sb + 1, max_sb)}", label="✅")
                add_node(t + 1, sw, sb, path + "b")
                # dot.edge(node_id, f"{t + 1}_{sw}_{sb}", label=r"fail")
                dot.edge(node_id, f"{t + 1}_{sw}_{sb}", label="❌")

            elif action == "B":
                add_node(t + 1, sw, sb, path + "E")
                dot.edge(node_id, f"{t + 1}_{sw}_{sb}", label="eat")

        add_node(0, 1, 0)
        return dot

    import graphviz

    def visualize_full_policy_tree(self, swim_success, sun_success, max_t=10, max_sw=7, max_sb=7):
        dot = Digraph(comment="Full Optimal Policy Tree")

        visited = set()

        def add_state(t, sw, sb):
            node_id = f"{t}_{sw}_{sb}"
            label = f"t={t}\nsw={sw}\nsb={sb}"
            dot.node(node_id, label=label)
            return node_id

        def recurse(t, sw, sb):
            if t >= max_t or sw > max_sw or sb > max_sb:
                return

            state_id = f"{t}_{sw}_{sb}"
            if state_id in visited:
                return
            visited.add(state_id)

            action = self.policy[t][sw][sb]
            current_node = add_state(t, sw, sb)

            if action == "E":
                next_id = add_state(t + 1, sw, sb)
                dot.edge(current_node, next_id, label="E")
                recurse(t + 1, sw, sb)
            elif action == "SW":
                p = swim_success[t]
                sw_succ = min(sw + 1, max_sw)
                next_succ = add_state(t + 1, sw_succ, sb)
                next_fail = add_state(t + 1, sw, sb)
                dot.edge(current_node, next_succ, label=f"SW ✅ ({p})")
                dot.edge(current_node, next_fail, label=f"SW ❌ ({1 - p})")
                recurse(t + 1, sw_succ, sb)
                recurse(t + 1, sw, sb)
            elif action == "SB":
                p = sun_success[t]
                sb_succ = min(sb + 1, max_sb)
                next_succ = add_state(t + 1, sw, sb_succ)
                next_fail = add_state(t + 1, sw, sb)
                dot.edge(current_node, next_succ, label=f"SB ✅ ({p})")
                dot.edge(current_node, next_fail, label=f"SB ❌ ({1 - p})")
                recurse(t + 1, sw, sb_succ)
                recurse(t + 1, sw, sb)

        recurse(0, 0, 0)
        return dot

