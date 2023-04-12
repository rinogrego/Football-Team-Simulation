import pandas as pd
import json
import numpy as np

def create_instance(request_data):
    
    f = open("features/store/feature_test.json")
    attributes_list = json.load(f)["register_features"]
    player_ref = pd.read_csv("data/transformed/player_references.csv", index_col=0).groupby(["player"], as_index=False).sum()
    # instance = {}
    instance = {
        "home_player_01": [],
        "home_player_01_position": [],
        "home_player_02": [],
        "home_player_02_position": [],
        "home_player_03": [],
        "home_player_03_position": [],
        "home_player_04": [],
        "home_player_04_position": [],
        "home_player_05": [],
        "home_player_05_position": [],
        "home_player_06": [],
        "home_player_06_position": [],
        "home_player_07": [],
        "home_player_07_position": [],
        "home_player_08": [],
        "home_player_08_position": [],
        "home_player_09": [],
        "home_player_09_position": [],
        "home_player_10": [],
        "home_player_10_position": [],
        "home_player_11": [],
        "home_player_11_position": [],
        "away_player_01": [],
        "away_player_01_position": [],
        "away_player_02": [],
        "away_player_02_position": [],
        "away_player_03": [],
        "away_player_03_position": [],
        "away_player_04": [],
        "away_player_04_position": [],
        "away_player_05": [],
        "away_player_05_position": [],
        "away_player_06": [],
        "away_player_06_position": [],
        "away_player_07": [],
        "away_player_07_position": [],
        "away_player_08": [],
        "away_player_08_position": [],
        "away_player_09": [],
        "away_player_09_position": [],
        "away_player_10": [],
        "away_player_10_position": [],
        "away_player_11": [],
        "away_player_11_position": []
    }
    instance_keys = [key for key in instance.keys()]
    
    for key, value in request_data.items():
        if key in instance_keys:
            if "position" in key:
                instance[key] = np.array([value], dtype="object")
            else:
                instance[key] = player_ref.query("player == @value")[attributes_list].fillna(0).to_numpy()
            
    return instance