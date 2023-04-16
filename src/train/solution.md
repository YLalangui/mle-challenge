# Dataset preprocess

## Introduction

This folder contains necessary code to train a model. The structure is as follows:

- `config.py`: General configuration related to model training.
- `evaluation.py`: Evaluation functions are defined in this script. They are used to evaluate our model: they will create plots and will save scores.
- `train.py`: Training functions are defined in this script such as model training itself or model saving.
- `main.py`: Entrypoint for training. It executes training process by using functions from `evaluation.py` and `train.py` scripts

## How to execute this component

As this component could be more iterative all inputs for this component are saved in `config.py` file. When this component is executed all configuration for training will come from `config.py` (local/remote path dataset, hyperparams...) and model will be trained.

Once pur model has been training all information (metadata) related to that model (hiperparams, evaluation outputs like plots or dataframes, the model itself) will be saved in the same folder following the following structure: `{config.SAVE_MODEL_PATH}/{config.EXPERIMENT_NAME}`. Hence, each experiment will have its own metadata, so that allows us to reproduce again and track a specific experiment.

Here an example:

`$ python train.py`

If config is left as default in `config.py` file then all metadata and artifact will have been saved in /models/experiment1/...

## Tests

To execute tests please refer to `solution.md` at the root of this project

## Documentation

To create documentation (`index.html` file) please refer to `solution.md` at the root of this project

## Comments

This component has been created to be executed locally (metadata and artifact saved locally), but other tools can be used to track experiments like MLflow or Kubeflow pipelines. For that this code has to be refactored to accept these tools and support cloud-based solutions.
