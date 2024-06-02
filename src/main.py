import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from population import initializePopulation, updateUrgencyAndVOT
from models import travel_time_model_random, expected_cost_model
from datetime import datetime
import os
import random

# Set random seed (reproducibility)
seed = 42
np.random.seed(seed)
random.seed(seed)

# Parameters
simulation_time = 100
pop_size = 10000
urgency_scenario = 0
history_length_personal = 5
history_length_reported = 5
exploration_rate = 0.05

system_optimum = 3983 
nash_equilibrum = 6169


def expected_time_model(route, memory_routeA, memory_routeB):
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


def makeDecision(urgency, salary, memory_routeA, memory_routeB, history_reportedA, history_reportedB):
    """ Return which route to take (0 or 1) based on multiple parameters

    Function arguments:
    urgency : Integer value between 1 (low urgency) and 10 (high urgency) representing urgency of a person
    salary : Integer value representing salary of a person
    memory_routeA : List containing the memory of a person for route A (lower indices are older)
    memory_routeA : List containing the memory of a person for route B (lower indices are older)
    history_reportedA : List containing additonal information for route A (lower indices are older)
    history_reportedB : List containing additonal information for route B (lower indices are older)
    """

    # Check inputs for validity
    if urgency < 1 or urgency > 10:
        raise ValueError("Urgency must be between 1 and 10")
    if salary < 0:
        raise ValueError("Salary can't be negative")

    # Calculate the time it will probably take to go on route A/0 or B/1
    expected_time_A = expected_time_model(0, memory_routeA, memory_routeB)
    expected_time_B = expected_time_model(1, memory_routeA, memory_routeB)

    if expected_time_A==-1 or expected_time_B==-1:
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




# Initialize Population
population = initializePopulation(pop_size, urgency_scenario)

# Initialize Population Memory
memory_route_A = [[] for i in range(0, len(population))]
memory_route_B = [[] for i in range(0, len(population))]
history_reported_A = []
history_reported_B = []

# Init Recording
df_records = pd.DataFrame([], columns=["time", "flow_A", "flow_B", "stat_tt_A", "stat_tt_B"])

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
    stat_tt_A = np.mean(travel_times[decisions==0])
    stat_tt_B = np.mean(travel_times[decisions==1])
    
    # update histories
        # update reported history
    history_reported_A.append(stat_tt_A)
    history_reported_B.append(stat_tt_B)
    if len(history_reported_A) > history_length_reported:
        history_reported_A.pop(0)
    if len(history_reported_B) > history_length_reported:
        history_reported_B.pop(0)
        # update memory history
    for idx in range(0, len(decisions)):
        decision = decisions[idx]
        if decision==0:
            memory_route_A[idx].append(travel_times[idx])
            if len(memory_route_A[idx]) > history_length_personal:
                memory_route_A[idx].pop(0)
        else:
            memory_route_B[idx].append(travel_times[idx])
            if len(memory_route_B[idx]) > history_length_personal:
                memory_route_B[idx].pop(0)
        
    # recording
    df_records.loc[len(df_records.index)] = [time, flow_A, flow_B, stat_tt_A, stat_tt_B] 
        
    # update urgencies randomly
    population = updateUrgencyAndVOT(population, urgency_scenario)
    
    print(time, "/", simulation_time)
    
# Plot Results
plt.figure(figsize=(12,8))

plt.subplot(1,2,1)
plt.title("Split")
plt.plot(df_records["time"], df_records["flow_A"], label="Split (Flow on Route A)")
plt.xlabel("# Times")
plt.ylabel("Split (Route A, # veh)")
plt.plot([0, df_records["time"].iloc[-1]], [system_optimum, system_optimum], "--", label="System Optimum")
plt.plot([0, df_records["time"].iloc[-1]], [nash_equilibrum, nash_equilibrum], "--", label="Nash Equilibrium")
plt.grid()
plt.legend()

plt.subplot(1,2,2)
plt.title("Travel Times per Route")
plt.plot(df_records["time"], df_records["stat_tt_A"], label="Lincoln Tunnel (Route A)")
plt.plot(df_records["time"], df_records["stat_tt_B"], label="George Washington Bridge (Route B)")
plt.xlabel("# Times")
plt.ylabel("Travel Time [minutes]")
plt.grid()
plt.legend()

# Print the plot into a folder, with a unique name (containing date and time)
if not os.path.exists("plots"):
    os.makedirs("plots")
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'simulation_results_{current_time}.png'
plt.savefig("plots/"+filename)
