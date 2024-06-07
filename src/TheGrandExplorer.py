# Imports
import matplotlib.pyplot as plt
import os
import json
import pandas as pd




# Parameters
json_folder = "clusterresult/result_json/"
csv_folder = "clusterresult/result_csv/"

# Draw Parameters
method = 1     # 1 2 3 4

# Determine result timestamps
files = os.listdir(json_folder)
json_buffer = {}
for file in files:
    timestamp = file.split("_json_")[1].split(".json")[0]
    json_buffer[timestamp] = json.load(open(json_folder+file, "r"))
    
    # {"simulation_time": 800, "simulation_type": 1, "pop_size": 10000, "urgency_scenario": 0, "history_length_personal": 5, "history_length_reported": 5, "history_weight_personal": 0, "history_weight_reported": 1, "exploration_rate": 0.02, "system_optimum": 3983, "nash_equilibrium": 6169, "seed": 42}



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
    if plot_by_expl_rates:
        for expl in [0.00, 0.001, 0.01, 0.02]:
            df = timeSeriesDF(meth=method, weigA=weigA, weigB=weigB, expl=expl, hor=alter)
            if not df is None:
                plt.plot(df["time"], df["flow_A"], label="Expl.Rate="+str(expl))
    else:
         for hor in [5, 10, 15, 50]:
             df = timeSeriesDF(meth=method, weigA=weigA, weigB=weigB, expl=alter, hor=hor)
             if not df is None:
                 plt.plot(df["time"], df["flow_A"], label="Horizon="+str(hor))
    plt.legend()
    
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
        



plt.figure(figsize=(8.2, 11.6)) # din-a4 size in inch
    
method=1

plt.subplot(5,3,1)
plt.title("Exploration Rate = 0.00")
drawFigure(sidetitle="Both", shall_draw_y=True, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.00, weigA=1, weigB=1)
plt.subplot(5,3,2)
plt.title("Exploration Rate = 0.01")
drawFigure(sidetitle="Both", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.01, weigA=1, weigB=1)
plt.subplot(5,3,3)
plt.title("Exploration Rate = 0.02")
drawFigure(sidetitle="Both", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.02, weigA=1, weigB=1)
    
plt.subplot(5,3,4)
plt.title("Exploration Rate = 0.00")
drawFigure(sidetitle="Only Rep", shall_draw_y=True, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.00, weigA=0, weigB=1)
plt.subplot(5,3,5)
plt.title("Exploration Rate = 0.01")
drawFigure(sidetitle="Only Rep", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.01, weigA=0, weigB=1)
plt.subplot(5,3,6)
plt.title("Exploration Rate = 0.02")
drawFigure(sidetitle="Only Rep", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.02, weigA=0, weigB=1)

plt.subplot(5,3,7)
plt.title("Exploration Rate = 0.00")
drawFigure(sidetitle="Only Pers", shall_draw_y=True, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.00, weigA=1, weigB=0)
plt.subplot(5,3,8)
plt.title("Exploration Rate = 0.01")
drawFigure(sidetitle="Only Pers", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.01, weigA=1, weigB=0)
plt.subplot(5,3,9)
plt.title("Exploration Rate = 0.02")
drawFigure(sidetitle="Only Pers", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.02, weigA=1, weigB=0)

plt.subplot(5,3,10)
plt.title("Exploration Rate = 0.00")
drawFigure(sidetitle="Both 2-1", shall_draw_y=True, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.00, weigA=2, weigB=1)
plt.subplot(5,3,11)
plt.title("Exploration Rate = 0.01")
drawFigure(sidetitle="Both 2-1", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.01, weigA=2, weigB=1)
plt.subplot(5,3,12)
plt.title("Exploration Rate = 0.02")
drawFigure(sidetitle="Both 2-1", shall_draw_y=False, shall_draw_x=False, plot_by_expl_rates=False, timelimit=[0,500], alter=0.02, weigA=2, weigB=1)

plt.subplot(5,3,13)
plt.title("Exploration Rate = 0.00")
drawFigure(sidetitle="Both 1-2", shall_draw_y=True, shall_draw_x=True, plot_by_expl_rates=False, timelimit=[0,500], alter=0.00, weigA=1, weigB=2)
plt.subplot(5,3,14)
plt.title("Exploration Rate = 0.01")
drawFigure(sidetitle="Both 1-2", shall_draw_y=False, shall_draw_x=True, plot_by_expl_rates=False, timelimit=[0,500], alter=0.01, weigA=1, weigB=2)
plt.subplot(5,3,15)
plt.title("Exploration Rate = 0.02")
drawFigure(sidetitle="Both 1-2", shall_draw_y=False, shall_draw_x=True, plot_by_expl_rates=False, timelimit=[0,500], alter=0.02, weigA=1, weigB=2)


plt.tight_layout()

# weight = [0, 1] # [0,1] [1,0] [1,1] [2,1] [1,2]
# explor = 0.00   # 0.00 0.001 0.01 0.02
# horizo = 5      # 5 10 15 50

# shall_draw_y = True
# shall_draw_x = True
# plot_by_expl_rates = True
# timelimit = [0, 500]
# alter = 5


    
# plt.title("Four Consecutive Annotation Boxes")
# # draw Image
# plt.gca().imshow(image, interpolation='none')
# plt.axis("equal")
# plt.gca().invert_yaxis()
# # draw annotations
# drawAnnotationSubFunction(anno1, coordinates, circle_annotation1, "red")
# drawAnnotationSubFunction(anno2, coordinates, circle_annotation2, "orange")
# drawAnnotationSubFunction(anno3, coordinates, circle_annotation3, "yellow")
# drawAnnotationSubFunction(anno4, coordinates, circle_annotation4, "green")
# # draw initial labels
# trans_annotation = transformAnnotationsFrom2DMToPixel(anno1, circle_annotation1)
# for idx in range(0, len(initial_labels)):
#     plt.text(trans_annotation[idx][1], trans_annotation[idx][2], str(initial_labels[idx]), 
#               #color="white",
#               fontsize=10, 
#               bbox=dict(boxstyle="round", ec=(1., 0.5, 0.5), fc=(1., 0.8, 0.8),) 
#               )
    
# plt.xlim([760,2560])
# plt.ylim([530,2150])
# plt.legend()
