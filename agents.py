import math
from mesa.experimental.cell_space import CellAgent

def get_distance(cell_1, cell_2):
    """
    Calculate Euclidean distance between two grid cells.

    Parameters:
        cell_1, cell_2: Cell objects with `.coordinate` (x, y)

    Returns:
        float: The Euclidean distance between the two cells.
    """
    x1, y1 = cell_1.coordinate
    x2, y2 = cell_2.coordinate
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx**2 + dy**2)

class SugarAgent(CellAgent):
    """
    An agent in the SugarScape model, extended to simulate emotion-driven heuristics
    and probabilistic ethical rule violations under stress (e.g., panic).

    Attributes:
        sugar (int): The agent's current sugar reserve.
        metabolism (int): The sugar cost per timestep to stay alive.
        vision (int): Number of cells the agent can observe in cardinal directions.
        risk_aversion (float): Tendency to avoid high-risk situations (0 = risk-seeking, 1 = risk-averse).
        overconfidence (float): Degree to which the agent overestimates outcomes (1 = highly overconfident).
        ethics_threshold (float): Probability the agent will *not* break rules under pressure.
        in_panic (bool): True if the agent’s sugar level is dangerously low.
        just_cheated (bool): True if the agent violated ethics this step (used for visualization).
    """

    def __init__(self, model, cell, sugar=0, metabolism=0, vision=0):
        """
        Initialize the agent with its traits and initial state.

        Parameters:
            model: The SugarScape model instance.
            cell: The starting cell for this agent.
            sugar: Initial sugar held by the agent.
            metabolism: Sugar cost per step.
            vision: Number of cells visible in cardinal directions.
        """
        super().__init__(model)
        self.cell = cell
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision

        # Emotion-driven heuristics
        self.risk_aversion = self.random.uniform(0, 1)
        self.overconfidence = self.random.uniform(0, 1)
        self.ethics_threshold = self.random.uniform(0.1, 0.6)
        self.in_panic = False

        # Visualization flag
        self.just_cheated = False

    def move(self):
        """
        Move the agent to a new cell.

        If the agent is in panic and fails the ethical check, it may move unethically
        by stealing sugar from a neighboring occupied cell. Otherwise, it picks the
        best unoccupied sugar-rich cell within its vision.
        """
        # ✅ Reset visualization flag at the start of each step
        self.just_cheated = False

        if self.in_panic and self.random.random() > self.ethics_threshold:
            neighbors = self.cell.get_neighborhood(self.vision, include_center=False)
            occupied_neighbors = [c for c in neighbors if not c.is_empty]
            if occupied_neighbors:
                target = self.random.choice(occupied_neighbors)
                self.sugar += target.sugar
                target.sugar = 0
                self.model.unethical_moves += 1
                self.just_cheated = True

                # Logging unethical behavior
                print(f"[CHEAT] Agent {self.unique_id} stole sugar at step {getattr(self.model, 'step_count', '?')}")
                return

        # Ethical move: choose the best unoccupied cell
        possibles = [
            cell for cell in self.cell.get_neighborhood(self.vision, include_center=True)
            if cell.is_empty
        ]
        if not possibles:
            return

        sugar_values = [cell.sugar for cell in possibles]
        max_sugar = max(sugar_values)
        best_indices = [i for i, s in enumerate(sugar_values) if math.isclose(s, max_sugar)]
        candidates = [possibles[i] for i in best_indices]

        min_dist = min(get_distance(self.cell, c) for c in candidates)
        final_candidates = [
            c for c in candidates if math.isclose(get_distance(self.cell, c), min_dist, rel_tol=1e-2)
        ]

        self.cell = self.random.choice(final_candidates)

    def gather_and_eat(self):
        """
        Collect sugar from the current cell and consume sugar based on metabolism.

        Also updates panic state and optionally logs if agent had cheated.
        """
        self.sugar += self.cell.sugar
        self.cell.sugar = 0
        self.sugar -= self.metabolism
        self.in_panic = self.sugar < 10

        if self.just_cheated:
            print(f"[RESET] Agent {self.unique_id} is resetting just_cheated flag after gather.")

    def see_if_die(self):
        """
        Remove the agent if its sugar reserve is zero or below.
        """
        if self.sugar <= 0:
            self.remove()

    @property
    def color(self):
        """
        Define visualization color based on internal agent state.

        Returns:
            str: Color string for use in visualization.
        """
        if self.just_cheated:
            return "deeppink"  # Actively cheating agent
        elif self.metabolism > 3:
            return "red"
        elif self.vision > 5:
            return "green"
        else:
            return "blue"
