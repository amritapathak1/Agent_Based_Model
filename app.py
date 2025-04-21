from model import SugarScapeModel
from mesa.visualization import Slider, SolaraViz, make_plot_component
from mesa.visualization.components.matplotlib_components import make_mpl_space_component

# Define agent portrayal (color, size, shape)

def agent_portrayal(agent):
    is_cheater = getattr(agent, "just_cheated", False)
    if is_cheater:
        return {
            "marker": "o",         # or "X"
            "color": "red",   # or something super visible
            "size": 20,
        }
    return {
        "marker": "o",
        "color": "blue",
        "size": 20,
    }



# Define map portrayal, with yellower squares having more sugar than white squares
propertylayer_portrayal = {
    "sugar": {
        "color": "yellow",
        "alpha": 0.8,
        "colorbar": True,
        "vmin": 0,
        "vmax": 10,
    },
}

# Define model space component
sugarscape_space = make_mpl_space_component(
    agent_portrayal=agent_portrayal,
    propertylayer_portrayal=propertylayer_portrayal,
    post_process=None,
    draw_grid=False,
)

# Define plot components
GiniPlot = make_plot_component("Gini")
UnethicalPlot = make_plot_component("UnethicalMoves")

# Define variable model parameters
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "width": 50,
    "height": 50,
    "initial_population": Slider(
        "Initial Population", value=300, min=50, max=500, step=10
    ),
    "endowment_min": Slider("Min Initial Endowment", value=25, min=5, max=30, step=1),
    "endowment_max": Slider("Max Initial Endowment", value=50, min=30, max=100, step=1),
    "metabolism_min": Slider("Min Metabolism", value=1, min=1, max=3, step=1),
    "metabolism_max": Slider("Max Metabolism", value=7, min=3, max=8, step=1),
    "vision_min": Slider("Min Vision", value=1, min=1, max=3, step=1),
    "vision_max": Slider("Max Vision", value=5, min=3, max=8, step=1),
}

# Instantiate model
model = SugarScapeModel()

# Define and return the full visualization page
page = SolaraViz(
    model,
    components=[
        sugarscape_space,
        GiniPlot,
        UnethicalPlot,
    ],
    model_params=model_params,
    name="Sugarscape",
    play_interval=400,  # ⏱️ Slower to help visualize purple flash
)

page
