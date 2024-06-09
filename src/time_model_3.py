import numpy as np
from helpers import compute_exponential_weights

def expected_time_model3(route: int, memory_routeA: list, memory_routeB: list, history_routeA: list, history_routeB: list, history_weight_personal: float, history_weight_reported: float) -> float:
    """Calculate the expected travel time for a given route by weighting history and memory based on an exponential function."""
    if not route in [0,1]:
        raise ValueError("We only have route 0 and route 1 as an option in expected_time_model()")
    if(history_weight_personal == 0 and history_weight_reported== 0):
        return -1
    # Calculate for route A or B
    if route==0:
        memory_route = memory_routeA
        history_route = history_routeA
    else:
        memory_route = memory_routeB
        history_route = history_routeB

    if len(memory_route)==0 or len(history_route)==0:
        return -1
    elif len(memory_route)==1 or len(history_route)==1:
        return (memory_route[0] * history_weight_personal + history_route[0] * history_weight_reported)/(history_weight_personal + history_weight_reported)
    else:
        weights_memory = compute_exponential_weights(memory_route)
        weights_history = compute_exponential_weights(history_route)

        exponent_weighted_average_memory = np.average(a=memory_route, weights=weights_memory)
        exponent_weighted_average_history = np.average(a=history_route, weights=weights_history)
        
        return (exponent_weighted_average_memory*history_weight_personal+exponent_weighted_average_history*history_weight_reported)/(history_weight_personal+history_weight_reported)