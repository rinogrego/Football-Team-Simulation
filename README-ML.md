# Machine Learning End-to-End Project

This README section explains the things regarding end-to-end machine learning of this project from collecting the data to deploying the model and further things that can be implemented or improved.

<!-- Insert Gambar ML Life Cycle -->

## Project Goal

- Predict football match result based on players capabilities
- Enables user to measure the impact of a player on a match

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

The `collect.py` scripts is run manually, so depends on how frequent the script is run. But preferrably the script should be run between two different gameweeks because the pre-match information of match at gameweek N, around the last time the script was run, may be populated with pre-match information of match at gameweek N+T, with T being around the time the script is run, which should be impossible because it means pre-match info at gameweek N is populated by future statistics.

Like for example if at gameweek 21 I run the script and get pre-match info of gameweek 22, and then I run the script again at gameweek 24, the script will retrieve pre-match info of gameweek 25 for not only gameweek 25 but also for gameweek 23 and 24.

- How is the data stored

The data is stored in folder specialized for storage so that it can be switched to cloud storage if ever needed. Pre-match information are stored with .csv format and the post-match information are stored with json. Though in the future, the .csv format might be changed to something different (e.g. pickle, parquet, json)

- Challenges
  - Structuring the data. Even in one source, sometimes the structure of one category from one table can be different in two different teams
  - Keeping track of the dimension, shape, inconsistencies, data-type
  - Repetitive checks of each code/function done (There was a time I didn't do it and the saved data was ended up messy. Fortunately I managed to make script to fix that)

## Data Cleaning

- Handling some common things: missing values, skewed/outlier, duplicates, data types

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

The model is deployed by two ways: first is via django templating HTML for web interface, second is via API with djangorestframework.

### Local Deployment

Steps to local deployment

### API Call

API docs

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
