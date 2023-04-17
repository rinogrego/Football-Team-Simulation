# Machine Learning End-to-End Project

This README section explains the things regarding end-to-end machine learning of this project from collecting the data to deploying the model and further things that can be implemented or improved.

<!-- Insert Gambar ML Life Cycle -->
<div align="center">
  <h2>Tech Stack Used</h2>
  <img src="docs\images\football-prediction-project-stacks.PNG" />
</div>

## Project Goal

- Predict football match result based on players capabilities
- Enables user to measure the impact of a player on a match

<div align="center">
  <h2>Project Workflow</h2>
  <img src="docs\images\football-prediction-project-workflow.PNG" />
</div>

## Data Acquisition

<!-- Insert ilustrasi Data Acquisition (fbref logo) along with additional info (like data format (.csv/.json)) -->

- What is the data (and source)

  - Information regarding a match which consists of the general information of the match
  - The players pre-match information like their statistics up to before the match
  - Post-match information which consists of the match result and the players that played the game (including subs) along with additional information such as how many minutes they played and their position
  - Data source: fbref/football references

- How is the data collected

The data is collected through web scraping. A script named `collect.py` to automate the process was created so the scraping can just be done by running that script from the terminal.

- How frequent the data is collected

The `collect.py` script is run manually, so depends on how frequent the script is run. But preferrably the script should be run between two different gameweeks because the pre-match information of match at gameweek N, around the last time the script was run, may be populated with pre-match information of match at gameweek N+T, with T being around the time the script is run, which should be impossible because it means pre-match info at gameweek N is populated by future statistics.

Like for example if at gameweek 21 I run the script and get pre-match info of gameweek 22, and then I run the script again at gameweek 24, the script will retrieve pre-match info of gameweek 25 for not only gameweek 25 but also for gameweek 23 and 24.

- How is the data stored

The data is stored in folder specialized for storage so that it can be switched to cloud storage if ever needed. Pre-match information are stored with .csv format and the post-match information are stored with json. Though in the future, the .csv format might be changed to something different (e.g. pickle, parquet, json)

- Challenges
  - Structuring the data. Even in one source, sometimes the structure of one category from one table can be different in two different teams
  - Keeping track of the dimension, shape, inconsistencies, data-type
  - Repetitive checks of each code/function done (There was a time I didn't do it and the saved data was ended up messy. Fortunately I managed to make script to fix that)

## Data Cleaning

- Handling some common things: missing values, skewed/outlier, duplicates, data types.

Ideally, I should handle all common dirty data things like missing value, skewness/outlier, duplicates, and data types, but for this project I just drop duplicates and replace missing value with 0 since missing value stat basically means the player never attempted/achieved the said stat. I ignored handling the outliers and the data types. If the code breaks later because of data types I will just handle it along the way.

- Challenges
  - Consistent data shape and format. Treating the missing value (either as 0 or kept as NaN).
  - Duplicate found for players transferred within the same league for player references

## Data Transformation / Feature Engineering

<!-- Insert ilustrasi feature engineering: from .csv/.json into multi-level tables -->

~~The data is transformed by various considerations below. A script named `transform.py` to automate the process was created so the transformation can just be done by running that script from the terminal.~~

Data transformation and feature engineering is done in notebook environment. The script (though messy) can be seen inside the `notebooks` directory. Original plan was to create a script to automate the process but I am not confident on my own laptop's CPU performance.

To handle the lack of data I did try to increase the number of data points by augmentation. I think the data is kinda unstructured in that while the information of players' attribute is structured, the order of the player input can be rearranged (like putting goalkeeper in as the first player or the fifth player in the input row since ideally, we want the model to NOT be affected by that positioning)

<!-- Insert ilustrasi feature engineering: augmentation by randomly shuffle players -->

- Numerical variables
  - per 90s or not
  - standardization/normalization
  - data type (int and float variants like float16, float32, etc.)

- Categorical variables
  - Player Position feature. There are seventeen different positions recorded in fbref, and it's possible for a player to have more than one position. One-hot encoding will make the dimension grow by 17x11x2 = 352 if we only consider starters in our model. So position embedding is a good consideration.

- Challenges
  - Too many variables (attributes) to track/monitor (distribution, missing value, etc.)
  - Creating input pipeline (tf.data)
  - Handling the position information

## Feature Selection

- Manual Selection, but
  - needs to consider attack and defense category along other category like possession and goalkeeping statistics
  - either separate goalkeeper or treat goalkeeper as any other player, meaning that outfield players will also have goalkeeper stats as inputs for the model

- Challenges
  - Selecting features is tricky because in football, one's attribute (say, shooting) may or may not effect the game depends on either the player's other attributes or the players' teammates or opponents.
  - Selecting one additional feature/attribute for a player means multiplying that feature by the number of players being accounted for the model.

## Model Creation & Evaluation

<!-- Insert ilustrasi model used -->
<!-- Insert table hyperparam tuning -->

Like data transformation/feature engineering, the modelling task is done in google colab notebook environment. I am more comfortable with it currently.

- (Ideas for) Models
  - ~~Neural Network (baseline)~~
  - ~~Embedding + NN~~
  - ~~1D-CNN/LSTM/BiLSTM~~
  - Transformer Encoder
  - NN/Embedding/Transformer for Feature Extraction and then classic ML models
  - TabTransformer

- Evaluation
  - Score: mean absolute error, rooted mean squared error
  - Win/Draw/Loss: categorical crossentropy loss, accuracy

- Hyperparameter Tuning
  - not yet

- Challenges
  - Deciding on evaluation/performance metric and why
  - Hyperparams tuning
  - Randomness nature of football
  - The model might be biased towards home team winning, so the prediction isn't exactly fair like being played in neutral venue
  - Each league in which the matches were used for training the model might actually have different data and score distributions, so it's something important to note

## Deployment

The model is deployed in two ways: first is via django templating HTML for web interface, second is via API with djangorestframework.

### Local Deployment

Steps to local deployment (from the terminal)

1. Create a new project folder and then go inside that folder.

2. Clone this repository

```
  git clone https://github.com/rinogrego/Football-Team-Simulation && cd Football-Team-Simulation
```

3. Install python package to handle virtual environment.

```
  python -m venv VIRTUALENV_NAME
```

4. Setup virtual environment

```
  VIRTUALENV_NAME\\scripts\\activate
```

5. Install the necessary python packages for the project

```
  pip install -r requirements.txt
```

6. Run the django server

```
  python backend\\manage.py runserver
```

7. To view the server, go to any web browser and then go to the following url: 127.0.0.1:8000

### API Call

This section explains possible API calls that can be requested. With urls below, information available to be retrieved, respectively, are: past predictions made, players & their information available in the database, and the possible position used by the model

```
GET /api/view-predictions/
GET /api/database/players/
GET /api/database/positions/
```

You can make your own prediction by first retrieving available players and then use that information to build your custom line up and then send POST request to the following url to get the prediction.

```
POST /api/predict/
```

If you want to see how to access the API and how to structure the data to send as a POST request, open test_request_api.py. From your project directory, you can run the following python script from the terminal to see the example result which will be printed in the terminal (need to run the server first).

```
    python "backend/football_prediction/tests/test_request_api.py"
```

The script will send a POST request to the given URL:

```
POST /api/predict/
```


With the following json structure:

```
{
    "home_player_01": "Alisson Becker",
    "home_player_01_position": "GK",
    "home_player_02": "Trent Alexander-Arnold",
    "home_player_02_position": "RB",
    "home_player_03": "Joe Gomez",
    "home_player_03_position": "CB",
    "home_player_04": "Joel Matip",
    "home_player_04_position": "CB",
    "home_player_05": "Andy Robertson",
    "home_player_05_position": "LB",
    "home_player_06": "Fabinho",
    "home_player_06_position": "DM",
    "home_player_07": "Stefan Bajcetic",
    "home_player_07_position": "CM",
    "home_player_08": "Naby Keita",
    "home_player_08_position": "CM",
    "home_player_09": "Darwin Nunez",
    "home_player_09_position": "LW",
    "home_player_10": "Mohamed Salah",
    "home_player_10_position": "RW",
    "home_player_11": "Cody Gakpo",
    "home_player_11_position": "ST",
    "away_player_01": "Alisson Becker",
    "away_player_01_position": "GK",
    "away_player_02": "Neco Williams",
    "away_player_02_position": "RB",
    "away_player_03": "Virgil van Dijk",
    "away_player_03_position": "CB",
    "away_player_04": "Konate",
    "away_player_04_position": "CB",
    "away_player_05": "Kostas Tsimikas",
    "away_player_05_position": "LB",
    "away_player_06": "Jordan Henderson",
    "away_player_06_position": "DM",
    "away_player_07": "James Milner",
    "away_player_07_position": "CM",
    "away_player_08": "Thiago",
    "away_player_08_position": "CM",
    "away_player_09": "Luis Diaz",
    "away_player_09_position": "LW",
    "away_player_10": "Roberto Firmino",
    "away_player_10_position": "RW",
    "away_player_11": "Diogo Jota",
    "away_player_11_position": "ST"
}
```
will give the response something like below back

```
{
  'id': 74,
  'datetime': '2023-04-17T11:35:08.840857Z',
  'home_player_01': 'Alisson',
  'home_player_01_position': 'GK',
  'home_player_02': 'Trent Alexander-Arnold',
  'home_player_02_position': 'RB',
  'home_player_03': 'Andrew Robertson',
  'home_player_03_position': 'LB',
  'home_player_04': 'Virgil van Dijk',
  'home_player_04_position': 'CB',
  'home_player_05': 'Ibrahima Konaté',
  'home_player_05_position': 'CB',
  'home_player_06': 'Fabinho',
  'home_player_06_position': 'DM',
  'home_player_07': 'Thiago Alcántara',
  'home_player_07_position': 'CM',
  'home_player_08': 'Jordan Henderson',
  'home_player_08_position': 'CM',
  'home_player_09': 'Darwin Núñez',
  'home_player_09_position': 'LW',
  'home_player_10': 'Mohamed Salah',
  'home_player_10_position': 'RW',
  'home_player_11': 'Cody Gakpo',
  'home_player_11_position': 'FW',
  'away_player_01': 'Aaron Ramsdale',
  'away_player_01_position': 'GK',
  'away_player_02': 'Ben White',
  'away_player_02_position': 'RB',
  'away_player_03': 'Oleksandr Zinchenko',
  'away_player_03_position': 'LB',
  'away_player_04': 'Rob Holding',
  'away_player_04_position': 'CB',
  'away_player_05': 'Gabriel Dos Santos',
  'away_player_05_position': 'CB',
  'away_player_06': 'Thomas Partey',
  'away_player_06_position': 'DM',
  'away_player_07': 'Granit Xhaka',
  'away_player_07_position': 'CM',
  'away_player_08': 'Martin Ødegaard',
  'away_player_08_position': 'CM',
  'away_player_09': 'Martinelli',
  'away_player_09_position': 'LW',
  'away_player_10': 'Bukayo Saka',
  'away_player_10_position': 'RW',
  'away_player_11': 'Gabriel Jesus',
  'away_player_11_position': 'FW',
  'home_score_pred': 2.0121467113494873,
  'away_score_pred': 0.8686701655387878,
  'home_result_pred': 'W'
}
```

## Ideas for future works

- Frontend
  - React implementation
  - Formation form suggestion to auto-fill formations
  - Team separator in player selection form
  - Frontend form validation
- Backend
  - Scheduled data acquisition
  - Access model specifications (model architecture, features used, etc.)
  - Performance monitoring
  - Implement model experiment tracking
  - Implement `collect.py` -> `transform.py` -> `increment_training.py` -> `push_model.py` with one code execution
  - Implement logging
- App Feature
  - Login system
  - League simulation
- Overengineering the entire thing
  - pandas -> polars
  - tfx
  - React
  - Custom monitoring
  - Test cases
  - GitHub actions for CI/CD
  - Docker, kubernetes
