# Imports
import matplotlib.pyplot as plt
import os
import json
import pandas as pd




# Parameters
json_folder = "clusterresult/result_json/"
csv_folder = "clusterresult/result_csv/"

# Draw Parameters
method = 4     # 1 2 3 4

# Determine result timestamps
files = os.listdir(json_folder)
json_buffer = {}
for file in files:
    timestamp = file.split("_json_")[1].split(".json")[0]
    json_buffer[timestamp] = json.load(open(json_folder+file, "r"))
    
    # {"simulation_time": 800, "simulation_type": 1, "pop_size": 10000, "urgency_scenario": 0, "history_length_personal": 5, "history_length_reported": 5, "history_weight_personal": 0, "history_weight_reported": 1, "exploration_rate": 0.01, "system_optimum": 3983, "nash_equilibrium": 6169, "seed": 42}



def getTimeTimeStamp(meth, weigA, weigB, expl, hor):
    for timestamp in json_buffer:
        if json_buffer[timestamp]["simulation_type"]==meth and json_buffer[timestamp]["history_weight_personal"]==weigA and json_buffer[timestamp]["history_weight_reported"]==weigB and json_buffer[timestamp]["exploration_rate"]==expl and json_buffer[timestamp]["history_length_personal"]==hor:
            return timestamp
    return None

def timeSeriesDF(meth, weigA, weigB, expl, hor):
    timestamp = getTimeTimeStamp(meth, weigA, weigB, expl, hor)
    if not timestamp is None:
        df = pd.read_csv(csv_folder+"simulation_results_csv_"+timestamp+".csv")
        return df
    print("niet availabilski", meth, weigA, weigB, expl, hor)
    return None

def drawFigure(sidetitle, shall_draw_y=True, shall_draw_x=True, plot_by_expl_rates=True, timelimit=[0,500], alter=5, weigA=1, weigB=1):
    colors = ["orange", "blue", "red", "lightgreen"]
    ctr = 0
    if plot_by_expl_rates:
        for expl in [0.00, 0.001, 0.00, 0.01]:
            df = timeSeriesDF(meth=method, weigA=weigA, weigB=weigB, expl=expl, hor=alter)
            if not df is None:
                plt.plot(df["time"], df["flow_A"], label="Expl.Rate="+str(expl), color=colors[ctr])
            ctr+=1
    else:
         for hor in [5, 10, 15, 50]:
             df = timeSeriesDF(meth=method, weigA=weigA, weigB=weigB, expl=alter, hor=hor)
             if not df is None:
                 plt.plot(df["time"], df["flow_A"], label="Horizon="+str(hor), color=colors[ctr])
             ctr+=1
    plt.legend(loc="lower right")
    
    plt.plot(timelimit, [3983, 3983], "--", color="gray")
    plt.plot(timelimit, [6179, 6179], "--", color="gray")
    
    plt.ylim(0, 10000)
    plt.xlim(timelimit[0], timelimit[1])
    if not shall_draw_y:
        plt.yticks([])
    else:
        plt.ylabel(sidetitle+"\nTravel Split [veh/h]")
    if not shall_draw_x:
        plt.xticks([])
    else:
        plt.xlabel("Simulation Time [days]")
        


# METHODEN
# A - 2 (unweighted)
# B - 1 (geometric)
# C - 3 (exponential)
# D - 4 (MAX)


# #############################################################################
# # FIG NR 1 (upper)
# #############################################################################
# plt.figure(figsize=(8.2, 3.5)) # din-a4 size in inch
    
# plt.suptitle("                                (A) Only Personal                                           (B) Only Reported", fontweight="bold")

# plt.subplot(1,3,1)
# df = timeSeriesDF(meth=2, weigA=1, weigB=0, expl=0.00, hor=10)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=1%", color="blue")
# df = timeSeriesDF(meth=2, weigA=1, weigB=0, expl=0.01, hor=10)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=2%", color="green")
# df = timeSeriesDF(meth=2, weigA=1, weigB=0, expl=0.05, hor=10)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=5%", color="orange")
# plt.xlabel("Simulation Time [days]")
# plt.ylabel("Travel Split [veh/h]")
# plt.legend()
# plt.plot([0, 500], [3983, 3983], "--", color="gray")
# plt.plot([0, 500], [6179, 6179], "--", color="gray")
# plt.ylim([5800,6300])
# plt.xlim([0,300])

# plt.subplot(3,3,2)
# plt.title("Exploration Rate 1%")
# df = timeSeriesDF(meth=2, weigA=1, weigB=0, expl=0.01, hor=10)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=1%", color="blue")
# plt.xlim([200,300])
# plt.ylim([6000, 6300])
# plt.plot([0, 500], [3983, 3983], "--", color="gray")
# plt.plot([0, 500], [6179, 6179], "--", color="gray")
# plt.subplot(3,3,5)
# plt.title("Exploration Rate 2%")
# df = timeSeriesDF(meth=2, weigA=1, weigB=0, expl=0.02, hor=10)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=2%", color="green")
# plt.xlim([200,300])
# plt.ylim([6000, 6300])
# plt.plot([0, 500], [3983, 3983], "--", color="gray")
# plt.plot([0, 500], [6179, 6179], "--", color="gray")
# plt.subplot(3,3,8)
# plt.title("Exploration Rate 5%")
# df = timeSeriesDF(meth=2, weigA=1, weigB=0, expl=0.05, hor=10)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=5%", color="orange")
# plt.xlim([200,300])
# plt.ylim([6000, 6300])
# plt.xlabel("Simulation Time [days]")
# plt.plot([0, 500], [3983, 3983], "--", color="gray")
# plt.plot([0, 500], [6179, 6179], "--", color="gray")

# plt.subplot(1,3,3)
# df = timeSeriesDF(meth=2, weigA=0, weigB=1, expl=0, hor=10)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=0%", color="blue")
# df = timeSeriesDF(meth=2, weigA=0, weigB=1, expl=0.01, hor=10)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=1%", color="green")
# df = timeSeriesDF(meth=2, weigA=0, weigB=1, expl=0.05, hor=10)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=5%", color="orange")
# plt.xlabel("Simulation Time [days]")
# plt.ylabel("Travel Split [veh/h]")
# # plt.legend()
# plt.plot([0, 500], [3983, 3983], "--", color="gray")
# plt.plot([0, 500], [6179, 6179], "--", color="gray")
# plt.xlim([100,130])
# # plt.ylim([6000, 6300])

# plt.tight_layout()






# # #############################################################################
# # FIG NR 1 (lower)
# # #############################################################################
# plt.figure(figsize=(8.2, 3.0)) # din-a4 size in inch
    
# # plt.suptitle("                                (A) Only Personal                                           (B) Only Reported", fontweight="bold")

# plt.subplot(1,3,1)
# plt.title("(C) Both (1P-1R)", fontweight="bold")
# # df = timeSeriesDF(meth=2, weigA=1, weigB=1, expl=0.05, hor=5)
# # plt.plot(df["time"], df["flow_A"], label="Horizon=5")
# df = timeSeriesDF(meth=2, weigA=1, weigB=1, expl=0.05, hor=10)
# plt.plot(df["time"], df["flow_A"], label="Horizon=10", color="orange")
# # df = timeSeriesDF(meth=2, weigA=1, weigB=1, expl=0.05, hor=15)
# # plt.plot(df["time"], df["flow_A"], label="Horizon=15")
# plt.xlabel("Simulation Time [days]")
# plt.ylabel("Travel Split [veh/h]")
# plt.plot([0, 500], [3983, 3983], "--", color="gray")
# plt.plot([0, 500], [6179, 6179], "--", color="gray")
# plt.ylim([2000, 9000])
# plt.xlim([0,300])
# # plt.legend()

# plt.subplot(1,3,2)
# plt.title("(D) Both (2P-1R)", fontweight="bold")
# df = timeSeriesDF(meth=2, weigA=2, weigB=1, expl=0.05, hor=10)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=1%", color="orange")
# plt.xlabel("Simulation Time [days]")
# plt.plot([0, 500], [3983, 3983], "--", color="gray")
# plt.plot([0, 500], [6179, 6179], "--", color="gray")
# plt.ylim([2000, 9000])
# plt.xlim([0,300])

# plt.subplot(1,3,3)
# plt.title("(E) Both (1P-2R)", fontweight="bold")
# df = timeSeriesDF(meth=2, weigA=1, weigB=2, expl=0.05, hor=10)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=1%", color="orange")
# plt.xlabel("Simulation Time [days]")
# plt.plot([0, 500], [3983, 3983], "--", color="gray")
# plt.plot([0, 500], [6179, 6179], "--", color="gray")
# plt.ylim([2000, 9000])
# plt.xlim([0,300])



# plt.tight_layout()





# # #############################################################################
# # FIG NR 2
# # #############################################################################
# plt.figure(figsize=(8.2, 3.0)) # din-a4 size in inch
    
# # plt.suptitle("                                (A) Only Personal                                           (B) Only Reported", fontweight="bold")

# plt.subplot(1,3,1)
# plt.title("(A) Plain Average", fontweight="bold")
# df = timeSeriesDF(meth=2, weigA=2, weigB=1, expl=0.05, hor=5)
# plt.plot(df["time"], df["flow_A"], label="Horizon=5")
# df = timeSeriesDF(meth=2, weigA=2, weigB=1, expl=0.05, hor=50)
# plt.plot(df["time"], df["flow_A"], label="Horizon=50")
# plt.xlabel("Simulation Time [days]")
# plt.ylabel("Travel Split [veh/h]")
# plt.plot([0, 500], [3983, 3983], "--", color="gray")
# plt.plot([0, 500], [6179, 6179], "--", color="gray")
# plt.ylim([0, 8000])
# plt.xlim([0,300])
# plt.legend()

# plt.subplot(1,3,2)
# plt.title("(B) Geometric Weights", fontweight="bold")
# df = timeSeriesDF(meth=1, weigA=2, weigB=1, expl=0.05, hor=5)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=1%")
# df = timeSeriesDF(meth=1, weigA=2, weigB=1, expl=0.05, hor=50)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=1%")
# plt.xlabel("Simulation Time [days]")
# plt.plot([0, 500], [3983, 3983], "--", color="gray")
# plt.plot([0, 500], [6179, 6179], "--", color="gray")
# plt.ylim([0, 8000])
# plt.xlim([0,300])

# plt.subplot(1,3,3)
# plt.title("(C) Exponential Weights", fontweight="bold")
# df = timeSeriesDF(meth=3, weigA=2, weigB=1, expl=0.05, hor=5)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=1%")
# df = timeSeriesDF(meth=3, weigA=2, weigB=1, expl=0.05, hor=50)
# plt.plot(df["time"], df["flow_A"], label="Expl.Rate=1%")
# plt.xlabel("Simulation Time [days]")
# plt.plot([0, 500], [3983, 3983], "--", color="gray")
# plt.plot([0, 500], [6179, 6179], "--", color="gray")
# plt.ylim([0, 8000])
# plt.xlim([0,300])



# plt.tight_layout()




# #############################################################################
# FIG NR 3
# #############################################################################
plt.figure(figsize=(8.2, 3.0)) # din-a4 size in inch
    
plt.subplot(1,3,1)
plt.title("(A) Personal (2%)", fontweight="bold")
df = timeSeriesDF(meth=4, weigA=1, weigB=0, expl=0.02, hor=5)
plt.plot(df["time"], df["flow_A"], label="Horizon=5", color="orange")
df = timeSeriesDF(meth=4, weigA=1, weigB=0, expl=0.02, hor=10)
plt.plot(df["time"], df["flow_A"], label="Horizon=10", color="blue")
df = timeSeriesDF(meth=4, weigA=1, weigB=0, expl=0.02, hor=15)
plt.plot(df["time"], df["flow_A"], label="Horizon=15", color="lime")
plt.xlabel("Simulation Time [days]")
plt.ylabel("Travel Split [veh/h]")
# plt.legend()
plt.plot([0, 500], [3983, 3983], "--", color="gray")
plt.plot([0, 500], [6179, 6179], "--", color="gray")
plt.ylim([1000, 8000])
plt.xlim([0,300])

plt.subplot(1,3,2)
plt.title("(B) Personal (5%)", fontweight="bold")
df = timeSeriesDF(meth=4, weigA=1, weigB=0, expl=0.05, hor=5)
plt.plot(df["time"], df["flow_A"], label="Horizon=5", color="orange")
df = timeSeriesDF(meth=4, weigA=1, weigB=0, expl=0.05, hor=10)
plt.plot(df["time"], df["flow_A"], label="Horizon=10", color="blue")
df = timeSeriesDF(meth=4, weigA=1, weigB=0, expl=0.05, hor=15)
plt.plot(df["time"], df["flow_A"], label="Horizon=15", color="lime")
plt.xlabel("Simulation Time [days]")
# plt.ylabel("Travel Split [veh/h]")
plt.legend()
plt.plot([0, 500], [3983, 3983], "--", color="gray")
plt.plot([0, 500], [6179, 6179], "--", color="gray")
plt.ylim([1000, 8000])
plt.xlim([0,300])


plt.subplot(1,3,3)
plt.title("(C) Both (1P-1R, 5%)", fontweight="bold")
df = timeSeriesDF(meth=4, weigA=1, weigB=1, expl=0.05, hor=5)
plt.plot(df["time"], df["flow_A"], label="Horizon=5", color="orange")
df = timeSeriesDF(meth=4, weigA=1, weigB=1, expl=0.05, hor=10)
plt.plot(df["time"], df["flow_A"], label="Horizon=10", color="blue")
df = timeSeriesDF(meth=4, weigA=1, weigB=1, expl=0.05, hor=15)
plt.plot(df["time"], df["flow_A"], label="Horizon=15", color="lime")
plt.xlabel("Simulation Time [days]")
# plt.ylabel("Travel Split [veh/h]")
# plt.legend()
plt.plot([0, 500], [3983, 3983], "--", color="gray")
plt.plot([0, 500], [6179, 6179], "--", color="gray")
plt.ylim([1000, 8000])
plt.xlim([0,300])



plt.tight_layout()






import sys
sys.exit(0)

# method 1
# nur personal
# horizon = 10
# expl 0, 0.05


method=2
methods={1:"Geometrically Weighted Mean", 2:"Average", 3:"Exponentially Weighted Mean", 4:"Maximum"}

plt.suptitle("Time Estimation Method "+str(method)+": "+methods[method], fontweight="bold")

plt.subplot(5,4,1)
plt.title("Exploration Rate = 0.00")
drawFigure(sidetitle="Both", shall_draw_y=True, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.00, weigA=1, weigB=1)
plt.subplot(5,4,2)
plt.title("Exploration Rate = 0.01")
drawFigure(sidetitle="Both", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.01, weigA=1, weigB=1)
plt.subplot(5,4,3)
plt.title("Exploration Rate = 0.02")
drawFigure(sidetitle="Both", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.02, weigA=1, weigB=1)
plt.subplot(5,4,4)
plt.title("Exploration Rate = 0.05")
drawFigure(sidetitle="Both", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.05, weigA=1, weigB=1)
    
plt.subplot(5,4,5)
plt.title("Exploration Rate = 0.00")
drawFigure(sidetitle="Only Rep", shall_draw_y=True, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.00, weigA=0, weigB=1)
plt.subplot(5,4,6)
plt.title("Exploration Rate = 0.01")
drawFigure(sidetitle="Only Rep", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.01, weigA=0, weigB=1)
plt.subplot(5,4,7)
plt.title("Exploration Rate = 0.02")
drawFigure(sidetitle="Only Rep", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.02, weigA=0, weigB=1)
plt.subplot(5,4,8)
plt.title("Exploration Rate = 0.05")
drawFigure(sidetitle="Only Rep", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.05, weigA=0, weigB=1)

plt.subplot(5,4,9)
plt.title("Exploration Rate = 0.00")
drawFigure(sidetitle="Only Pers", shall_draw_y=True, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.00, weigA=1, weigB=0)
plt.subplot(5,4,10)
plt.title("Exploration Rate = 0.01")
drawFigure(sidetitle="Only Pers", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.01, weigA=1, weigB=0)
plt.subplot(5,4,11)
plt.title("Exploration Rate = 0.02")
drawFigure(sidetitle="Only Pers", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.02, weigA=1, weigB=0)
plt.subplot(5,4,12)
plt.title("Exploration Rate = 0.05")
drawFigure(sidetitle="Only Pers", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.05, weigA=1, weigB=0)

plt.subplot(5,4,13)
plt.title("Exploration Rate = 0.00")
drawFigure(sidetitle="Both 2-1", shall_draw_y=True, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.00, weigA=2, weigB=1)
plt.subplot(5,4,14)
plt.title("Exploration Rate = 0.01")
drawFigure(sidetitle="Both 2-1", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.01, weigA=2, weigB=1)
plt.subplot(5,4,15)
plt.title("Exploration Rate = 0.02")
drawFigure(sidetitle="Both 2-1", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.02, weigA=2, weigB=1)
plt.subplot(5,4,16)
plt.title("Exploration Rate = 0.05")
drawFigure(sidetitle="Both 2-1", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.05, weigA=2, weigB=1)

plt.subplot(5,4,17)
plt.title("Exploration Rate = 0.00")
drawFigure(sidetitle="Both 1-2", shall_draw_y=True, shall_draw_x=True, plot_by_expl_rates=False, timelimit=[0,500], alter=0.00, weigA=1, weigB=2)
plt.subplot(5,4,18)
plt.title("Exploration Rate = 0.01")
drawFigure(sidetitle="Both 1-2", shall_draw_y=False, shall_draw_x=True, plot_by_expl_rates=False, timelimit=[0,500], alter=0.01, weigA=1, weigB=2)
plt.subplot(5,4,19)
plt.title("Exploration Rate = 0.02")
drawFigure(sidetitle="Both 1-2", shall_draw_y=False, shall_draw_x=True, plot_by_expl_rates=False, timelimit=[0,500], alter=0.02, weigA=1, weigB=2)
plt.subplot(5,4,20)
plt.title("Exploration Rate = 0.05")
drawFigure(sidetitle="Both 1-2", shall_draw_y=False, shall_draw_x=True, plot_by_expl_rates=False, timelimit=[0,500], alter=0.05, weigA=1, weigB=2)


plt.tight_layout()
