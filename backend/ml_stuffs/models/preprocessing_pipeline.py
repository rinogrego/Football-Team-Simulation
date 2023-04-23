from sklearn.preprocessing import MinMaxScaler
import pandas as pd

class Pipeline:
    def __init__(self, register_features):
        self.MinMaxScaler_per_attribute = {}
        self.features = register_features
        for attribute in register_features:
            self.MinMaxScaler_per_attribute[attribute] = MinMaxScaler()
    
    def fit(self, X_train):
        print("Features for fitting:")
        for attribute in self.features:
            feature_values = X_train.loc[:, pd.IndexSlice[:, :, attribute]].unstack().values.reshape(-1, 1)
            self.MinMaxScaler_per_attribute[attribute].fit(feature_values)
            print(attribute, end=", ")

    def transform(self, X, inference=False):
        X_transform = X.copy()
        if not inference:
            teams = X.columns.get_level_values(level="Club").unique().to_list()
            players = X.columns.get_level_values(level="Player").unique().to_list()
            for team in teams:
                for player in players:
                    for attribute in self.features:
                        values = X_transform.loc[:, pd.IndexSlice[team, player, attribute]].values.reshape(-1, 1)
                        X_transform.loc[:, pd.IndexSlice[team, player, attribute]] = self.MinMaxScaler_per_attribute[attribute].transform(values)
        elif inference:
            # inference mode only have 1 level column
            for attribute in self.features:
                values = X_transform.loc[:, pd.IndexSlice[attribute]].values.reshape(-1, 1)
                X_transform.loc[:, pd.IndexSlice[attribute]] = self.MinMaxScaler_per_attribute[attribute].transform(values)
        return X_transform


import __main__
__main__.Pipeline = Pipeline