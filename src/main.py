import numpy as np
import pandas as pd
from population import initializePopulation, updateUrgencyAndVOT
from models import travel_time_model_random, expected_cost_model
from plotting import plot_results
import random

def set_seed(seed:int) -> None:
    """Set random seed (reproducibility)"""
    np.random.seed(seed)
    random.seed(seed)


def expected_time_model(route : int, memory_routeA: list, memory_routeB :list) -> float:
    """Calculate the expected travel time for a given route."""
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


def makeDecision(urgency: int, salary: int, memory_routeA: list, memory_routeB: list, history_reportedA : list, history_reportedB :list) -> int:
    """ Return which route to take (0 or 1) based on multiple parameters"""

    # Check inputs for validity
    if urgency < 1 or urgency > 10:
        raise ValueError("Urgency must be between 1 and 10")
    if salary < 0:
        raise ValueError("Salary can't be negative")

    # Calculate the time it will probably take to go on route A/0 or B/1
    expected_time_A = expected_time_model(0, memory_routeA, memory_routeB)
    expected_time_B = expected_time_model(1, memory_routeA, memory_routeB)

    if expected_time_A==-1 or expected_time_B==-1:  #What happens here??? - czeiter
        return np.random.randint(2)
    
    
    # Calculate the expected costs for each route
    expected_cost_A = expected_cost_model(route=0, exp_time=expected_time_A, pers_salary=salary, pers_urgency=urgency)
    expected_cost_B = expected_cost_model(route=1, exp_time=expected_time_B, pers_salary=salary, pers_urgency=urgency)
    
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



# Parameters
simulation_time = 100
pop_size = 10000
urgency_scenario = 0
history_length_personal = 5
history_length_reported = 5
exploration_rate = 0.05

system_optimum = 3983 
nash_equilibrium = 6169

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
    
    print(time, "/", simulation_time)
    
plot_results(df_records, system_optimum, nash_equilibrium)
