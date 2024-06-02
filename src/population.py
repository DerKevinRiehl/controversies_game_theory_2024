import numpy as np
import pandas as pd

# ****** POPULATION Salary Data & Urgency Process Geometric
share_population = [ # 3.24, # 1.62, # 3.45, # 3.6, # 3.84, # 3.6, # 4.02, 
                    3.56, 3.62, 3.39, 3.68, 3.24, 3.4, 2.94, 2.97, 2.79, 2.67, 2.33, 2.38, 2.16, 2.52, 1.77, 1.87, 1.67, 1.84, 1.59, 1.52, 1.32, 1.28, 1.05, 1.53, 1.06, 1.11, 0.86, 0.87, 0.79, 0.84, 0.7, 0.72, 0.68, 4.58, 7.33 ] 
hour_salary = [ # 0.463530655, # 4.030655391, # 6.575052854, # 9.170190275, # 11.76004228, # 14.38160677, # 16.91331924, 
               19.59830867, 22.17758985, 24.91014799, 27.42071882, 30.14270613, 32.70613108, 35.46511628, 38.04968288, 40.68181818, 43.31395349, 46.03065539, 48.58879493, 51.34249471, 53.80549683, 56.60676533, 59.19661734, 61.89217759, 64.37632135, 67.17758985, 69.76744186, 72.41014799, 75, 77.8012685, 80.28541226, 82.98097252, 85.62367865, 88.3192389, 90.96194503, 93.60465116, 96.24735729, 98.89006342, 101.5327696, 104.2283298, 116.8604651, 225.4756871 ] 
salary_intervals = [ 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, ]

def getUrgencyProcess(p:float):
    """Function that takes a probability and returns urgency_level list and it's distribution via urgency_dist"""
    urgency_level = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    urgency_dist = [p*np.power(1-p, k-1) for k in urgency_level]
    urgency_dist = urgency_dist/sum(urgency_dist)
    return urgency_dist, urgency_level

def getRandomUrgencysForPopulation(urgency_scenario, pop_size):
    urgency_scenarios = [0.6, 0.5, 0.4]
    urgency_dist, urgency_level = getUrgencyProcess(p=urgency_scenarios[urgency_scenario])
    return np.random.choice(urgency_level, pop_size, p=urgency_dist)

def initializePopulation(pop_size:int, urgency_scenario):
    salaries = np.random.choice(hour_salary, pop_size , p=np.asarray(share_population)/sum(share_population))
    population = pd.DataFrame(salaries, columns=["salary"])
    population = updateUrgencyAndVOT(population, urgency_scenario)
    return population

def updateUrgencyAndVOT(population:int, urgency_scenario):
    population["urgency"] = getRandomUrgencysForPopulation(urgency_scenario, pop_size=len(population))
    population["VOT"] = population["urgency"] * population["salary"]
    return population

