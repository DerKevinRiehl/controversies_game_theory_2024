import numpy as np


def time_cost_model(expected_time:float, personal_salary:int, personal_urgency:int)->float:
    """Calculates cost for the time that a person has to invest to take the route"""
    return personal_urgency * personal_salary * expected_time

def distance_cost_model(route:int) -> float:
    """Calculates the cost (in dollars) to drive a route (fuel cost)"""
    
    # Calculate costs
    fuel_consumption_per_hundred_km = 6.5 # liter/100km # = 36mpg miles per gallon # https://edition.cnn.com/2022/04/01/energy/fuel-economy-rules/index.html
    fuel_price = 0.96 # $ / liter # https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://tradingeconomics.com/united-states/gasoline-prices&ved=2ahUKEwiz1pSYtYKGAxW93wIHHVEvDiAQFnoECBwQAQ&usg=AOvVaw1-g4NBldoNZD3kxvR5GifM
    fuel_price_per_km = 0.01 * fuel_consumption_per_hundred_km

    if route==0:
        distance_lincoln = 26.55 # km
        return fuel_price_per_km * distance_lincoln
    
    else:
        distance_george = 49.89 # km
        return fuel_price_per_km * distance_george

def expected_cost_model(route:int, expected_time:float, personal_salary:int, personal_urgency:int)->float:
    """Returns the total cost of the model"""
    # check for faulty inputs
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