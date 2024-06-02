import numpy as np
def expected_time_model1(route : int, memory_routeA: list, memory_routeB :list) -> float:
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