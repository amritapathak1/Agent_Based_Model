# run_simulation.py
from model import SugarScapeModel

def main(
    steps: int = 100,
    output_csv: str = "simulation_results.csv",
    **model_kwargs,
):
    # 1. Create the model
    model = SugarScapeModel(**model_kwargs)
    
    # 2. Run it for a fixed number of steps
    for _ in range(steps):
        model.step()
    
    # 3. Save results
    model.save_results(filename=output_csv)
    print(f"Done: ran {steps} steps and wrote {output_csv}")

if __name__ == "__main__":
    # Example: 200 steps, seed=42, 300 agents
    main(steps=200, output_csv="results.csv", seed=42, initial_population=300)
