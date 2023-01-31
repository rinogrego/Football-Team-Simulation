## Data Storage Folder

This is where the data is stored. Everything in this folder is used as data storage.
The folder structure is:
```
data
    ├── fbref
    │        ├── raw
    │        │      └── Premier League
    │        │              ├── 2022-2023_Matches
    │        │              │       ├── 2023-01-18_Crystal-Palace-vs-Manchester-United.csv
    │        │              │       ├── 2023-01-18_Crystal-Palace-vs-Manchester-United.json
    │        │              │       └── ...
    │        │              └── table_ref.csv
    │        └── dictionaries.json
    └── transformed
            ├── data_for_ml.parquet
            └── ...
```