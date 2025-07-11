import random

class EinTagAmSeeKorrekt:
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
        self.belohnung_perfekt = 20

        # Realistische Obergrenze für erfolgreiche Aktionen
        self.max_realistic = 7

        # Ergebnisse - korrekte Struktur
        self.V = {}  # V[t][state] = Wert für Zustand 'state' in Stufe t
        self.policy = {}  # policy[t][state] = optimale Aktion für Zustand 'state' in Stufe t

    def _set_terminal_conditions(self):
        """
        Setzt die Terminalbedingungen für t=0 (21 Uhr)
        Zustand: (b, s) - Anzahl erfolgreicher Bäder und Sonnenbäder
        """
        self.V[0] = {}

        for b in range(self.max_realistic + 1):
            for s in range(self.max_realistic + 1):
                state = (b, s)

                # Terminaler Wert: 0 wenn perfekter Tag, sonst Strafe
                if b >= self.min_baden and s >= self.min_sonnen:
                    self.V[0][state] = self.belohnung_perfekt  # Perfekter Tag
                else:
                    self.V[0][state] = self.strafe_nicht_perfekt  # Nicht perfekt: -100

    def _backward_iteration(self):
        """
        Führt die Rückwärts-DP-Iteration durch
        Berechnet V_t(s) für alle Stufen t = 1, 2, ..., 11
        """
        # Rückwärts von t=1 (20 Uhr) bis t=11 (10 Uhr)
        for t in range(1, len(self.hours) + 1):
            self.V[t] = {}
            self.policy[t] = {}

            # Index für Wahrscheinlichkeits-Arrays (0-basiert)
            hour_index = len(self.hours) - t

            # Für alle möglichen Zustände (b, s)
            for b in range(self.max_realistic + 1):
                for s in range(self.max_realistic + 1):
                    state = (b, s)

                    best_value = float('-inf')
                    best_action = None

                    # Teste alle möglichen Aktionen
                    for action in self.actions:
                        expected_value = self._calculate_expected_value(
                            state, action, hour_index, t)

                        if expected_value > best_value:
                            best_value = expected_value
                            best_action = action

                    # Speichere optimalen Wert und Aktion
                    self.V[t][state] = best_value
                    self.policy[t][state] = best_action

    def _calculate_expected_value(self, state, action, hour_index, t):
        """
        Berechnet den erwarteten Wert für eine Aktion in einem gegebenen Zustand

        Args:
            state: (b, s) - aktueller Zustand
            action: "B", "S", oder "I" - gewählte Aktion
            hour_index: Index für Wahrscheinlichkeits-Arrays
            t: aktuelle Stufe

        Returns:
            Erwarteter Wert der Aktion
        """
        b, s = state

        # Erfolgswahrscheinlichkeit und Belohnung bestimmen
        if action == "B":
            p_success = self.p_B[hour_index]
            reward = self.rewards["B"]
        elif action == "S":
            p_success = self.p_S[hour_index]
            reward = self.rewards["S"]
        else:  # action == "I"
            p_success = 1.0  # Imbiss ist immer erfolgreich
            reward = self.rewards["I"]

        # Folgezustände berechnen
        if action == "B":
            # Bei erfolgreichem Baden: b erhöht sich
            b_success = min(b + 1, self.max_realistic)
            s_success = s
        elif action == "S":
            # Bei erfolgreichem Sonnen: s erhöht sich
            b_success = b
            s_success = min(s + 1, self.max_realistic)
        else:  # action == "I"
            # Imbiss ändert b und s nicht
            b_success = b
            s_success = s

        # Zustände für Erfolg und Misserfolg
        state_success = (b_success, s_success)
        state_fail = (b, s)  # Bei Misserfolg bleibt Zustand gleich

        # Erwarteter Wert berechnen
        if action == "I":
            # Imbiss ist immer erfolgreich
            expected_value = reward + self.V[t - 1][state_success]
        else:
            # Erwartungswert über Erfolg/Misserfolg
            value_success = reward + self.V[t - 1][state_success]
            value_fail = 0 + self.V[t - 1][state_fail]  # Keine Belohnung bei Misserfolg

            expected_value = p_success * value_success + (1 - p_success) * value_fail

        return expected_value

    def solve(self):
        """Löst das Problem mit korrekter MDP-Modellierung"""
        self._set_terminal_conditions()
        self._backward_iteration()
        return self.V, self.policy

    def get_optimal_value(self):
        """Gibt den optimalen Wert V*_11(0,0) zurück (Startzustand um 10 Uhr)"""
        return self.V[len(self.hours)][(0, 0)]

    def print_policy_compact(self):
        """Gibt die optimale Strategie in kompakter Form aus - INKLUSIVE t=0"""
        print("Optimale Strategie (Stufe -> Zustand -> Aktion/Wert):")
        print("=" * 60)

        # Zeige ALLE Stufen von t=11 bis t=0
        for t in range(len(self.hours), -1, -1):  # Jetzt bis -1, damit 0 inkludiert ist
            if t == 0:
                print(f"\nV_{t}(b,s) (Stufe t={t} -> 21:00 Uhr - TERMINAL):")
                print("  Terminalwerte (keine Aktionen mehr möglich):")

                # Zeige Terminalwerte
                for b in range(min(4, self.max_realistic + 1)):
                    for s in range(min(4, self.max_realistic + 1)):
                        state = (b, s)
                        if state in self.V[t]:
                            value = self.V[t][state]
                            status = "PERFEKT" if value == 0 else "NICHT PERFEKT"
                            print(f"    (b={b}, s={s}): V={value:4.0f} ({status})")
            else:
                hour = self.hours[len(self.hours) - t]
                print(f"\nV_{t}(b,s) (Stufe t={t} -> {hour}:00 Uhr):")

                # Zeige Aktionen und Werte
                for b in range(min(4, self.max_realistic + 1)):
                    for s in range(min(4, self.max_realistic + 1)):
                        state = (b, s)
                        if state in self.policy[t]:
                            action = self.policy[t][state]
                            value = self.V[t][state]
                            print(f"    (b={b}, s={s}): {action} (V={value:6.2f})")

    def simulate_success_probability(self, num_simulations=100000):
        """
        Simuliert die Wahrscheinlichkeit für einen perfekten Tag unter optimaler Strategie

        Args:
            num_simulations: Anzahl der Monte-Carlo-Simulationen

        Returns:
            Wahrscheinlichkeit für einen perfekten Tag (0.0 bis 1.0)
        """
        count_perfect = 0

        for _ in range(num_simulations):
            b = 0  # Anzahl erfolgreicher Bäder
            s = 0  # Anzahl erfolgreicher Sonnenbäder

            # Simuliere einen kompletten Tag
            for t in range(len(self.hours), 0, -1):
                state = (b, s)
                action = self.policy[t][state]
                hour_index = len(self.hours) - t

                # Führe Aktion aus
                if action == "B":
                    p_success = self.p_B[hour_index]
                    if random.random() < p_success:
                        b = min(b + 1, self.max_realistic)
                elif action == "S":
                    p_success = self.p_S[hour_index]
                    if random.random() < p_success:
                        s = min(s + 1, self.max_realistic)
                # Imbiss ist immer erfolgreich, ändert aber b und s nicht

            # Prüfe ob perfekter Tag erreicht wurde
            if b >= self.min_baden and s >= self.min_sonnen:
                count_perfect += 1

        return count_perfect / num_simulations

    def print_detailed_results(self):
        """Gibt detaillierte Ergebnisse für alle Aufgabenteile aus"""
        print("=" * 70)
        print("LÖSUNG: Ein Tag am See - Backward Dynamic Programming")
        print("=" * 70)

        # a) Optimale Strategie
        print("\na) OPTIMALE STRATEGIE:")
        print("-" * 30)
        self.print_policy_compact()

        # b) Optimaler Wert
        optimal_value = self.get_optimal_value()
        print(f"\nb) OPTIMALER WERT V*:")
        print("-" * 20)
        print(f"V*_11(0,0) = {optimal_value:.4f}")
        print(f"(Erwarteter Nutzen bei optimalem Verhalten ab 10:00 Uhr)")

        # c) Wahrscheinlichkeit für perfekten Tag
        print(f"\nc) WAHRSCHEINLICHKEIT FÜR PERFEKTEN TAG:")
        print("-" * 40)
        print("Berechnung läuft... (100.000 Simulationen)")
        prob_perfect = self.simulate_success_probability()
        print(f"Wahrscheinlichkeit: {prob_perfect:.6f} ({prob_perfect * 100:.4f}%)")

        # Zusätzliche Analyse
        print(f"\nZUSÄTZLICHE ANALYSE:")
        print("-" * 20)
        print(f"• Mindestanforderungen: {self.min_baden} Bäder + {self.min_sonnen} Sonnenbäder")
        print(f"• Strafe für nicht-perfekten Tag: {self.strafe_nicht_perfekt}")
        print(f"• Anzahl Entscheidungsstufen: {len(self.hours)}")
        print(f"• Zustandsraum-Größe pro Stufe: {(self.max_realistic + 1) ** 2}")

    def print_strategy_summary(self):
        """Gibt eine kompakte Zusammenfassung der Strategie aus"""
        print("\nSTRATEGIE-ZUSAMMENFASSUNG:")
        print("-" * 30)

        # Analysiere Strategie für Startzustand
        for t in range(len(self.hours), 0, -1):
            hour = self.hours[len(self.hours) - t]
            state = (0, 0)  # Startzustand
            if state in self.policy[t]:
                action = self.policy[t][state]
                value = self.V[t][state]
                print(f"{hour}:00 Uhr - Aktion: {action} (Wert: {value:.2f})")


def main():
    """Hauptfunktion - löst alle Aufgabenteile"""
    see = EinTagAmSeeKorrekt()

    print("Starte Backward Dynamic Programming...")
    see.solve()

    print("Berechnung abgeschlossen!\n")
    see.print_detailed_results()

    # Optional: Kompakte Strategieübersicht
    see.print_strategy_summary()


if __name__ == "__main__":
    main()
