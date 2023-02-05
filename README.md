# Football 11-vs-11 Simulation
Web application for player-based football match result prediction. User can build custom teams and then try to predict the result of the match between those two teams.

Can be used to:

- Find out how a player played in a different position can affect the match result
- Find out the impact of only 1 different player from starting line-up can affect the match result

## Motivation

1. I like the idea
2. Want to code a project of something I like
3. Want to practice my machine learning engineering skills
4. It's fun (until I reached the data cleaning part, which is 1 day in after I started the project)


## Stack Used

Python for everything. But to be specific:

- Data Scraping: Beautifulsoup4, Pandas.
- Data Transformation/Preprocessing: Numpy, Pandas.
- Modeling: Tensorflow/Keras.
- MLOps: ,
- Backend: Django.
- Frontend: React.

## Test is Performed On

- When the data is scraped
- When the data is about to be transformed
- After the data is transformed
- After feature engineering
- Before the data is used to train/retrain the model (tfdv)
- Before the model is served

## Machine Learning End-to-End Project

<!-- Insert Gambar ML Life Cycle-->

### Goal

- Predict football match result based on players capabilities
- Enables user to measure the impact of a player on a match

### Data Acquisition

- What is the data (and source)

  - Information regarding a match which consists of the general information of the match
  - The players pre-match information like their statistics up to before the match
  - Post-match information which consists of the match result and the players that played the game (including subs) along with additional information such as how many minutes they played and their position

- How is the data collected

The data is collected through scraping method. A script to automate the process was created so the scraping can just be done by running the script from the terminal.

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

Consistent data shape and format. Treating the missing value (either as 0 or kept as NaN).

### Data Transformation / Feature Engineering

- Handling some common things: missing values, skewed/outlier, duplicates, data types
- Numerical variables
  - per 90s or not
  - standardization/normalization
  - data type (int and float variants like float16, float32, etc.)

- Categorical variables
  - Player Position feature. There are sixteen different positions recorded in fbref, and it's possible for a player to have more than one position. One-hot encoding will make the dimension grow by 16x11x2 = 352 if we only consider starters in our model. So position embedding was employed.

- Challenges
  - Handling the position information

### Feature Selection

- Manual Selection, but
  - needs to consider attack and defense category along other category like possession and goalkeeping statistics
  - either separate goalkeeper or treat goalkeeper as any other player, meaning that outfield players will also have goalkeeper stats as inputs for the model

- Challenges
  - Selecting features is tricky because in football, one's attribute (say, shooting) may or may not effect the game depends on either the player's other attributes or the players' teammates or opponents.
  - Selecting one additional feature/attribute for a player means multiplying that feature by the number of players being accounted for the model.

### Model Creation & Evaluation

- Models
  - Neural Network (baseline)
  - Embedding + NN
  - 1D-CNN/LSTM/BiLSTM
  - Transformer Encoder
  - NN/Embedding/Transformer for Feature Extraction and then classic ML models

- Evaluation
  - Score: mean absolute error, rooted mean squared error
  - Win/Draw/Loss: categorical crossentropy loss, accuracy

- Hyperparameter Tuning

- Challenges
  - Deciding on evaluation/performance metric and why
  - Hyperparams tuning
  - Randomness nature of football

### Model Deployment & Monitoring

- What's being monitored
  - Inputs (details & distribution)
  - Outputs/Predictions (details & distribution)
  - Feature & Model versions
  - Latency
  - IO/Memory/Disk Utilisation
  - Uptime/System Reliability
  - Read/Write

- How is the model deployed
  - Website interface
  - API

- Challenges
  - Custom monitoring system may be needed

### Model Re-Training & Model Re-Deployment

- Challenges
