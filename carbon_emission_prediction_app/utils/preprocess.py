import pandas as pd

def preprocess_input(fuel_consumption, vehicle_type, distance, engine_size, country_factor):
    """
    Preprocess user input for model prediction.
    """
    input_data = pd.DataFrame({
        'fuel_consumption': [fuel_consumption],
        'vehicle_type': [vehicle_type],
        'distance': [distance],
        'engine_size': [engine_size],
        'country_factor': [country_factor]
    })
    return input_data
