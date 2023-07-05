## Intro:


This repository contains the code for the First Week project completed during the [Machine Learning Engineering](https://www.neuefische.de/en/bootcamp/machine-learning-engineering) bootcamp at [NeueFische school](https://www.neuefische.de/en). In the first week, we focused on topics such as refactoring Jupyter Notebooks into object-oriented programming (OOP) programs using Python. The curriculum also covered Pydantic, Feature Engineering, Unit and Integration testing, as well as Docker, FastAPI, and an introduction to Google Cloud Platform (GCP).


## Tasks
You have a jupyter notebook [King-County.ipynb](./King-County.ipynb), with some EDA, Data cleaning, Feature Engineering and some ML models. The necessary libraries are listed in the [requirements.txt](./requirements.txt) file. You will have to do the following:

- Refactor the code into python files 
- Build a pipeline for the data cleaning, feature engineering.
- Build a FastAPI app, that allows you to Create, Read, Update, and Delete houses to/from a database.
- Create a Dockerfile for the app.
- Run the app in a docker container.

## Setup

The data is in the [data](./data) folder.

The necessary libraries are listed in the [requirements.txt](./requirements.txt) file. You can install them with the following command:

```bash
pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## How to run
### 1. Refactoring:
```bash
cd src
python main.py
```

### 2. FastAPI and Docker:
```bash
cd fastapi_docker
docker-compose up --build
```

Now you can open the FastAPI app in your browser at http://localhost:8000/docs.

#### Tests for FastAPI app:
```bash
cd fastapi_docker
docker-compose run --rm app sh -c "python -m pytest -v -s"
```

## Questions
### Section 1: Refactoring [From Jupyter notebooks to Python programs] (in [src](./src) folder)

* What are the steps you took to complete the project?
    * I created pre-commit hooks locally using mypy and black.
    * I extracted the functions from the notebook and put them in a python file
      in [kc_refactoring.py](./src/kc_refactoring.py).
    * I used the functions in as sklearn transformers classes in [kc_preprocessing.py](./src/kc_preprocessing.py).
    * I used the transformers in a sklearn pipeline in [kc_transformer_pipelines.py](./src/kc_transformer_pipelines.py).
    * I showcase using the pipeline in [main.py](./src/main.py)


* What are the challenges you faced?
    * Deciding on whether to call the functions from [kc_refactoring.py](./src/kc_refactoring.py) or write them inside
      the classes in [kc_preprocessing.py](./src/kc_preprocessing.py).


* What are the things you would do differently if you had more time?
    * Improve structure of the files in order to allow integration between the refactoring section and the API/Docker
      section. Currently, the two sections are independent of each other. 
    * Write tests for the functions in [kc_preprocessing.py](./src/kc_preprocessing.py) and [kc_transformer_pipelines.py](./src/kc_transformer_pipelines.py).
    * Write [kc_preprocessing.py](./src/kc_preprocessing.py) without inheritance.
    * Apply transformation using ColumnsTransformer instead of Pipeline to reduce load of data in memory.
    * Finish refactoring the modeling part of the notebook. 

### Section 2: FastAPI and Docker (in [fastapi_docker](./fastapi_docker) folder)
* What are the steps you took to complete the project?
    * Build a FastAPI app, that allows to Create, Read, Update, and Delete houses to/from a database. Found in [./fastapi_docker/app/main.py](./fastapi_docker/app/main.py).
    * Create a Dockerfile and a Docker compose for the app. Found in [./fastapi_docker/Dockerfile](./fastapi_docker/Dockerfile) and [./fastapi_docker/docker-compose.yml](./fastapi_docker/docker-compose.yml). 
    * Wrote tests for the CRUD system, they run inside the docker container. Found in [./fastapi_docker/tests/test_app.py](./fastapi_docker/tests/test_app.py).
    
 
* What are the challenges you faced?
  * Aligning the names of the containers and database.

  
* What are the things you would do differently if you had more time? 
  * Automatically upload csv file to database and run the pipeline.
  * Creating a call for a prediction model.

