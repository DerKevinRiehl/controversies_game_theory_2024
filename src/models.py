import numpy as np




def time_cost_model(exp_time, pers_salary, pers_urgency):
    return pers_urgency*pers_salary*exp_time

def distance_cost_model(route):
    distance_lincoln = 26.55 # km
    distance_george = 49.89 # km
    kraftstoff_verbrauch = 6.5 # liter/100km # = 36mpg miles per gallon # https://edition.cnn.com/2022/04/01/energy/fuel-economy-rules/index.html
    kraftstoff_preis = 0.96 # $ / liter # https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://tradingeconomics.com/united-states/gasoline-prices&ved=2ahUKEwiz1pSYtYKGAxW93wIHHVEvDiAQFnoECBwQAQ&usg=AOvVaw1-g4NBldoNZD3kxvR5GifM
    km_cost_lincoln = kraftstoff_verbrauch * (distance_lincoln/100) * kraftstoff_preis
    km_cost_george = kraftstoff_verbrauch * (distance_george/100) * kraftstoff_preis
    if route==0:
        return km_cost_lincoln
    else:
        return km_cost_george

def expected_cost_model(route, exp_time, pers_salary, pers_urgency):
    return time_cost_model(exp_time, pers_salary, pers_urgency) + distance_cost_model(route)

def travel_time_model_random(route, flow_A, flow_B):
    if route==0:   # Lincoln     
        mean_tt = 30 + np.power((flow_A * 0.0004), 3)
        std_tt = (30 + np.power((flow_A * 0.0004), 3))/20
    else: # George Washington
        mean_tt = 45 + np.power((flow_B*0.00012), 5)
        std_tt = (45 + np.power((flow_B*0.00012), 5))/20
    random_time = np.random.normal(mean_tt, std_tt)
    return random_time