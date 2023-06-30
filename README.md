# Refactoring Project

Please do not fork this repository, but use this repository as a template for your refactoring project. Make Pull
Requests to your own repository even if you work alone and mark the checkboxes with an `x`, if you are done with a topic
in the pull request message.

## Project for today

The task for today you can find in the [project-for-today.md](./project-for-today.md) file.

## Setup

The necessary libraries are listed in the [requirements.txt](./requirements.txt) file. You can install them with the
following command:

```bash
pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Questions

### Section 1: From Jupyter notebooks to Python programs

* What are the steps you took to complete the project?
    * I created pre-commit hools locally using mypy and black.
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
      section. Currently, the two sections are in two separate folders. 
    * Write tests for the functions in [kc_preprocessing.py](./src/kc_preprocessing.py) and [kc_transformer_pipelines.py](./src/kc_transformer_pipelines.py).
    * Write [kc_preprocessing.py](./src/kc_preprocessing.py) without inheritance.
    * Apply transformation using ColumnsTransformer instead of Pipeline to reduce load of data in memory.
    * Finish refactoring the modeling part of the notebook. 