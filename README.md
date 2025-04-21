# SugarScape with Emotion-Driven Ethics

This project extends the classic Epstein & Axtell SugarScape agent-based model to simulate emotion-driven decision-making and probabilistic ethical violations. 
Agents will occasionally **break rules** and steal sugar from occupied cells when under **resource stress** (e.g., panic from low reserves), depending on individualized traits like **risk aversion**, **overconfidence**, and an **ethics threshold**.

---

## How to Run

To launch the interactive simulation locally using [Solara](https://solara.dev):

```bash
solara run app.py


## Files Overview

| File | Description |
|------|-------------|
| [`app.py`](./app.py) | Main entry point for the **Solara-based GUI**. Defines sliders for model parameters and visual encoding for agents (e.g., color for ethical violations). |
| [`model.py`](./model.py) | Contains the `SugarScapeModel` class. Manages the simulation logic, data collection, sugar regrowth, and step-by-step updates. |
| [`agents.py`](./agents.py) | Defines the `SugarAgent` class. Implements panic-driven rule-breaking, emotion-based traits, movement logic, sugar gathering, and death conditions. |
| [`run_simulation.py`](./run_simulation.py) | Script for running the model **in headless mode** (no GUI) and saving results like Gini coefficients and unethical moves to CSV. |
| [`sugar-map.txt`](./sugar-map.txt) | Initial sugar distribution on the grid, loaded as a property layer by the model. Must be present for the simulation to run. |


