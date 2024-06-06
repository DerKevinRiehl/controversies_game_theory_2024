import numpy as np
def expected_time_model2(route : int, memory_routeA: list, memory_routeB :list, history_routeA: list, history_routeB: list, history_weight_personal:float, history_weight_reported:float) -> float:
    """Calculate the expected travel time for a given route. Normal average, not weighted."""
    if not route in [0,1]:
        raise ValueError("We only have route 0 and route 1 as an option in expected_time_model()")
    if(history_weight_personal == 0 and history_weight_reported== 0):
        return -1
    # Calculate for route A
    if route==0:
        if len(memory_routeA)==0:
            return -1
        else:
            if len(memory_routeA)>1 and len(history_routeA)>1:
                average_memory = np.average(a=memory_routeA)
                average_history = np.average(a=history_routeA)
                return (average_memory*history_weight_personal+average_history*history_weight_reported)/(history_weight_personal+history_weight_reported)
            else:
                return memory_routeA[0]
    # Calculate for route B
    else:
        if len(memory_routeB)==0:
            return -1
        else:
            if len(memory_routeB)>1 and len(history_routeB)>1:
                average_memory = np.average(a=memory_routeB)
                average_history = np.average(a=history_routeB)
                return (average_memory*history_weight_personal+average_history*history_weight_reported)/(history_weight_personal+history_weight_reported)
            else:
                return memory_routeB[0]