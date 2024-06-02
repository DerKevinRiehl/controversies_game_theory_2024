import random
import json
import os
import numpy as np

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