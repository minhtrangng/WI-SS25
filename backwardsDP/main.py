import random
import matplotlib.pyplot as plt

class EinTagAmSee:
    def __init__(self):
        # Parameter
        self.actions = ["B", "S", "I"]  # Baden, Sonnen, Imbiss
        self.hours = list(range(10, 21))  # 10:00 bis 20:00 (11 Entscheidungsstufen)

        # Erfolgswahrscheinlichkeiten
        self.p_B = [0.05, 0.05, 0.10, 0.15, 0.20, 0.20, 0.25, 0.25, 0.25, 0.15, 0.10]
        self.p_S = [0.15, 0.25, 0.30, 0.35, 0.35, 0.30, 0.20, 0.10, 0.05, 0, 0]

        # Belohnungen
        self.rewards = {"B": 10, "S": 5, "I": 5}

        # Perfekter Tag Bedingungen
        self.min_baden = 2
        self.min_sonnen = 2
        self.strafe_nicht_perfekt = -100

        # Realistische Obergrenze für erfolgreiche Aktionen
        self.max_realistic = 7

        # Ergebnisse
        self.V = {}
        self.policy = {}

    def solve(self):
        """Löst das Problem mit Backward Dynamic Programming"""
        self._set_terminal_conditions()
        self._backward_iteration()
        return self.V, self.policy

    def _set_terminal_conditions(self):
        """Setzt die Terminalbedingungen für 21:00 Uhr"""
        for b in range(self.max_realistic + 1):
            for s in range(self.max_realistic + 1):
                if b >= self.min_baden and s >= self.min_sonnen:
                    self.V[(21, b, s)] = 0  # Perfekter Tag
                else:
                    self.V[(21, b, s)] = self.strafe_nicht_perfekt  # Nicht perfekt

    def _backward_iteration(self):
        """Rückwärtsiteration von 20:00 bis 10:00"""
        for t in reversed(self.hours):  # 20, 19, ..., 10
            time_idx = self.hours.index(t)
            for b in range(self.max_realistic + 1):
                for s in range(self.max_realistic + 1):
                    best_value = float('-inf')
                    best_action = None
                    for action in self.actions:
                        value = self._calculate_action_value(action, t, b, s, time_idx)
                        if value > best_value:
                            best_value = value
                            best_action = action
                    self.V[(t, b, s)] = best_value
                    self.policy[(t, b, s)] = best_action

    def _calculate_action_value(self, action, t, b, s, time_idx):
        """Berechnet erwarteten Wert einer Aktion"""
        if action == "B":
            p_success = self.p_B[time_idx] * 2
            new_b = min(b + 1, self.max_realistic)
            success_value = self.rewards["B"] + self.V.get((t+1, new_b, s), self.strafe_nicht_perfekt)
            fail_value = self.V.get((t+1, b, s), self.strafe_nicht_perfekt)
            return p_success * success_value + (1 - p_success) * fail_value
        elif action == "S":
            p_success = self.p_S[time_idx] * 2
            new_s = min(s + 1, self.max_realistic)
            success_value = self.rewards["S"] + self.V.get((t+1, b, new_s), self.strafe_nicht_perfekt)
            fail_value = self.V.get((t+1, b, s), self.strafe_nicht_perfekt)
            return p_success * success_value + (1 - p_success) * fail_value
        else:  # "I"
            return self.rewards["I"] + self.V.get((t+1, b, s), self.strafe_nicht_perfekt)

    def get_optimal_value(self):
        return self.V.get((10, 0, 0), "Nicht gefunden")

    def print_V(self):
        print("\n📊 WERTFUNKTION V:")
        print("=" * 50)
        sorted_states = sorted(self.V.keys(), key=lambda x: (x[0], x[1], x[2]))
        current_time = None
        for state in sorted_states:
            t, b, s = state
            value = self.V[state]
            if t != current_time:
                print(f"\n🕐 {t}:00 Uhr:")
                current_time = t
            print(f"   V({t}, {b}, {s}) = {value:7.2f}")

    def print_policy(self):
        print("\n📋 OPTIMALE POLICY:")
        print("=" * 50)
        action_names = {"B": "Baden 🏊‍♂️", "S": "Sonnen ☀️", "I": "Imbiss 🍔"}
        sorted_states = sorted(self.policy.keys(), key=lambda x: (x[0], x[1], x[2]))
        current_time = None
        for state in sorted_states:
            t, b, s = state
            action = self.policy[state]
            action_name = action_names.get(action, action)
            if t != current_time:
                print(f"\n🕐 {t}:00 Uhr:")
                current_time = t
            print(f"   π({t}, {b}, {s}) = {action} ({action_name})")

    def simulate_success_probability(self, num_simulations=1000):
        print(f"\n🎲 Simuliere {num_simulations:,} Tage...")
        successful_days = 0
        for _ in range(num_simulations):
            b, s = 0, 0
            for t in self.hours:
                time_idx = self.hours.index(t)
                action = self.policy.get((t, min(b, self.max_realistic), min(s, self.max_realistic)), "I")
                if action == "B" and random.random() < self.p_B[time_idx]:
                    b = min(b + 1, self.max_realistic)
                elif action == "S" and random.random() < self.p_S[time_idx]:
                    s = min(s + 1, self.max_realistic)
            if b >= self.min_baden and s >= self.min_sonnen:
                successful_days += 1
        probability = successful_days / num_simulations
        print(f"   Perfekte Tage: {successful_days:,}")
        print(f"   Wahrscheinlichkeit: {probability:.3f} ({probability*100:.1f}%)")
        return probability

    def print_optimal_path(self):
        """Gibt nur den optimalen Pfad vom Startzustand aus aus"""
        t, b, s = 10, 0, 0
        print(f"\n🚩 OPTIMALER PFAD (Start bei V(10,0,0)):")
        print("=" * 40)
        for step in range(len(self.hours)):
            action = self.policy.get((t, b, s), "I")
            value = self.V.get((t, b, s), None)
            print(f"{t}:00 | V({t},{b},{s}) = {value:7.2f} | Aktion: {action}")
            # Simuliere den optimalen Übergang (ohne Zufall, aber mit Erwartungswert)
            if action == "B":
                # Nimm an, es klappt (für den Pfad) – alternativ könntest du beide Fälle zeigen
                b = min(b + 1, self.max_realistic)
            elif action == "S":
                s = min(s + 1, self.max_realistic)
            # Imbiss: b und s bleiben gleich
            t += 1
            if t > 20:
                break
        # Terminalzustand
        term_value = self.V.get((21, b, s), None)
        print(f"21:00 | V(21,{b},{s}) = {term_value:7.2f} | (Terminal)")


def main():
    see = EinTagAmSee()
    see.solve()
    #see.print_optimal_path()
    #print(see.get_optimal_value())
    see.print_V()
    #see.print_policy()
    see.simulate_success_probability()

if __name__ == "__main__":
    main()
