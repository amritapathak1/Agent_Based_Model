# SugarScape with Emotion-Driven Ethics

This project extends the classic Epstein & Axtell SugarScape agent-based model to simulate emotion-driven decision-making and probabilistic ethical violations. 
Agents will occasionally **break rules** and steal sugar from occupied cells when under **resource stress** (e.g., panic from low reserves), depending on individualized traits like **risk aversion**, **overconfidence**, and an **ethics threshold**.

Note: To evaluate the dynamics of ethical breakdown under increased emotional pressure, we configured a high-stress simulation environment by modifying key model parameters. 
Specifically, we reduced the maximum initial endowment from 100 to 50, increased the maximum metabolism from 5 to 8, and raised the initial population to 300 agents within a 50x50 grid. 
These adjustments were designed to intensify competition for sugar and raise the likelihood that agents would enter a panic state (in_panic = True). 
The scarcity of resources under these settings provided a testbed for observing how often and how quickly agents violated ethical norms in pursuit of survival.

---

## How to Run

To launch the interactive simulation locally using [Solara](https://solara.dev):

```bash
solara run app.py
```

## Files Overview

| File | Description |
|------|-------------|
| [`app.py`](./app.py) | Main entry point for the **Solara-based GUI**. Defines sliders for model parameters and visual encoding for agents (e.g., color for ethical violations). |
| [`model.py`](./model.py) | Contains the `SugarScapeModel` class. Manages the simulation logic, data collection, sugar regrowth, and step-by-step updates. |
| [`agents.py`](./agents.py) | Defines the `SugarAgent` class. Implements panic-driven rule-breaking, emotion-based traits, movement logic, sugar gathering, and death conditions. |
| [`run_simulation.py`](./run_simulation.py) | Script for running the model **in headless mode** (no GUI) and saving results like Gini coefficients and unethical moves to CSV. |
| [`sugar-map.txt`](./sugar-map.txt) | Initial sugar distribution on the grid, loaded as a property layer by the model. Must be present for the simulation to run. |


