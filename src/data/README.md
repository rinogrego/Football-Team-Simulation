<!-- ## Database Structure

|- Raw
|   |
|   |- Premier League
|   |   |
|   |   |- Matches (data type: list containing 3 key-value pairs of links of post-match information and pre-match
|   |       |       squad information of both teams as keys and their corresponding soups data in string as values)
|   |       |
|   |       |- 2023-01-31_Team-A-vs-Team-B.json
|   |       |
|   |       |- 2023-01-31_Team_D-vs-Team_C.json
|   |       |
|   |       |- ...
|   |
|   |- ...
|
|- Clean
    |
    | - Premier League
        |
        |- Matches (data type: .csv)
        |   |
        |   |- 2023-01-31_Team_A-vs-Team_B.csv
        |   |
        |   |- 2023-01-31_Team_D-vs-Team_C.csv
        |
        |- Previous_Fixtures.csv -->


## Data Flow

### Data Collection
1. Where is the data came from
2. How is the availability of the data
3. How is the data stored
4. How is the data updated
5. Data types consistency
6. Null/missing values

### Data Preprocessing
1. How is the data being processed
2. How is the preprocessed data stored
3. How is the position information handled


## Data Repositories

### Dictionaries
Contains dictionaries of key-valued pairs indicating either the league/team/player's code for the url or the value used to display (e.g. Manchester United in fbref is displayed as Manchester Utd).

### Raw
Repository containing raw data collected/scraped directly from the websites. The data stored in bs4/beautifulsoup/... format.

### Transformed
Repository containing transformed data ready to be used for modeling or analysis.

## Potential Data Problem

1. Feature Inconsistencies
2. Change in HTML structure of the website
3. Clubs using new player that hasn't been recorded before the match started
4. Potential scaling problems (data size per match, speed of read/write new data, etc.)
5. Data Usage Permission
6. New League, Season, etc.


## Things to Track

1. Data availability
2. HTML source format
3. Potential labels
4. Where the data come from