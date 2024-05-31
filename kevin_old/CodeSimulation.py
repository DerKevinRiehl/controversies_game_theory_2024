
# *****************************************************************************
# ****** IMPORTS
# *****************************************************************************
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
from matplotlib import cm
from matplotlib import ticker
import random




# *****************************************************************************
# ****** SIMULATION PARAMETERS
# *****************************************************************************
# ****** MAP
distance_lincoln = 26.55 # km
distance_george = 49.89 # km

# ****** DEMAND MODEL
total_flow = 10000

# ****** TRAVEL TIME MODEL
total_flow_TT_sim = 15000
flows = []
flows_real = []
tt_lincoln = []
tt_george = []
tt_lincoln_std = []
tt_george_std = []
for f in range(0, total_flow_TT_sim):
    flows.append(f)
    if f<total_flow:
        flows_real.append(f)
    tt_lincoln.append(
        30 + np.power((f * 0.0004), 3)
    )
    tt_lincoln_std.append(
        (30 + np.power((f * 0.0004), 3))/20*(1+np.random.random()*2)
    )
    tt_george.append( 
        45 + np.power((f*0.00012), 5)
    )
    tt_george_std.append(
        (45 + np.power((f*0.00012), 5))/20*(1+np.random.random()*2)
    )
def calculateTTT(delsA, delsB, total_flow):
    vals_TTT = []
    for flowA in range(0, total_flow):
        flowB = total_flow -1 - flowA
        mdDelayA = delsA[flowA]
        mdDelayB = delsB[flowB]
        vals_TTT.append(mdDelayA*flowA + mdDelayB*flowB)
    return np.asarray(vals_TTT)/60
valTTT = calculateTTT(tt_lincoln, tt_george, total_flow)

# ****** FUEL CONSUMPTION
kraftstoff_verbrauch = 6.5 # liter/100km # = 36mpg miles per gallon # https://edition.cnn.com/2022/04/01/energy/fuel-economy-rules/index.html
kraftstoff_preis = 0.96 # $ / liter # https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://tradingeconomics.com/united-states/gasoline-prices&ved=2ahUKEwiz1pSYtYKGAxW93wIHHVEvDiAQFnoECBwQAQ&usg=AOvVaw1-g4NBldoNZD3kxvR5GifM
km_cost_lincoln = kraftstoff_verbrauch * (distance_lincoln/100) * kraftstoff_preis
km_cost_george = kraftstoff_verbrauch * (distance_george/100) * kraftstoff_preis

# ****** PRICE
lincoln_price = 18.41 # 13.97 [p0.09-scen3] # 25.53 [p0.04-scen2] # 22.02 [p0.05-scen1] # 18.41 [p0.06-scen0] 

# ****** POPULATION Salary Data & Urgency Process Geometric
share_population = [ # 3.24, # 1.62, # 3.45, # 3.6, # 3.84, # 3.6, # 4.02, 
                    3.56, 3.62, 3.39, 3.68, 3.24, 3.4, 2.94, 2.97, 2.79, 2.67, 2.33, 2.38, 2.16, 2.52, 1.77, 1.87, 1.67, 1.84, 1.59, 1.52, 1.32, 1.28, 1.05, 1.53, 1.06, 1.11, 0.86, 0.87, 0.79, 0.84, 0.7, 0.72, 0.68, 4.58, 7.33 ] 
hour_salary = [ # 0.463530655, # 4.030655391, # 6.575052854, # 9.170190275, # 11.76004228, # 14.38160677, # 16.91331924, 
               19.59830867, 22.17758985, 24.91014799, 27.42071882, 30.14270613, 32.70613108, 35.46511628, 38.04968288, 40.68181818, 43.31395349, 46.03065539, 48.58879493, 51.34249471, 53.80549683, 56.60676533, 59.19661734, 61.89217759, 64.37632135, 67.17758985, 69.76744186, 72.41014799, 75, 77.8012685, 80.28541226, 82.98097252, 85.62367865, 88.3192389, 90.96194503, 93.60465116, 96.24735729, 98.89006342, 101.5327696, 104.2283298, 116.8604651, 225.4756871 ] 
salary_intervals = [ 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, ]
def getSalaryClass(salary):
    if salary < salary_intervals[0]:
        return 0
    elif salary > salary_intervals[-1]:
        return len(salary_intervals)
    else:
        last_passed = 0
        for val in salary_intervals:
            if salary >= val:
                last_passed += 1 
            else:
                break
    return last_passed
def getUrgencyProcess(p):
    urgency_dist = []
    urgency_level = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    urgency_dist = [p*np.power(1-p, k-1) for k in urgency_level]
    urgency_dist = urgency_dist/sum(urgency_dist)
    return urgency_dist, urgency_level
urgency_scenarios = [0.6, 0.5, 0.4, 0.9]




# *****************************************************************************
# ****** METHODS
# *****************************************************************************
def initPopulation(scenario, pop_size):
    population = {}
        # Calculate Salary
    population["salary"] = np.random.choice(hour_salary, pop_size , p=np.asarray(share_population)/sum(share_population))
    urgency_dist, urgency_level = getUrgencyProcess(p=urgency_scenarios[scenario])
        # Calculate Urgency
    population["urgency"] = np.random.choice(urgency_level, pop_size, p=urgency_dist)
        # Calculate VOT
    population["VOT"] = np.asarray(population["salary"])*np.asarray(population["urgency"])
        # Sort Lists by VOT
    resA = [x for _, x in sorted(zip(population["VOT"], population["salary"]))]
    resB = [x for _, x in sorted(zip(population["VOT"], population["urgency"]))]
    resC = sorted(population["VOT"])
    resA.reverse()
    resB.reverse()
    resC.reverse()
    population["salary"] = resA
    population["urgency"] = resB
    population["VOT"] = resC
        # Calculate Salary Class
    population["salary_class"] = []
    for person in range(0, total_flow):
        population["salary_class"].append(getSalaryClass(salary=population["salary"][person]))
    return population




# *****************************************************************************
# ****** MAIN WORKFLOW
# *****************************************************************************

# ****** INIT POPULATION
population = initPopulation(scenario=0, pop_size=total_flow)


# UNCLEAN CODE FROM HERE ON















# def getUserOptimum_Money(tableRouteA, tableRouteB, total_flow_real, price_routeA):  
#     pop_vot = np.random.choice(vots, total_flow_real, vots_probs) # eur/h
#     pop_vot.sort()
#     pop_vot = np.flip(pop_vot)
#     pop_route = np.ones(len(pop_vot)) # 1 = Route B for free, 0 = Route A for price_routeA
#     decision_changed = True
#     max_iter = 1 
#     iteration = 0
#     while decision_changed and iteration<max_iter:
#         iteration += 1
#         decision_changed = False
#         for decision_maker in range(0, len(pop_vot)):
#             flowA = np.sum(pop_route==0)
#             if flowA%2!=0:
#                 flowA-=1
#             flowB = total_flow_real-flowA
#             timeA = tableRouteA[tableRouteA["RealFlow"]==flowA].iloc[0]["sm_avg"]/60/60 # h
#             timeB = tableRouteB[tableRouteB["RealFlow"]==flowB].iloc[0]["sm_avg"]/60/60 # h
#             pop_cost = []
#             for idx in range(0, len(pop_route)):
#                 if pop_route[idx]==1:
#                     pop_cost.append(timeB*pop_vot[idx])
#                 else:
#                     pop_cost.append(timeA*pop_vot[idx] + price_routeA)
#             current_cost = pop_cost[decision_maker]
#             if pop_route[decision_maker] == 1:
#                 potential_cost = timeA*pop_vot[decision_maker] + price_routeA
#             else:
#                 potential_cost = timeB*pop_vot[decision_maker]
#             if current_cost > potential_cost: # change
#                 if pop_route[decision_maker] == 1:
#                     pop_route[decision_maker] = 0 
#                 else:
#                     pop_route[decision_maker] = 1 
#                 decision_changed = True
#         print("\t", np.sum(pop_route==1), sum(pop_cost))
#     return np.sum(pop_route==1), sum(pop_cost), pop_vot, pop_route










# #############################################################################
# Methods for MAP AND TIME CALCULATION
# #############################################################################
   
# def getUserEquilibrium(delsA, delsB, total_flow):
#     flows_A = []
#     flowA = 0
#     flowB = 0
#     for flow in range(0, total_flow):
#         if delsA[flowA]<delsB[flowB]:
#             flowA+=1
#         else:
#             flowB+=1
#         flows_A.append(flowA)
#     return flowA, flowB, flows_A

def makeDecisionIteration(flow_A, flow_B):
    changes = 0
    print("start makeDecisionItertion ", flow_A, flow_B)
    person_Idxs = []
    for person in range(0, total_flow):
        person_Idxs.append(person)
    random.shuffle(person_Idxs)
    for person in person_Idxs:
        travel_timeA = tt_lincoln[flow_A] + np.random.normal(0, tt_lincoln_std[flow_A])/100
        cost_A = km_cost_lincoln + travel_timeA/60*population["VOT"][person] + lincoln_price
        travel_timeB = tt_george[flow_B] + np.random.normal(0, tt_george_std[flow_B])/100
        cost_B = km_cost_george + travel_timeB/60*population["VOT"][person]
        old_decision = population["decisions"][person]
        if cost_A < cost_B:
            flow_A += 1
            population["decisions"][person] = "Lincoln"            
            population["traveltimes"][person] = travel_timeA
        elif cost_B < cost_A:
            flow_B += 1
            population["decisions"][person] = "George" 
            population["traveltimes"][person] = travel_timeB
        else:
            if np.random.random()<=0.5:
                flow_A += 1
                population["decisions"][person] = "Lincoln" 
                population["traveltimes"][person] = travel_timeA
            else:
                flow_B += 1
                population["decisions"][person] = "George" 
                population["traveltimes"][person] = travel_timeB
        if old_decision!=population["decisions"][person]:
            changes += 1
        if old_decision=="Lincoln":
            flow_A -= 1 
        else:#if old_decision=="George":
            flow_B -= 1
        if flow_A + flow_B != 10000:
            print("RRR", flow_A, flow_B)
            break
    return flow_A, flow_B, changes

def getRouteCostSummary(flow_A, flow_B):
    costs_A = 0
    costs_B = 0
    for person in range(0, total_flow):
        if population["decisions"][person]=="Lincoln":
            costs_A += km_cost_lincoln + population["traveltimes"][person]/60*population["VOT"][person] + lincoln_price
        else:
            costs_B += km_cost_george +population["traveltimes"][person]/60*population["VOT"][person]
    return costs_A, costs_B

def printCostSummaryMarketEquilibriumCalculation(flow_A, flow_B):
    av_vot = np.mean(population["VOT"])
    print("\t",
          km_cost_lincoln+tt_lincoln[flow_A]/60*av_vot+ + lincoln_price, 
          km_cost_george+tt_george[flow_B]/60*av_vot)
    costs_A,costs_B = getRouteCostSummary(flow_A, flow_B)
    # print(costs_A, costs_B)
    if flow_A>0 and flow_B > 0:
        print("\t", costs_A/flow_A, costs_B/flow_B)
    
def initDecisionsRandom(population):
    population["decisions"] = []
    population["traveltimes"] = []
    init_flow = [0, 0]
    for person in range(0, total_flow):
        population["traveltimes"].append(0)
        if np.random.random()<=0.5:
            init_flow[0] += 1
            population["decisions"].append("Lincoln")
        else:
            init_flow[1] += 1
            population["decisions"].append("George")
    return population, init_flow

def initDecisionsAllLincoln(population):
    population["decisions"] = []
    population["traveltimes"] = []
    init_flow = [0, 0]
    for person in range(0, total_flow):
        population["traveltimes"].append(0)
        init_flow[0] += 1
        population["decisions"].append("Lincoln")
    return population, init_flow

def runDecisionMaking(init_flow, max_iter=20):
    print("# Start Iteration 0")
    flow_A, flow_B, change = makeDecisionIteration(init_flow[0], init_flow[1])
    print(flow_A, flow_B)
    printCostSummaryMarketEquilibriumCalculation(flow_A, flow_B)
    print(change)
    print("")
    n_iter = 0
    while change>0 and n_iter<max_iter:
        print("# Start Iteration ", max_iter+1)
        flow_A, flow_B, change = makeDecisionIteration(flow_A, flow_B)
        print(flow_A, flow_B)
        printCostSummaryMarketEquilibriumCalculation(flow_A, flow_B)
        print(change)
        n_iter += 1
        print("")
    return flow_A, flow_B, n_iter






population, init_flow = initDecisionsRandom(population)
# population, init_flow = initDecisionsAllLincoln(population)

flow_A, flow_B, n_iter = runDecisionMaking(init_flow, max_iter=20)


print("\n\n")
print("=======================")
print("Total Statistics for Price (", lincoln_price, ")")
print("=======================")
valTTT = calculateTTT(tt_lincoln, tt_george, total_flow)
print("Total Travel Time (TTT) : ", valTTT[flow_A])
tot_cost = 0
tot_cost_fee = 0
tot_cost_fuel = 0
tot_cost_dist = 0
for idx in range(0, total_flow):
    if population["decisions"][idx]=="Lincoln":
        tot_cost += km_cost_lincoln + population["traveltimes"][idx]/60*population["VOT"][idx] + lincoln_price
        tot_cost_fee += lincoln_price
        tot_cost_fuel += km_cost_lincoln
        tot_cost_dist += population["traveltimes"][idx]/60*population["VOT"][idx]
    else:
        tot_cost += km_cost_george +population["traveltimes"][idx]/60*population["VOT"][idx]
        tot_cost_fuel += km_cost_george
        tot_cost_dist += population["traveltimes"][idx]/60*population["VOT"][idx]
print("Total Costs : \t", tot_cost)
print("  Fees : \t", tot_cost_fee)
print("  Fuel : \t", tot_cost_fuel)
print("  TravelTime : \t", tot_cost_dist)


print("\n\n")
print("=======================")
print("Summary by Route")
print("=======================")
print("TODO: COST SPLIT MAYBE, TIME COST, FEE COST, FUEL COST")
print("TODO: TOTAL STATISTICS: TOTAL TRAVEL TIME, TOTAL COSTS+COST BREAKDOWN")
print("TODO: FUEL MODEL DEPENDING ON TIME https://afdc.energy.gov/data/10312")
print("Travel Times : ")
print("  Lincoln : ", tt_lincoln[flow_A], "mins")
print("  George  : ", tt_george[flow_B],  "mins")

print("Split : ")
print("  Lincoln : ", flow_A, " , ", flow_A/total_flow*100, "%")
print("  George  : ", flow_B, " , ", flow_B/total_flow*100, "%")

print("Average User Cost : ")
av_vot = np.mean(population["VOT"])
print("  Lincoln : ", km_cost_lincoln+tt_lincoln[flow_A]/60*av_vot + lincoln_price, "$")
print("  George  : ", km_cost_george+tt_george[flow_B]/60*av_vot, "$")

print("Actual Cost per User: ")
costs_A, costs_B = getRouteCostSummary(flow_A, flow_B)
print("  Lincoln : ", costs_A/flow_A, "$")
print("  George  : ", costs_B/flow_B, "$")




print("\n\n")
print("=======================")
print("Summary by Urgency")
print("=======================")

class_scheme = [1,2,3,4,5,6,7,8,9,10] # Urgency Levels
pop_idx = {}
for urgency in class_scheme:
    pop_idx_lst = []
    for person in range(0, total_flow):
        if population["urgency"][person]==urgency:
            pop_idx_lst.append(person)
    pop_idx[urgency] = pop_idx_lst
    
print("Travel Times : ")
for c in class_scheme:
    vals = []
    for idx in pop_idx[c]:
        vals.append(population["traveltimes"][idx])
    print("  ", c, " : ", np.nanmean(vals), "mins")
    
print("Split : ")
for c in class_scheme:
    vals = []
    for idx in pop_idx[c]:
        vals.append(population["decisions"][idx])
    print("  ", c, " : ", np.sum([v=="Lincoln" for v in vals])/len(vals), "%")

print("Cost : ")
for c in class_scheme:
    vals = []
    vals_fuel = []
    vals_fees = []
    vals_time = []
    for idx in pop_idx[c]:
        if population["decisions"][idx]=="Lincoln":
            cost = km_cost_lincoln + population["traveltimes"][idx]/60*population["VOT"][idx] + lincoln_price
            vals_fees.append(lincoln_price)
            vals_fuel.append(km_cost_lincoln)
            vals_time.append(population["traveltimes"][idx]/60*population["VOT"][idx])
        else:
            cost = km_cost_george +population["traveltimes"][idx]/60*population["VOT"][idx]
            vals_fees.append(0)
            vals_fuel.append(km_cost_george)
            vals_time.append(population["traveltimes"][idx]/60*population["VOT"][idx])
        vals.append(cost)
    print("  ", c, " : ", np.nanmean(vals), "$", "(Fees: ", np.nanmean(vals_fees), ", Fuel: ", np.nanmean(vals_fuel), "Time: ", np.nanmean(vals_time),")" )

    


print("\n\n")
print("=======================")
print("Summary by Salary")
print("=======================")

class_scheme = [0,1,2,3,4,5,6,7,8,9,10] # Salary Classes
pop_idx = {}
for salary_class in class_scheme:
    pop_idx_lst = []
    for person in range(0, total_flow):
        if population["salary_class"][person]==salary_class:
            pop_idx_lst.append(person)
    pop_idx[salary_class] = pop_idx_lst
    
print("Travel Times : ")
for c in class_scheme:
    vals = []
    for idx in pop_idx[c]:
        vals.append(population["traveltimes"][idx])
    print("  ", c, " : ", np.nanmean(vals), "mins")
    
print("Split : ")
for c in class_scheme:
    vals = []
    for idx in pop_idx[c]:
        vals.append(population["decisions"][idx])
    print("  ", c, " : ", np.sum([v=="Lincoln" for v in vals])/len(vals), "%")

print("Cost : ")
for c in class_scheme:
    vals = []
    vals_fuel = []
    vals_fees = []
    vals_time = []
    for idx in pop_idx[c]:
        if population["decisions"][idx]=="Lincoln":
            cost = km_cost_lincoln + population["traveltimes"][idx]/60*population["VOT"][idx] + lincoln_price
            vals_fees.append(lincoln_price)
            vals_fuel.append(km_cost_lincoln)
            vals_time.append(population["traveltimes"][idx]/60*population["VOT"][idx])
        else:
            cost = km_cost_george +population["traveltimes"][idx]/60*population["VOT"][idx]
            vals_fees.append(0)
            vals_fuel.append(km_cost_george)
            vals_time.append(population["traveltimes"][idx]/60*population["VOT"][idx])
        vals.append(cost)
    print("  ", c, " : ", np.nanmean(vals), "$", "(Fees: ", np.nanmean(vals_fees), ", Fuel: ", np.nanmean(vals_fuel), "Time: ", np.nanmean(vals_time),")" )
    
import sys
sys.exit(0)


# 6288

# 7335

# population["costs"] = []
# for person in range(0, total_flow):
#     if population["decisions"][person]=="Lincoln":
#         population["costs"].append(km_cost_lincoln + tt_lincoln[flow_A]/60*population["VOT"][person])
#     else:
#         population["costs"].append(km_cost_george + tt_george[flow_B]/60*population["VOT"][person])


# costs_A = 0
# costs_B = 0
# for person in range(0, total_flow):
#     if population["decisions"][person]=="Lincoln":
#         costs_A += population["costs"][person]
#     else:
#         costs_B += population["costs"][person]
        
        
# print(flow_A, flow_B)
# print(costs_A, costs_B)
# print(costs_A/flow_A, costs_B/flow_B)

# av_vot = np.mean(population["VOT"])
# print(km_cost_lincoln+tt_lincoln[flow_A]/60*av_vot, 
#       km_cost_george+tt_george[flow_B]/60*av_vot)

import sys
sys.exit(0)
    

# # #############################################################################
# # MAIN CALCULATION AND VISUALIZATION
# # #############################################################################

# Figures
plt.rc('font', family='sans-serif') 
plt.rc('font', serif='Arial') 
plt.figure(figsize=(6, 4), dpi=100)
plt.subplot(2,1,1)
plt.title("Vehicle Travel Time per Route")
plt.plot(flows, tt_lincoln, label="Lincoln Tunnel", color="blue")
plt.fill_between(flows, np.asarray(tt_lincoln)-np.asarray(tt_lincoln_std), np.asarray(tt_lincoln)+np.asarray(tt_lincoln_std), alpha=0.5, facecolor="blue")
plt.plot(flows, tt_george, label="George Washington Bridge", color="black")
plt.fill_between(flows, np.asarray(tt_george)-np.asarray(tt_george_std), np.asarray(tt_george)+np.asarray(tt_george_std), alpha=0.5, facecolor="black")
plt.legend(loc="upper left")
plt.xlabel("Flow [veh/h]")
plt.ylabel("Travel Time [min]")
plt.ylim(25, 100)
plt.xlim(1000, 15000)

plt.subplot(2,1,2)
plt.title("Total Travel Time per Traffic Split")
valTTT = calculateTTT(tt_lincoln, tt_george, total_flow)
valTTT_U = calculateTTT(np.asarray(tt_lincoln)+np.asarray(tt_lincoln_std), np.asarray(tt_george)+np.asarray(tt_george_std), total_flow)
valTTT_L = calculateTTT(np.asarray(tt_lincoln)-np.asarray(tt_lincoln_std), np.asarray(tt_george)-np.asarray(tt_george_std), total_flow)
plt.plot(flows_real, valTTT, color="blue")
plt.fill_between(flows_real, valTTT_L, valTTT_U, alpha=0.5, facecolor="blue")
plt.xlabel("Split on Lincoln Tunnel [veh/h]")
plt.ylabel("vehicle x hours")

minV = np.min(valTTT)
minF = np.argmin(valTTT)
plt.scatter(minF, minV, color="black")
plt.text(minF-1100, minV+2000, "  System Optimum\n    "+str(int(minV))+" hours\n      "+str(int(minF))+" veh/h")
plt.ylim(6000, 15000)
plt.xlim(0, total_flow)


print("System Optimum", minF, "veh/h on Lincoln, ", valTTT[minF]/total_flow*60, "mins TT")
flowA, flowB, flows_A = getUserOptimum(tt_lincoln, tt_george, total_flow)
print("Wardrop Equilibrium", flowA, "veh/h on Lincoln, ", valTTT[flowA-1]/total_flow*60, "mins TT")
print("Cost due to egoism", valTTT[minF]/total_flow*60 - valTTT[flowA-1]/total_flow*60, "mins TT")

plt.tight_layout()

import sys
sys.exit(0)


flowA, flowB, flows_A = getUserOptimum(tt_lincoln, tt_george, total_flow)
# plt.plot(flows_real, flows_A)

