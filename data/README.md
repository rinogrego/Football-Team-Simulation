## Data Storage Folder

This is where the data is stored. Everything in this folder is used as data storage.
The folder structure is:
```
data
    ├── fbref
    │   ├── raw
    │   │   └── Premier League
    │   │       ├── 2022-2023_Matches
    │   │       │   ├── 2023-01-18_Crystal-Palace-vs-Manchester-United.csv
    │   │       │   ├── 2023-01-18_Crystal-Palace-vs-Manchester-United.json
    │   │       │   ├── 2023-01-19_Manchester-City-vs-Tottenham-Hotspur.csv
    │   │       │   ├── 2023-01-19_Manchester-City-vs-Tottenham-Hotspur.json
    │   │       │   └── ...
    │   │       └── table_ref.csv
    │   └── dictionaries.json
    └── transformed
        ├── data_for_ml.parquet
        └── ...
```

Pre-match information including the statistics of each player from both teams are saved in csv format. Post-match information are saved in json format. The file for modeling is saved in parquet format.