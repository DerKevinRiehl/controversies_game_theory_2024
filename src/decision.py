import numpy as np
from time_model_1 import expected_time_model1
from time_model_2 import expected_time_model2
from time_model_3 import expected_time_model3
from time_model_4 import expected_time_model4
from models import expected_cost_model

def makeDecision(exploration_rate: int, urgency: int, salary: int, memory_routeA: list, memory_routeB: list, history_reportedA: list, history_reportedB: list, simulation_type: int, history_weight_personal: float, history_weight_reported: float) -> int:
    """ Return which route to take (0 or 1) based on multiple parameters"""

    # Check inputs for validity
    if urgency < 1 or urgency > 10:
        raise ValueError("Urgency must be between 1 and 10 in makeDecision()")
    if salary < 0:
        raise ValueError("Salary can't be negative in makeDecision()")
    if exploration_rate < 0:
        raise ValueError("Exploration rate can't be negative in makeDecision()")
    if history_weight_personal <0 or history_weight_reported<0:
        raise ValueError("Weights must be postive in makeDecision()")

    # All available simulation models
    simulation_models = [expected_time_model1, expected_time_model2, expected_time_model3, expected_time_model4]

    # Choose simulation model
    current_model = simulation_models[simulation_type-1]

    # Apply chosen current model
    expected_time_A = current_model(0, memory_routeA, memory_routeB, history_reportedA, history_reportedB, history_weight_personal, history_weight_reported)
    expected_time_B = current_model(1, memory_routeA, memory_routeB, history_reportedA, history_reportedB, history_weight_personal, history_weight_reported)
    
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