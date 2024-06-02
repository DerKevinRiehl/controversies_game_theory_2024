import numpy as np
import pandas as pd
from population import initializePopulation, updateUrgencyAndVOT
from models import travel_time_model_random, makeDecision
from plotting import plot_results
from helpers import set_seed, load_parameters_json

def run_simulation(simulation_time: int, pop_size: int, urgency_scenario: int, history_length_personal: int, history_length_reported: int, exploration_rate: float, system_optimum: int, nash_equilibrium: int, config) -> None:
    """Run the entire simulation"""

    if simulation_time < 0:
        raise ValueError("Simulation time can't be negative in run_simulation()")
    if exploration_rate < 0:
        raise ValueError("Exploration rate can't be negative in run_simulation()")
    if history_length_personal < 0:
        raise ValueError("history_length_personal can't be negative in run_simulation()")
    if history_length_reported < 0:
        raise ValueError("history_length_reported can't be negative in run_simulation()")


    set_seed(42)

    # Initialize Population
    population = initializePopulation(pop_size, urgency_scenario)

    # Initialize Population Memory
    memory_route_A = [[] for i in range(0, len(population))]
    memory_route_B = [[] for i in range(0, len(population))]
    history_reported_A = []
    history_reported_B = []

    # Init Recording
    df_records = pd.DataFrame([], columns=["time", "flow_A", "flow_B", "mean_traveltime_A", "mean_traveltime_B"])

    
    # Iterate Over Time
    for time in range(0, simulation_time):
        # make decisions
        decisions = np.asarray([makeDecision(
                exploration_rate = exploration_rate,
                urgency = population["urgency"].iloc[idx],
                salary = population["salary"].iloc[idx],
                memory_routeA = memory_route_A[idx], 
                memory_routeB = memory_route_B[idx], 
                history_reportedA = history_reported_A, 
                history_reportedB = history_reported_B
            ) for idx in range(0, len(population))])
        
        # generate travel times
        flow_A = len(decisions) - sum(decisions)
        flow_B = sum(decisions)
        travel_times = np.asarray([travel_time_model_random(route, flow_A, flow_B) for route in decisions])
        mean_traveltime_A = np.mean(travel_times[decisions==0])
        mean_traveltime_B = np.mean(travel_times[decisions==1])
        
        # update histories
            # update reported history
        history_reported_A.append(mean_traveltime_A)
        history_reported_B.append(mean_traveltime_B)
            # Remove oldest time in the reported memory
        if len(history_reported_A) > history_length_reported:
            history_reported_A.pop(0)
        if len(history_reported_B) > history_length_reported:
            history_reported_B.pop(0)
            # update memory history for each individual
        for idx in range(0, len(decisions)):
            decision = decisions[idx]
            if decision==0:
                memory_route_A[idx].append(travel_times[idx])
                # removes oldest memory, after enough time
                if len(memory_route_A[idx]) > history_length_personal:
                    memory_route_A[idx].pop(0)
            else:
                memory_route_B[idx].append(travel_times[idx])
                # removes oldest memory, after enough time
                if len(memory_route_B[idx]) > history_length_personal:
                    memory_route_B[idx].pop(0)
            
        # recording
        df_records.loc[len(df_records.index)] = [time, flow_A, flow_B, mean_traveltime_A, mean_traveltime_B] 
            
        # update urgencies randomly
        population = updateUrgencyAndVOT(population, urgency_scenario)
        
        print(f"Time step {time + 1}/{simulation_time} completed")
    
    plot_results(df_records, system_optimum, nash_equilibrium, config)

if __name__ == "__main__":
    # Parameters from a json file
    config = load_parameters_json("config.json")

    run_simulation(simulation_time=config["simulation_time"], pop_size=config['pop_size'], urgency_scenario=config['urgency_scenario'], history_length_personal=config['history_length_personal'], history_length_reported=config['history_length_reported'], exploration_rate=config['exploration_rate'], system_optimum=config['system_optimum'], nash_equilibrium=config['nash_equilibrium'], config=config)