# Imports
import matplotlib.pyplot as plt
import os
import json
import pandas as pd




# Parameters
json_folder = "clusterresult/x/result_json/"
csv_folder = "clusterresult/x/result_csv/"

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
        



plt.figure(figsize=(11.6, 8.2)) # din-a4 size in inch
    
method=4
methods={1:"Linear Weighted Mean", 2:"Average", 3:"Exponentially Weighted Mean", 4:"Maximum"}

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
