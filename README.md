# Football 11-vs-11 Simulation

<!-- Implement badges: https://shields.io -->

Web application for player-based football match result prediction. User can build custom teams and then try to predict the result of the match between those two teams. Basically, user can predict a result of football match given players with their positions for each team in a match.

Can be used to:

- Find out how a player played in a different position can affect the match result
- Find out the impact of only 1 different player from starting line-up can affect the match result

## Motivation

1. I like the idea
2. Want to code a project of something I like
3. Want to practice my machine learning engineering skills
4. It's fun (until I reached the data cleaning part, which is 1 day in after I started the project)
5. To fill my time

*Being serious*, I am intrigued in creating a machine learning model to predict football match results. And since football match is heavily dependent on not only the team capabilities but also each players abilities and also their role for the team, I wanted to create a model that can predict the match outcome that consider these things and not just overall team capabilites. This is my main motivation for the project. To create a model that can predict a football match result that considers the details such as not only the player's abilities but also where they play.

**I am well aware** that a football match have too many variables that can impact it but I think the challenge of scratching the surface of that problem is fun.

**I am well aware** that this sh\*t can be turned into gambling tool but f\*ck it. I did this for fun and to hone my skills. I think the engineering challenge is good for me to try.

## Limitations

- Biased towards home team
- Not many attribute features were considered during model development
- The model was trained on dataset scrapped from five different leagues, but the league information isn't used when training the model. A good assumption to remember
- **NEED SOOO MANY** data points to make a good model to the point that I think I will never be able to create a good model

## Stack Used

Python for (almost) everything backend. But to be specific:

- Data Scraping: Beautifulsoup4, Pandas
- Data Transformation/Preprocessing: Numpy, Pandas
- Modeling: Tensorflow/Keras
- Backend: Django & djangorestframework
- Frontend: plain JavaScript, CSS with bootstrap

## Project Structure

Project structure manually created following [cookiecutter-data-science](https://drivendata.github.io/cookiecutter-data-science/#directory-structure) guide.

<!-- Insert ilustrasi project structure  -->

## Overall Challenges Faced

- Properly modelling the problem
  - Need to shuffle player input positions so that the model can see that input location isn't correlated with player position
  - Normalizing the attributes used as inputs
  - Determining the 'properness' of the team's position composition
  - Determining the 'properness' of the player's attributes and their position
- Creating separate logic for backend and frontend
  - backend: djangorestframework
  - frontend: React
- Maintaining data science end-to-end pipeline

## How I approach the Project

I tried to imitate how ML in industry (probably) works. I divided the project into 4 different works. This enables me to focus on 1 part without worrying it would break the other parts.

- Acquiring data
  - Create a script to automatically scrap and save the data to data folder. Script is run manually (no job scheduler)

- Transforming data and modelling
  - Transforming the acquired data and then using it for modelling is done in notebook environment.

- Deployment (backend)
  - Deployed in two ways, first is via django templating HTML, and second is via djangorestframework for API call.

- Deployment (frontend)
  - Currently done via django templating. But plans to implement it with React.

## What I've Learnt

- Data Acquisition
  - Working with pandas .loc and .iloc
  - Working with multi-index pandas dataframe
  - Learnt how useful it is to create a script to automate data collection process
- Data Transformation
  - Familiarizing myself creating a pipeline for transforming data acquired from previous script for machine learning purpose
  - Mapping from raw data to data format that meets the requirement for modelling
- Modeling
  - Getting more proficient in Tensorflow/Keras. Learnt how to implement complex architecture with Keras
  - Getting comfortable working with structured data using Tensorflow/Keras
- Deployment
  - Learnt how to serve ML app with djangorestframework
- Overall
  - Conscious about how useful it is to differentiate directories/storages for data, features, and models

<!-- 
## Images/Illustration

- Workflow from data acquisition to model deployment
- About data acquisition
- About data transformation
- About separated workflow for
  - Data acquisition/engineering
  - Modelling
  - Deployment/Web development
    - Frontend
    - Backend
- Model architecture plot -->
