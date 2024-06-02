import numpy as np

def expected_time_model4(route : int, memory_routeA: list, memory_routeB :list, history_routeA: list, history_routeB: list, history_weight_personal:float, history_weight_reported:float) -> float:
    """Calculate the expected travel time for a given route. Looks at maximum time."""
    if not route in [0,1]:
        raise ValueError("We only have route 0 and route 1 as an option in expected_time_model()")
    # Calculate for route A
    if route==0:
        if len(memory_routeA)==0 or len(history_routeA)==0:
            return -1
        else:
            if len(memory_routeA)>1 and len(history_routeA)>1:
                return (np.max(memory_routeA)*history_weight_personal+np.max(history_routeA)*history_weight_reported)/(history_weight_personal+history_weight_reported)
            else:
                 return memory_routeA[0]
    # Calculate for route B
    else:
        if len(memory_routeB)==0 or len(history_routeB)==0:
            return -1
        else:

            if len(memory_routeB)>1 and len(history_routeB)>1:
                return (np.max(memory_routeB)*history_weight_personal+np.max(history_routeB)*history_weight_reported)/(history_weight_personal+history_weight_reported)
            else:
                 return memory_routeB[0]