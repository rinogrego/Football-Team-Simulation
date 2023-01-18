# Football 11-vs-11 Simulation

## Motivation
1. I like the idea
2. Wants to code a project of something I like
3. Wants to practice my machine learning engineering skills
4. It's fun (until I reached the data cleaning part, which is 1 day in after I started the project)


## Stack Used
- Python for everything. 
- Scraping is done with beautifulsoup4. 
- Preprocessing with numpy & pandas (considering to switch to polars). 
- Modeling with tensorflow. 
- MLOps with tfx/weights & biases/cometml.
- Backend with flask/tensorflow-serving. 
- Frontend with javascript/react. 


## Test is Performed On:
- When the data is scraped
- When the data is about to be transformed
- After the data is transformed
- After feature engineering
- Before the data is used to train/retrain the model (tfdv)
- Before the model is served