import numpy as np
import pandas as pd
from population import initializePopulation, updateUrgencyAndVOT
from models import travel_time_model_random, expected_cost_model
from plotting import plot_results
import random
import json
import os

def set_seed(seed:int) -> None:
    """Set random seed (reproducibility)"""
    np.random.seed(seed)
    random.seed(seed)

def load_parameters_json(filename: str) -> dict:
    """Open the path to a json file and return it's content"""
    path_file = os.path.dirname(__file__) + "/"+ filename

    # check if file exists
    if not os.path.exists(path_file):
        raise FileNotFoundError(f"The path '{path_file}' is missing. Must be in same folder as main")
    
    with open(path_file, "r") as read_file:
        return json.load(read_file)

def expected_time_model(route : int, memory_routeA: list, memory_routeB :list) -> float:
    """Calculate the expected travel time for a given route."""
    if not route in [0,1]:
        raise ValueError("We only have route 0 and route 1 as an option in expected_time_model()")
    # Calculate for route A
    if route==0:
        if len(memory_routeA)==0:
            return -1
        else:
            weights = np.asarray([1/(i+1) for i in range(0, len(memory_routeA))])
            weights = np.flip(weights) # most recent / higher index is weighted stronger
            weights = weights/np.sum(weights)
            if len(weights)>1:
                return np.average(a=memory_routeA, weights=weights)
            else:
                return memory_routeA[0]
    # Calculate for route B
    else:
        if len(memory_routeB)==0:
            return -1
        else:
            weights = np.asarray([1/(i+1) for i in range(0, len(memory_routeB))])
            weights = np.flip(weights) # most recent / higher index is weighted stronger
            weights = weights/np.sum(weights)
            if len(weights)>1:
                return np.average(a=memory_routeB, weights=weights)
            else:
                return memory_routeB[0]

def expected_time_model2(route : int, memory_routeA: list, memory_routeB :list, history_routeA: list, history_routeB: list) -> float:
    """Calculate the expected travel time for a given route."""
    if not route in [0,1]:
        raise ValueError("We only have route 0 and route 1 as an option in expected_time_model()")
    # Calculate for route A
    if route==0:
        if len(memory_routeA)==0 or len(history_routeA)==0:
            return -1
        else:
            values = [*memory_routeA, *history_routeA]
            return np.average(values)
            
            # weights = np.asarray([1/(i+1) for i in range(0, len(memory_routeA))])
            # weights = np.flip(weights) # most recent / higher index is weighted stronger
            # weights = weights/np.sum(weights)
            # if len(weights)>1:
            #     return np.average(a=memory_routeA, weights=weights)
            # else:
            #     return memory_routeA[0]
    # Calculate for route B
    else:
        if len(memory_routeB)==0 or len(history_routeB)==0:
            return -1
        else:
            values = [*memory_routeB, *history_routeB]
            return np.average(values)
            
            # weights = np.asarray([1/(i+1) for i in range(0, len(memory_routeB))])
            # weights = np.flip(weights) # most recent / higher index is weighted stronger
            # weights = weights/np.sum(weights)
            # if len(weights)>1:
            #     return np.average(a=memory_routeB, weights=weights)
            # else:
            #     return memory_routeB[0]

            
def makeDecision(exploration_rate: int, urgency: int, salary: int, memory_routeA: list, memory_routeB: list, history_reportedA : list, history_reportedB :list) -> int:
    """ Return which route to take (0 or 1) based on multiple parameters"""

    # Check inputs for validity
    if urgency < 1 or urgency > 10:
        raise ValueError("Urgency must be between 1 and 10 in makeDecision()")
    if salary < 0:
        raise ValueError("Salary can't be negative in makeDecision()")
    if exploration_rate < 0:
        raise ValueError("Exploration rate can't be negative in makeDecision()")

    # Calculate the time it will probably take to go on route A/0 or B/1
    # expected_time_A = expected_time_model(0, memory_routeA, memory_routeB)
    # expected_time_B = expected_time_model(1, memory_routeA, memory_routeB)
    # expected_time_A = expected_time_model(0, history_reportedA, history_reportedB)
    # expected_time_B = expected_time_model(1, history_reportedA, history_reportedB)
    expected_time_A = expected_time_model2(0, memory_routeA, memory_routeB, history_reportedA, history_reportedB)
    expected_time_B = expected_time_model2(1, memory_routeA, memory_routeB, history_reportedA, history_reportedB)

    # If no experiences yet, random decisions
    if expected_time_A==-1 or expected_time_B==-1:
        return np.random.randint(2)

    # Calculate the expected costs for each route
    expected_cost_A = expected_cost_model(route=0, expected_time=expected_time_A, personal_salary=salary, personal_urgency=urgency)
    expected_cost_B = expected_cost_model(route=1, expected_time=expected_time_B, personal_salary=salary, personal_urgency=urgency)
    
    # Decides which route to take based on cost. Might still take the other route, based on random exploration
    should_explore = np.random.random() < exploration_rate
    if expected_cost_A < expected_cost_B:
        if should_explore:
            return 1
        else:
            return 0
    elif expected_cost_A > expected_cost_B:
        if should_explore:
            return 0
        else:
            return 1
    else:
        # If both costs are the same, choose one route randomly between 0 and 1
        return np.random.randint(2)


def run_simulation(simulation_time: int, pop_size: int, urgency_scenario: int, history_length_personal: int, history_length_reported: int, exploration_rate: float, system_optimum: int, nash_equilibrium: int) -> None:
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
    
    plot_results(df_records, system_optimum, nash_equilibrium)


if __name__ == "__main__":
    # Parameters from a json file
    config = load_parameters_json("config.json")

    run_simulation(simulation_time=config["simulation_time"], pop_size=config['pop_size'], urgency_scenario=config['urgency_scenario'], history_length_personal=config['history_length_personal'], history_length_reported=config['history_length_reported'], exploration_rate=config['exploration_rate'], system_optimum=config['system_optimum'], nash_equilibrium=config['nash_equilibrium'])