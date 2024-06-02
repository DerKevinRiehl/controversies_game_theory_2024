import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

def plot_results(df_records : pd.DataFrame, system_optimum: int, nash_equilibrium:int, config) -> None:
    """Plot simulation results to a file in /plots"""
    # Plot Results
    plt.figure(figsize=(12,8))
    
    plt.subplot(1,2,1)
    plt.title("Split")
    plt.plot(df_records["time"], df_records["flow_A"], label="Split (Flow on Route A)")
    plt.xlabel("# Times")
    plt.ylabel("Split (Route A, # veh)")
    plt.plot([0, df_records["time"].iloc[-1]], [system_optimum, system_optimum], "--", label="System Optimum")
    plt.plot([0, df_records["time"].iloc[-1]], [nash_equilibrium, nash_equilibrium], "--", label="Nash Equilibrium")
    plt.grid()
    plt.legend()

    plt.subplot(1,2,2)
    plt.title("Travel Times per Route")
    plt.plot(df_records["time"], df_records["mean_traveltime_A"], label="Lincoln Tunnel (Route A)")
    plt.plot(df_records["time"], df_records["mean_traveltime_B"], label="George Washington Bridge (Route B)")
    plt.xlabel("# Times")
    plt.ylabel("Travel Time [minutes]")
    plt.grid()
    plt.legend()

    # Add a box with the variables to the graphs
    config_text = (
        f"Simulation Timesteps: {config['simulation_time']}\n"
        f"Population Size: {config['pop_size']}\n"
        f"Urgency Scenario: {config['urgency_scenario']}\n"
        f"Personal History Length: {config['history_length_personal']}\n"
        f"Reported History Length: {config['history_length_reported']}\n"
        f"Exploration Rate: {config['exploration_rate']}\n"
        f"Seed: {config['seed']}"
    )
    plt.figtext(0.5,0.8,config_text, ha="center", fontsize=10,bbox={"facecolor": "white", "alpha": 1, "pad": 5})

    # Print the plot into a folder, with a unique name (containing date and time)
    if not os.path.exists("plots"):
        os.makedirs("plots")
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'simulation_results_{current_time}.png'
    plt.savefig("plots/"+filename)