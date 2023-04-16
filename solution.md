# Solution challenge 1

## Introduction

This part of the challenge can be executed in several ways (we want to be sure that the code works regarding the host O.S., windows, ubuntu...). As we are using docker then every component (dataset_preprocess & train) should work correctly. Let's see how this part can be executed

## Quick way (dataset_preprocessing, train, unit tests and documentation)

#### Dataset_preprocessing & train
```
// first of all, docker should be installed in your host

// clone repository in your host
git clone https://github.com/YLalangui/mle-challenge.git
cd mle-challenge
git checkout challenge_1

// If you navigate a little bit through the repository you could see there is no `data/processed` folder (just data/raw/listings.csv file) nor `models` folder. We will populate these two folders with the `data_preprocess` component and `train` component.

// build docker image
docker build -t challenge_1 .

// Execute data_preprocess component (change ${pwd} with $(pwd) if you are using a unix-based O.S.)
docker run -v ${pwd}:/app challenge_1 python /app/src/dataset_preprocess/main.py --read-csv-path /app/data/raw/listings.csv --save-csv-path /app/data/processed/processed_listings.csv

// At this point data/processed/processed_listings.csv has been created. We have proccesed our dataset! Now let's train our model
// (change ${pwd} with $(pwd) if you are using a unix-based O.S.)
docker run -v ${pwd}:/app challenge_1 python /app/src/train/main.py

// A new `models/experiment1` has been created. Inside that folder you will found the trained model, evaluation features (plots, csv...) en the config file used for its training.

// Congrats! We have preprocessed our dataset and train our first model using docker and put results in our local machine!
```

#### Unit tests
```
// PD: if you want to execute unit tests you can do it! (change ${pwd} with $(pwd) if you are using a unix-based O.S.)
docker run -v ${pwd}:/app challenge_1 sh -c "poetry install; pytest"
```

#### Documentation

There is already a `public` folder with an `index.html` file with the documentation of the code (You can open this html file right now on your favourite browser to take a look at it!). All code related to documentation is already placed in `docs` folder. It was created by using `sphinx` python library. If you change the source code and want to generate new documentation (It can be implemented in a CI/CD pipeline as well) please execute:

```
//(change ${pwd} with $(pwd) if you are using a unix-based O.S.)
docker run -v ${pwd}:/app challenge_1 sh -c "poetry install; sphinx-apidoc -e -M -f -o docs/source src; sphinx-build -b html docs/source/ public"

// At this point you will see that documentation ('public' folder) has been updated
```
#### Conclusion of this Quick way

As we could see we have containarized all components, so all of them can be take part of a training pipeline (In case of dataset_preprocess & train for example in a kubeflow pipeline. Interesting if we want to train our model automatically) or CI/CD pipeline (In case of unit tests and documentation).
It wasn't part of this challenge but the last step in a CI/CD pipeline or in a training pipeline could be to have a deployment stage in which we can deploy our model in a cloud or on-premise infrastructure, so Infrastructure as Code is really important as well in order to support our model deployment.

## Longer way with explanation

This project was implemented by using VSCode IDE, so it is easy to dive in and test more hidden features.

#### Devcontainer

Devcontainer feature was used to implement and test this code (you can take a look at `.devcontainer` folder). This way I can be sure that if my code works inside a container then I can hand off my project to other collegue. So, if you are using VSCode you can create a container in VSCode environment just installing "Dev container" pluging, going to this repository (cd /path/to/mle-challenge), clicking on bottom-left green button and clicking on "Reopen in container". This way VSCode will create a Docker container by using `.devcontainer/devcontainer.json` and it will lead you inside the container. So every code change inside the container it will be seen in your local host.

IMPORTANT: If you are using a unix-based O.S. please change `USERPROFILE` value in `.devcontainer/devcontainer.json` with `HOME`. In addition, you need to have Docker installed in order to use devcontainer.

Some of the features added in `.devcontainer/devcontainer.json` are:

- Automatically applies "black" & "isort" when you save a file with "ctrl+s" (So your code will be formatted automatically)
- Gitlens installed: You will see the tipycal blamer to see who changed one specific line of code and you can apply git commands by using the VSCode UI

#### Poetry

Poetry is a python package manager. It can be used to create virtual environments as well, but due to a Docker container is a virtual environment per se we wont create a virtual environment inside a docker container. So we will use poetry just as a package manager. `poetry.lock` & `pyproject.toml` are the two files related to this tool.

With Poetry and devcontainer you can notice that Dockerfile is not a complex file. In our case we want to have a generic dockerfile.

#### Documentation
Documentation has been created by using `sphinx` python library. The `docs` folder is a generic folder which will be used by `sphinx` to create all needed documentation.

If you are using devcontainer you can re-create documentation executing:
```
cd /app
sphinx-apidoc -e -M -f -o docs/source src
sphinx-build -b html docs/source/ public
```
`public` folder will be created/updated with documentation which can be uploaded to a web server (i.e. Gitlab Pages)

#### Tests

All tests are placed in `tests` folder. If you are inside devcontainer you can execute tests:
```
cd /app
pytest
```
You will see test coverage, which is configured by using `setup.cfg` file.

#### Code structure

Once we have explained all folders and script which support our development let's tackle our code structure. All code related to this challenge is placed in `src` folder. There you will find two folders:

- `dataset_preprocess`: All code related to dataset preprocessing is placed in this folder
- `train`: All code related to training is placed in this folder

In each folder you will find a `solution.md` file, so for more information about code structure please refer to these `solution.md` files.

#### Conclusion of this Longer way
If we can use devcontainer with all this configuration (poetry, Dockerfile, devcontainer.json, unittest, documentation, code formatting) it is easy to create reproducible projects and it can be easy to maintain code. A Data Scientist can execute a lot of experiments just by changing the config files and re-executing these components following the `solution.md` files. Furthermore, a Data Scientist do not have to worry about code formatting, containarization or package managing, it is already implemented in the repository so the Data Scientist can be focused on data and model development.
