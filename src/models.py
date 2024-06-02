import numpy as np


def time_cost_model(expected_time:float, personal_salary:int, personal_urgency:int)->float:
    """Calculates cost for the time that a person has to invest to take the route"""
    # check for faulty inputs
    if personal_urgency < 1 or personal_urgency > 10:
        raise ValueError("Urgency must be between 1 and 10 in time_cost_model()")
    if expected_time < 0:
        raise ValueError("expected_time can't be negative in time_cost_model()")
    if personal_salary < 0:
        raise ValueError("personal_salary can't be negative in time_cost_model()")
    
    # calculate
    return personal_urgency * personal_salary * expected_time

def distance_cost_model(route:int) -> float:
    """Calculates the cost (in dollars) to drive a route (fuel cost)"""
    #Check for faulty inputs
    if not route in [0,1]:
        raise ValueError("We only have route 0 and route 1 as an option in distance_cost_model()")
    
    # Calculate costs
    fuel_consumption_per_hundert_km = 6.5 # liter/100km # = 36mpg miles per gallon # https://edition.cnn.com/2022/04/01/energy/fuel-economy-rules/index.html
    fuel_price = 0.96 # $ / liter # https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://tradingeconomics.com/united-states/gasoline-prices&ved=2ahUKEwiz1pSYtYKGAxW93wIHHVEvDiAQFnoECBwQAQ&usg=AOvVaw1-g4NBldoNZD3kxvR5GifM

    if route==0:
        distance_lincoln = 26.55 # km
        km_cost_lincoln = fuel_consumption_per_hundert_km * (distance_lincoln/100) * fuel_price
        return km_cost_lincoln
    
    else:
        distance_george = 49.89 # km
        km_cost_george = fuel_consumption_per_hundert_km * (distance_george/100) * fuel_price
        return km_cost_george

def expected_cost_model(route:int, expected_time:float, personal_salary:int, personal_urgency:int)->float:
    """Returns the total cost of the model"""
    # check for faulty inputs
    if personal_urgency < 1 or personal_urgency > 10:
        raise ValueError("Urgency must be between 1 and 10 in expected_cost_model()")
    if expected_time < 0:
        raise ValueError("expected_time can't be negative in expected_cost_model()")
    if personal_salary < 0:
        raise ValueError("personal_salary can't be negative in expected_cost_model()")
    if not route in [0,1]:
        raise ValueError("We only have route 0 and route 1 as an option in expected_cost_model()")
    
    # Calculations
    return time_cost_model(expected_time, personal_salary, personal_urgency) + distance_cost_model(route)

def travel_time_model_random(route, flow_A, flow_B):
    """Returns travel time given a route and flow on routes based on sampling from a random distribution."""
    if route==0:   # Lincoln     
        mean_tt = 30 + np.power((flow_A * 0.0004), 3)
        std_tt = (30 + np.power((flow_A * 0.0004), 3))/20
    else: # George Washington
        mean_tt = 45 + np.power((flow_B*0.00012), 5)
        std_tt = (45 + np.power((flow_B*0.00012), 5))/20
    random_time = np.random.normal(mean_tt, std_tt)
    return random_time

def expected_time_model(route : int, memory_routeA: list, memory_routeB :list) -> float:
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

def expected_time_model2(route : int, memory_routeA: list, memory_routeB :list, history_routeA: list, history_routeB: list) -> float:
    """Calculate the expected travel time for a given route."""
    if not route in [0,1]:
        raise ValueError("We only have route 0 and route 1 as an option in expected_time_model()")
    # Calculate for route A
    if route==0:
        if len(memory_routeA)==0 or len(history_routeA)==0:
            return -1
        else:
            values = [*memory_routeA, *history_routeA]
            return np.average(values)
            
            # weights = np.asarray([1/(i+1) for i in range(0, len(memory_routeA))])
            # weights = np.flip(weights) # most recent / higher index is weighted stronger
            # weights = weights/np.sum(weights)
            # if len(weights)>1:
            #     return np.average(a=memory_routeA, weights=weights)
            # else:
            #     return memory_routeA[0]
    # Calculate for route B
    else:
        if len(memory_routeB)==0 or len(history_routeB)==0:
            return -1
        else:
            values = [*memory_routeB, *history_routeB]
            return np.average(values)
            
            # weights = np.asarray([1/(i+1) for i in range(0, len(memory_routeB))])
            # weights = np.flip(weights) # most recent / higher index is weighted stronger
            # weights = weights/np.sum(weights)
            # if len(weights)>1:
            #     return np.average(a=memory_routeB, weights=weights)
            # else:
            #     return memory_routeB[0]

def makeDecision(exploration_rate: int, urgency: int, salary: int, memory_routeA: list, memory_routeB: list, history_reportedA : list, history_reportedB :list) -> int:
    """ Return which route to take (0 or 1) based on multiple parameters"""

    # Check inputs for validity
    if urgency < 1 or urgency > 10:
        raise ValueError("Urgency must be between 1 and 10 in makeDecision()")
    if salary < 0:
        raise ValueError("Salary can't be negative in makeDecision()")
    if exploration_rate < 0:
        raise ValueError("Exploration rate can't be negative in makeDecision()")

    # Calculate the time it will probably take to go on route A/0 or B/1
    # expected_time_A = expected_time_model(0, memory_routeA, memory_routeB)
    # expected_time_B = expected_time_model(1, memory_routeA, memory_routeB)
    # expected_time_A = expected_time_model(0, history_reportedA, history_reportedB)
    # expected_time_B = expected_time_model(1, history_reportedA, history_reportedB)
    expected_time_A = expected_time_model2(0, memory_routeA, memory_routeB, history_reportedA, history_reportedB)
    expected_time_B = expected_time_model2(1, memory_routeA, memory_routeB, history_reportedA, history_reportedB)

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