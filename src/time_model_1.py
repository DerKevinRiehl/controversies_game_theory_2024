import numpy as np
from helpers import compute_geometric_weights

def expected_time_model1(route: int, memory_routeA: list, memory_routeB: list, history_routeA: list, history_routeB: list, history_weight_personal: float, history_weight_reported: float) -> float:
    """Calculate the expected travel time for a given route. Geometrically weighted."""

    if not route in [0,1]:
        raise ValueError("We only have route 0 and route 1 as an option in expected_time_model()")
    if(history_weight_personal == 0 and history_weight_reported == 0):
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
        weights_memory = compute_geometric_weights(memory_route)
        weights_history = compute_geometric_weights(history_route)

        weighted_avg_mem = np.average(a=memory_route, weights=weights_memory)
        weighted_avg_hist = np.average(a=history_route, weights=weights_history)
        
        return (weighted_avg_mem*history_weight_personal + weighted_avg_hist*history_weight_reported)/(history_weight_personal+history_weight_reported)
