import numpy as np
import math
from collections import deque

def expected_time_model3(route : int, memory_routeA: deque, memory_routeB :deque, history_routeA: deque, history_routeB: deque, history_weight_personal:float, history_weight_reported:float) -> float:
    """Calculate the expected travel time for a given route by weighting history and memory based on an exponential function."""
    if not route in [0,1]:
        raise ValueError("We only have route 0 and route 1 as an option in expected_time_model()")
    # Calculate for route A
    if route==0:
        len_memory_a = len(memory_routeA)
        if len_memory_a==0 or len(history_routeA)==0:
            return -1
        else:
            
            weights_memory = np.asarray([math.exp(i) for i in range(0, len_memory_a)])
            weights_memory /= np.sum(weights_memory)

            len_history_a = len(history_routeA)
            weights_history = np.asarray([math.exp(i) for i in range(0, len_history_a)])
            weights_history /= np.sum(weights_history)

            if len(weights_memory)>1 and len(weights_history)>1:
                exponent_weighted_average_memory = np.average(a=memory_routeA, weights=weights_memory)
                exponent_weighted_average_history = np.average(a=history_routeA, weights=weights_history)
                return (exponent_weighted_average_memory*history_weight_personal+exponent_weighted_average_history*history_weight_reported)/(history_weight_personal+history_weight_reported)
            else:
                 return memory_routeA[0]
    # Calculate for route B
    else:
        len_memory_b = len(memory_routeB)
        if len_memory_b==0 or len(history_routeB)==0:
            return -1
        else:
            
            weights_memory = np.asarray([math.exp(i) for i in range(0, len_memory_b)])
            weights_memory /= np.sum(weights_memory)

            len_history_b = len(history_routeB)
            weights_history = np.asarray([math.exp(i) for i in range(0, len_history_b)])
            weights_history /= np.sum(weights_history)

            if len(weights_memory)>1 and len(weights_history)>1:
                exponent_weighted_average_memory = np.average(a=memory_routeB, weights=weights_memory)
                exponent_weighted_average_history = np.average(a=history_routeB, weights=weights_history)
                return (exponent_weighted_average_memory*history_weight_personal+exponent_weighted_average_history*history_weight_reported)/(history_weight_personal+history_weight_reported)
            else:
                 return memory_routeB[0]