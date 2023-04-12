# Football 11-vs-11 Simulation

<!-- Implement badges: https://shields.io -->

Web application for player-based football match result prediction. User can build custom teams and then try to predict the result of the match between those two teams.

Can be used to:

- Find out how a player played in a different position can affect the match result
- Find out the impact of only 1 different player from starting line-up can affect the match result

## Motivation

1. I like the idea
2. Want to code a project of something I like
3. Want to practice my machine learning engineering skills
4. It's fun (until I reached the data cleaning part, which is 1 day in after I started the project)

## Features

- Predict a football match given players with their positions for each team in a match
<!-- - Given an eleven, simulate a league with that eleven (future feature consideration) -->

## Limitations

- Biased towards home team
- Not many features were considered during model development
- The model was trained on dataset scrapped from five different leagues, but the league information isn't used when training the model. A good assumption to remember

## Stack Used

Python for (almost) everything. But to be specific:

- Data Scraping: Beautifulsoup4, Pandas.
- Data Transformation/Preprocessing: Numpy, Pandas.
- Modeling: Tensorflow/Keras.
- MLOps: Github Actions, Docker.
- Backend: Django, PostgreSQL.
- Frontend: React.

<!-- ## Test is Performed On

- When the data is scraped
- When the data is about to be transformed
- After the data is transformed
- After feature engineering
- Before the data is used to train/retrain the model (tfdv)
- Before the model is served -->

## Project Structure

Project structure manually created following [cookiecutter-data-science](https://drivendata.github.io/cookiecutter-data-science/#directory-structure) guide.
<!-- Insert ilustrasi project structure  -->

## Machine Learning End-to-End Project

<!-- Insert Gambar ML Life Cycle -->

### Goal

- Predict football match result based on players capabilities
- Enables user to measure the impact of a player on a match

### Data Acquisition

<!-- Insert ilustrasi Data Acquisition (fbref logo) along with additional info (like data format (.csv/.json)) -->

- What is the data (and source)

  - Information regarding a match which consists of the general information of the match
  - The players pre-match information like their statistics up to before the match
  - Post-match information which consists of the match result and the players that played the game (including subs) along with additional information such as how many minutes they played and their position
  - Data source: fbref/football references

- How is the data collected

The data is collected through scraping method. A script named `collect.py` to automate the process was created so the scraping can just be done by running that script from the terminal.

- How frequent the data is collected

The data is collected manually, so depends on how frequent the script is run. But preferrably should be between two different gameweeks because the pre-match information of match at gameweek N, around the last time the script was run, may be populated with pre-match information of match at gameweek N+K, with K being around the time the script is run.

- How is the data stored

The data is stored in folder specialized for storage so that it can be switched to cloud storage if ever needed. Pre-match information are stored with .csv format and the post-match information are stored with json. Though in the future, the .csv format might be changed to something different (e.g. pickle, parquet)

- Challenges
  - Structuring the data. Even in one source, sometimes the structure of one category from one table can be different in two different teams
  - Keeping track of the dimension, shape, inconsistencies, data-type
  - Repetitive checks of each code/function done (There was a time I didn't do it and the saved data was ended up messy. Fortunately I managed to make script to fix that)

### Data Cleaning

- Challenges
  - Consistent data shape and format. Treating the missing value (either as 0 or kept as NaN).
  - Duplicate found for players transferred within the same league for player references

### Data Transformation / Feature Engineering

The data is transformed by various considerations below. A script named `transform.py` to automate the process was created so the transformation can just be done by running that script from the terminal.

- Handling some common things: missing values, skewed/outlier, duplicates, data types

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
  - Logging

### Feature Selection

- Manual Selection, but
  - needs to consider attack and defense category along other category like possession and goalkeeping statistics
  - either separate goalkeeper or treat goalkeeper as any other player, meaning that outfield players will also have goalkeeper stats as inputs for the model

- Challenges
  - Selecting features is tricky because in football, one's attribute (say, shooting) may or may not effect the game depends on either the player's other attributes or the players' teammates or opponents.
  - Selecting one additional feature/attribute for a player means multiplying that feature by the number of players being accounted for the model.
  - Logging

### Model Creation & Evaluation

- Models
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

- Challenges
  - Deciding on evaluation/performance metric and why
  - Hyperparams tuning
  - Randomness nature of football
  - The model might be biased towards home team winning, so the prediction isn't exactly fair like being played in neutral venue
  - Each league in which the matches were used for training the model might actually have different data and score distributions, so it's something important to note
  - Logging

### Model Deployment & Monitoring

- What's being monitored
  - Inputs (details & distribution)
  - Outputs/Predictions (details & distribution)
  - Feature & Model versions
  - Traffic
  - Latency
  - IO/Memory/Disk Utilisation
  - Uptime/System Reliability
  - Read/Write

- How is the model deployed
  - Website interface
  - API

- Challenges
  - Custom monitoring system may be needed (like creating new django app in the backend for monitoring-all-things-necessary purpose only)

### Model Re-Training & Model Re-Deployment

- Challenges
  - implementing incremental training
  - monitoring model
  - Tests code or GitHub actions for testing new deployed model against the older version
  - implement A/B test environment

### Overall Challenges Faced

- Properly modelling the problem
  - Need to shuffle player input positions
  - Normalizing the attributes used as inputs
  - Determining the 'properness' of the team's position composition
  - Determining the 'properness' of the player's attributes and their position
- Creating separate logic for backend and frontend
  - backend: djangorestframework
  - frontend: React
- Maintaining data science end-to-end pipeline
