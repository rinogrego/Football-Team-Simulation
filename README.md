# Football 11-vs-11 Simulation
Web application for player-based football match result prediction.

## Motivation
1. I like the idea
2. Wants to code a project of something I like
3. Wants to practice my machine learning engineering skills
4. It's fun (until I reached the data cleaning part, which is 1 day in after I started the project)


        Being serious, I am intrigued in creating a machine learning model to predict football match results. And since football match is heavily dependent on not only the team capabilities but also each players abilities and also their role for the team, I wanted to create a model that can predict the match outcome that consider these things and not just overall team capabilites. This is my main motivation for the project. To create a model that can predict a football match result that considers the details such as not only the player's abilities but also where they play.

    What about the success metric? well I tried to count the visit into my website and also the satisfactory. 
        
        I am well aware this shit can be turned into gambling tool but f*ck it. I did this for fun and to hone my skills.


## Stack Used
- Python for everything. 
- Scraping is done with beautifulsoup4. 
- Preprocessing with numpy & pandas (considering to switch to polars). 
- Modeling with tensorflow/scikit learn. 
- MLOps with tfx/weights & biases/cometml.
- Backend with flask/tensorflow-serving/django. 
- Frontend with javascript/react. 


## Test is Performed On:
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
- How is the data collected
- How frequent the data is collected
- How is the data stored
- Challenges:
    - Structuring the data. Even in one source, sometimes the structure of one category
        of table can be different in two different teams
    - Keeping track of the dimension, shape, inconsistencies, data-type
    - Repetitive checks of each code/function done (there was a time I didn't do it
        and the saved the data was ended up messy. fortunately I managed to make script to fix that)

### Data Cleaning
- Challenges

### Data Transformation / Feature Engineering
- Handling some common things: missing values, skewed/outlier, duplicates, data types
- Numerical variables
- Categorical variables
    - Player Position feature. There are sixteen different positions recorded in fbref, and 
        it's possible for a player to have more than one position. One-hot encoding will make
        the dimension grow by 16x11x2 = 352 if we only consider starters in our model. So
        position embedding was employed.
- Challenges
    - Randomness nature of football

### Feature Selection
- Selection Manual
- Challenges
    - Selecting features is tricky because in football, one's attribute (say, shooting) may or may
        not effect the game depends on either the player's other attributes or the players' teammates
        or opponents.
    - Selecting one additional feature/attribute for a player means multiplying that feature by the number
        of players being accounted for the model.

### Model Creation & Evaluation
- Baseline: Neural Network
- Hyperparameter
- Challenges
    - Deciding on evaluation/performance metric and why
    - Hyperparams tuning
    - 

### Model Deployment & Monitoring
- What's being monitored
- How is the model deployed
    - Website interface
    - API
- Challenges

### Model Re-Training & Model Re-Deployment
- Challenges