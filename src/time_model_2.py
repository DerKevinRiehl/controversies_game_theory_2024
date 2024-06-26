import numpy as np


def expected_time_model2(route: int, memory_routeA: list, memory_routeB: list, history_routeA: list, history_routeB: list, history_weight_personal: float, history_weight_reported: float) -> float:
    """Calculate the expected travel time for a given route. Normal average, not weighted."""

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
        average_memory = np.average(a=memory_route)
        average_history = np.average(a=history_route)
        
        return (average_memory*history_weight_personal + average_history*history_weight_reported)/(history_weight_personal + history_weight_reported)