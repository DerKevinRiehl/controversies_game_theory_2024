import json
import subprocess

# Load parameters from the JSON file
with open('src/config.json', 'r') as f:
    parameters = json.load(f)

# Define ranges for history lengths, exploration rates, and weights
history_length_range = [1, 5, 10, 15, 20]
exploration_rate_range = [0.02, 0.05,  0.1, 0.5]
weight_range = range(0, 3)
simulation_type_range = range(1, 5)
simulation_time_range = [10]

counter = 0
total_runs = len(history_length_range)**2 * len(exploration_rate_range) * len(simulation_time_range) * len(weight_range)**2 * len(simulation_type_range)

# Loop through each combination of parameters
for simulation_type in simulation_type_range:
    for simulation_time in simulation_time_range:
         for exploration_rate in exploration_rate_range:
            for history_length_personal in history_length_range:
                for history_length_reported in history_length_range:
                    for history_weight_personal in weight_range:
                        for history_weight_reported in weight_range:
                            # Update parameters with the current combination
                            parameters['history_length_personal'] = history_length_personal
                            parameters['history_length_reported'] = history_length_reported
                            parameters['exploration_rate'] = exploration_rate
                            parameters['history_weight_personal'] = history_weight_personal
                            parameters['history_weight_reported'] = history_weight_reported
                            parameters['simulation_type'] = simulation_type
                            parameters['simulation_time'] = simulation_time
                            
                            counter +=1
                            print(f"Iteration {counter}/{total_runs}")
                            # Write updated parameters to a temporary JSON file
                            with open('src/temp_config.json', 'w') as f:
                                json.dump(parameters, f)
                            
                            # Run the main.py file with the updated parameters
                            subprocess.run(['python', 'src/main.py'])

# Optionally, remove the temporary JSON file
import os
os.remove('temp_config.json')
