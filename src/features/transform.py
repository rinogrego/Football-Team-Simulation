"""
    File to extract information from collected data. 
    The transformed data is saved into data/preprocessed directory as .csv file.
    The transformed data can be used directly for training the model, for analysis, or 
        to be used again for another transformation process.
"""

import argparse
import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
import json


DATA_DIR = "data"
SAVE_DIR = DATA_DIR + "/fbref/raw/Premier League/2022-2023_Matches"
TABLE_REF_PATH = DATA_DIR + "/fbref/raw/Premier League/table_ref.csv"
TRANSFORM_DIR = DATA_DIR + "/transformed"

FEATURES_DIR = "features"

POSITION_CHOICES = [
    "GK", 
    "DF", "CB", "FB", "LB", "RB", "WB",
    "MF", "DM", "CM", "LM", "RM", "WM", "AM",
    "FW", "LW", "RW"
]

TEAM_DISPLAY = json.load(open(f"{DATA_DIR}/fbref/dictionaries.json"))["TEAM_DISPLAY"]


def get_data_for_ml(
    df_recorded_matches: pd.DataFrame, 
    features: list, 
    starter_only: bool = True, 
    ignore_new_players: bool = True
) -> np.ndarray:
    df_for_ml = pd.DataFrame()
    check_cols = features

    for idx, row in df_recorded_matches.reset_index(drop=True).iterrows():
        ###Iterate and combine csv and json files to feed into the ML model
        home = TEAM_DISPLAY[row["Home"]]
        away = TEAM_DISPLAY[row["Away"]]
        date = row["Date"]
        print("Processing:", f"{date}_{home}-vs-{away}")

        # open csv file
        try:
            df_csv = pd.read_csv(f"{SAVE_DIR}/{date}_{home}-vs-{away}.csv", index_col=0, header=[0, 1, 2])
        except:
            print("    File cannot be opened somehow")
            continue
        
        # open json file
        json_file = json.load(open(f"{SAVE_DIR}/{date}_{home}-vs-{away}.json"))
        # iterate over home team
        home_starters = []
        for player, attributes in json_file[home].items():
            if starter_only:
                if "(Sub)" in player:
                    continue
            df_csv[home, player, "Pos"] = attributes["Pos"]
            df_csv[home, player, "Age"] = attributes["Age"]
            df_csv[home, player, "Min"] = attributes["Min"]
            home_starters.append(player)
            
        # iterate over away team
        away_starters = []
        for player, attributes in json_file[away].items():
            if starter_only:
                if "(Sub)" in player:
                    continue
            df_csv[away, player, "Pos"] = attributes["Pos"]
            df_csv[away, player, "Age"] = attributes["Age"]
            df_csv[away, player, "Min"] = attributes["Min"]
            away_starters.append(player)

        # concate column-wise
        df_per_row = df_csv.copy()
        assert len(home_starters) == len(away_starters) == 11
        df_home = df_per_row.loc[:, pd.IndexSlice[home, home_starters, features]].copy()
        df_away = df_per_row.loc[:, pd.IndexSlice[away, away_starters, features]].copy()
        
        _home_starters_recorded = df_home.columns.get_level_values("Player").unique()
        _away_starters_recorded = df_away.columns.get_level_values("Player").unique()
        if ignore_new_players is False:
            # checking team starters that have been fetched from the dataframe
            # if the dataframe of a team contains less than 11 players
            # then that means there is a player that just debuted in that match
            ## for each team check remaining players needed, then
            ##      create numpy array based on the dimension
            ##      create the df along the columns
            ##      concat column-wise with the home/away dataframe
            assert len(_home_starters_recorded) == len(_away_starters_recorded) == 11
        
        if len(_home_starters_recorded) != 11 or len(_away_starters_recorded) != 11:
            # ignore match whose team that has less than 11 players recorded on the match
            print("    Match Ignored since No 11 vs 11")
            continue
        
        # rename player columns from their original names to Player 1, Player 2, etc.
        numbered_player_cols = ["Player_"+f"{i}".zfill(2) for i in range(1, 11+1)]
        # for home team
        real_player_cols = df_home.columns.get_level_values(level="Player")
        real_player_cols_unique = real_player_cols.unique().tolist()
        cols_mapping = {key: value for key, value in zip(real_player_cols_unique, numbered_player_cols)}
        home_level_1 = ["Home"] * 11 * len(features)
        home_level_2 = [cols_mapping[player_name] for player_name in real_player_cols.tolist()]
        home_level_3 = df_home.columns.get_level_values(level=2)
        if len(home_level_1) != len(home_level_2) or \
            len(home_level_1) != len(home_level_3) or \
            len(home_level_2) != len(home_level_3):
            print("    Inconsistent array length construction. Match ignored")
            continue
        new_cols_home = pd.MultiIndex.from_arrays([
            home_level_1,
            home_level_2,
            home_level_3
        ])
        df_home.columns = new_cols_home

        # for away team
        real_player_cols = df_away.columns.get_level_values(level="Player")
        real_player_cols_unique = real_player_cols.unique().tolist()
        cols_mapping = {key: value for key, value in zip(real_player_cols_unique, numbered_player_cols)}
        away_level_1 = ["Away"] * 11 * len(features)
        away_level_2 = [cols_mapping[player_name] for player_name in real_player_cols.tolist()]
        away_level_3 = df_away.columns.get_level_values(level=2)
        if len(away_level_1) != len(away_level_2) or \
            len(away_level_1) != len(away_level_3) or \
            len(away_level_2) != len(away_level_3):
            print("    Inconsistent array length construction. Match ignored")
            continue
        new_cols_away = pd.MultiIndex.from_arrays([
            away_level_1,
            away_level_2,
            away_level_3
        ])
        df_away.columns = new_cols_away    

        # concat column-wise home and away df
        df_per_row = pd.concat([df_home, df_away], axis=1)

        # checking inconsistent columns
        cols = df_per_row.columns.get_level_values(level="Statistic").unique()
        diff_cols = [col for col in cols if col not in check_cols]
        if len(cols) != len(check_cols) and len(check_cols) == 0:
            check_cols = cols
        assert len(diff_cols) == 0

        # get the score
        home_score = int(row["Score"].split("–")[0])
        away_score = int(row["Score"].split("–")[1])
        scores = [[home_score, away_score]]
        columns_Y = pd.MultiIndex.from_arrays([
            ["Home", "Away"],
            ["----", "----"],
            ["Score", "Score"]
        ])
        scores = pd.DataFrame(
            scores,
            columns=columns_Y
        )
        df_per_row = pd.concat([df_per_row, scores], axis=1)
        df_per_row = df_per_row.fillna(0)
        ## save transformed csv
        # df_per_row.to_csv(f"{TRANSFORM_DIR}/{date}_{home}-vs-{away}.csv")
        
        # concate row-wise
        df_for_ml = pd.concat([df_for_ml, df_per_row], axis=0)

    df_for_ml.columns.names = ["Club", "Player", "Statistic"]
    return df_for_ml.reset_index(drop=True)


def process_position(df):
    _df = df.copy()
    teams = ["Home", "Away"]
    numbered_player_cols = ["Player_"+f"{i}".zfill(2) for i in range(1, 11+1)]
    pos_cols = [f"Pos_{pos}" for pos in POSITION_CHOICES]
    position_mlb = MultiLabelBinarizer(classes=POSITION_CHOICES)

    for team in teams:
        for player in numbered_player_cols:
            _pos = _df.loc[:, pd.IndexSlice[team, player, "Pos"]].copy().apply(lambda x: x.split(","))
            _pos_label = position_mlb.fit_transform(_pos)
            for idx, pos in enumerate(POSITION_CHOICES):
                df.loc[:, (team, player, f"Pos_{pos}")] = _pos_label[:, idx]
    
    _df_home = df.loc[:, pd.IndexSlice["Home", :, :]].sort_index(level="Player", axis=1, sort_remaining=False)
    _df_away = df.loc[:, pd.IndexSlice["Away", :, :]].sort_index(level="Player", axis=1, sort_remaining=False)
    df = pd.concat([_df_home, _df_away], axis=1)
    df = df.drop(columns="Pos", axis=1, level=2)
    return df


if __name__ == "__main__":
    features_path = ""
    register_features = json.load(open(f"{FEATURES_DIR}/store/feature_test.json"))["register_features"]
    
    table_ref = pd.read_csv(TABLE_REF_PATH, index_col=0)
    cond = table_ref["Score"].notnull()
    # since the start of the data scrapping for PL matches is at 
    # Crystal Palace vs Manchester United then start from there, whose index is 197
    cond2 = table_ref.index >= 197
    df_recorded_matches = table_ref.loc[cond & cond2, :]
    
    print("============================================================")
    print("Collecting raw data")
    print("------------------------------------------------------------")
    dataset = get_data_for_ml(df_recorded_matches, features=register_features)
    dataset["Home Result", "----", "Win"] = (dataset.loc[:, pd.IndexSlice["Home", "----", "Score"]] > dataset.loc[:, pd.IndexSlice["Away", "----", "Score"]]).apply(lambda x: 1 if x is True else 0)
    dataset["Home Result", "----", "Draw"] = (dataset.loc[:, pd.IndexSlice["Home", "----", "Score"]] == dataset.loc[:, pd.IndexSlice["Away", "----", "Score"]]).apply(lambda x: 1 if x is True else 0)
    dataset["Home Result", "----", "Lost"] = (dataset.loc[:, pd.IndexSlice["Home", "----", "Score"]] < dataset.loc[:, pd.IndexSlice["Away", "----", "Score"]]).apply(lambda x: 1 if x is True else 0)
    print("Raw data collected")
    print("------------------------------------------------------------")
    print("Processing position information")
    print("------------------------------------------------------------")
    X, y = dataset.iloc[:, :-5], dataset.iloc[:, -5:]
    X = process_position(X)
    dataset = pd.concat([X, y], axis=1)
    print("Position processed successfully")
    dataset.to_parquet(f"{TRANSFORM_DIR}/data_for_ml.parquet")
    print("============================================================")
    print("Transforming data is success")
    print(f"Data is saved to: {TRANSFORM_DIR}/data_for_ml.parquet")