from pathlib import Path
import numpy as np
import mesa
from agents import SugarAgent

# Use Mesa's experimental spatial grid and property layer
from mesa.experimental.cell_space import OrthogonalVonNeumannGrid
from mesa.experimental.cell_space.property_layer import PropertyLayer

class SugarScapeModel(mesa.Model):
    """
    The main SugarScape model class.

    Attributes:
        grid: The spatial grid environment.
        agents: List of SugarAgent instances in the model.
        sugar_distribution: The initial landscape of sugar quantities.
        unethical_moves: Counter for the number of rule violations by agents.
        datacollector: Mesa's built-in tool for tracking model statistics over time.
        step_count: Manual timestep counter for logging.
    """

    def calc_gini(self):
        """
        Calculate the Gini coefficient of sugar wealth among agents.

        Returns:
            float: Gini coefficient (0 = perfect equality, 1 = perfect inequality).
        """
        agent_sugars = [a.sugar for a in self.agents]
        sorted_sugars = sorted(agent_sugars)
        n = len(sorted_sugars)
        x = sum(el * (n - ind) for ind, el in enumerate(sorted_sugars)) / (n * sum(sorted_sugars))
        return 1 + (1 / n) - 2 * x

    def __init__(
        self,
        width=50,
        height=50,
        initial_population=200,
        endowment_min=25,
        endowment_max=50,
        metabolism_min=1,
        metabolism_max=5,
        vision_min=1,
        vision_max=5,
        seed=None
    ):
        """
        Initialize the SugarScapeModel with grid, agents, and parameters.
        """
        super().__init__(seed=seed)
        self.width = width
        self.height = height
        self.running = True
        self.unethical_moves = 0  # Track unethical actions taken by agents
        self.step_count = 0       # Track steps manually

        # Create grid
        self.grid = OrthogonalVonNeumannGrid((self.width, self.height), torus=False, random=self.random)

        # Load sugar map and define it as a property layer
        self.sugar_distribution = np.genfromtxt(Path(__file__).parent / "sugar-map.txt")
        self.grid.add_property_layer(
            PropertyLayer.from_data("sugar", self.sugar_distribution)
        )

        # Create agents
        SugarAgent.create_agents(
            self,
            initial_population,
            self.random.choices(self.grid.all_cells.cells, k=initial_population),
            sugar=self.rng.integers(endowment_min, endowment_max, (initial_population,), endpoint=True),
            metabolism=self.rng.integers(metabolism_min, metabolism_max, (initial_population,), endpoint=True),
            vision=self.rng.integers(vision_min, vision_max, (initial_population,), endpoint=True),
        )

        # Set up data collection
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Gini": self.calc_gini,
                "UnethicalMoves": lambda m: m.unethical_moves,
            },
        )

        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step:
        - Regrow sugar (up to original levels)
        - Move all agents
        - Have them gather and eat sugar
        - Check if they survive
        - Track step count
        - Log unethical actions
        - Collect updated statistics
        """
        # Reset just_cheated after visualization has occurred
        for agent in self.agents:
            agent.just_cheated = False
        
        self.grid.sugar.data = np.minimum(
            self.grid.sugar.data + 1, self.sugar_distribution
        )

        self.agents.shuffle_do("move")
        self.agents.shuffle_do("gather_and_eat")
        self.agents.shuffle_do("see_if_die")

        self.step_count += 1
        print(f"Step {self.step_count}: Unethical moves = {self.unethical_moves}")

        self.datacollector.collect(self)


    def save_results(self, filename="simulation_results.csv"):
        """
        Save model-level output (Gini, unethical moves) to a CSV file.

        Parameters:
            filename (str): File name for the CSV output.
        """
        df = self.datacollector.get_model_vars_dataframe()
        df.to_csv(filename, index_label="Step")
        print(f"Results saved to {filename}")
