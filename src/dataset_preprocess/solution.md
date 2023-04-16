# Dataset preprocess

## Introduction

This folder contains necessary code to preprocess airbnb dataset. The structure is as follows:

- `config.py`: General configuration related to data transformation
- `preprocess.py`: General and specific functions which are used to transform the dataset
- `main.py`: Entrypoint of the component. It executes all data transformation and uses functions defined in `preprocess.py`

## How to execute data transformation

This component can be executed locally or in a Docker container on cloud. As `main.py` is the entrypoint then a Docker image can be created from `dataset_preprocess` folder. In this case, four arguments are needed to execute the entry point:

- `read-csv-path`: local or remote path (S3, MinIO) where component will get dataset from
- `save-csv-path`: local or remote path (S3, MinIO) where component will put/save dataset
- `origin-storage-options`: Needed header authentication (http) to get dataset if remote path is provided
- `dest-storage-options`: Needed header authentication (http) to put/save dataset if remote path is provided

Here an example:

`$ python main.py --read-csv-path /path/to/get/dataset --save-csv-path /path/to/save/dataset`

## Tests

To execute tests please refer to `solution.md` at the root of this project

## Documentation

To create documentation (`index.html` file) please refer to `solution.md` at the root of this project

## Comments

This component has been created to be executed locally, but it can be seen as a dockerized component in order to take part to a data pipeline. It can be contaneirized and be used as a job in Airflow, Stepfunctions (AWS) or even in a Kubeflow pipeline. To do that, a Dockerfile has to be created in `dataset_preprocess` and that image has to be uploaded to a Docker Image repository. That repository has to be reachable by cloud/on-premise orchestrator (Airflow, Stepfunctions, kubeflow pipelines...)
