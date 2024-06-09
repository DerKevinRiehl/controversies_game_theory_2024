import random
import json
import os
import numpy as np
import math

def set_seed(seed:int) -> None:
    """Set random seed (reproducibility)"""
    np.random.seed(seed)
    random.seed(seed)

def load_parameters_json(filename: str) -> dict:
    """Open the path to a json file and return it's content"""
    path_file = os.path.dirname(__file__) + "/"+ filename

    # check if file exists
    if not os.path.exists(path_file):
        raise FileNotFoundError(f"The path '{path_file}' is missing. Must be in same folder as main")
    
    with open(path_file, "r") as read_file:
        return json.load(read_file)
    
def csv_results(df_records, current_time) -> None:
    """Create a CSV with the results"""
    if not os.path.exists("result_csv"):
        os.makedirs("result_csv")
    filename = f'simulation_results_csv_{current_time}.csv'
    df_records.to_csv('result_csv/'+filename)

def json_output(config, current_time) -> None:
    """Save the current config to a json file with the same timestamp as csv and plot"""
    if not os.path.exists("result_json"):
        os.makedirs("result_json")
    filename = f'simulation_results_json_{current_time}.json'
    with open('result_json/' + filename, 'w') as json_file:
        json.dump(config,json_file)
    

def compute_geometric_weights(iterable: list):
    res = np.asarray([1/(i+1) for i in range(0, len(iterable))])
    res = np.flip(res) # most recent / higher index is weighted stronger
    res /= np.sum(res)
    return res

def compute_exponential_weights(iterable: list):
    res = np.asarray([math.exp(i) for i in range(0, len(iterable))])
    res /= np.sum(res)
    return res