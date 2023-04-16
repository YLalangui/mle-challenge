# Solution challenge 2 & 3

## Introduction

This part of the challenge can be executed in several ways (we want to be sure that the code works regarding the host O.S., windows, ubuntu...). As we are using docker then every component should work correctly. Let's see how this part can be executed

## Quick way

```
// first of all, docker should be installed in your host

// clone repository in your host
git clone https://github.com/YLalangui/mle-challenge.git
cd mle-challenge
git checkout challenge_2_3

// build docker image
docker build -t challenge_2_3 .

// Execute server
docker run -p 80:80 challenge_2_3
// In your terminal you will see that the server is up

// You can go to you web browser and type 'localhost/ping'
// In the terminal where you executed 'docker run' command you will see this line:
INFO:     172.17.0.1:57332 - "GET /ping HTTP/1.1" 200 OK
// This means the server is up and ready to receive data

// Let's send some data for inference!
// Let's open another terminal and execute the following command
curl -d "{\"id\": 1001, \"accommodates\": 4, \"room_type\": \"Entire home/apt\", \"beds\": 2, \"bedrooms\": 1,  \"bathrooms\": 2, \"neighbourhood\": \"Brooklyn\", \"tv\": 1, \"elevator\": 1, \"internet\": 0, \"latitude\": 40.71383, \"longitude\": -73.9658}" -H "Content-Type: application/json" -X POST http://localhost:80/invocations/

// Yay! You have recieved a response from the inference service! You will see that response in the same tarminal you execute the `curl` command.
// In addition you can take a look at logger messages in the terminal you executed `docker run` command to track server functionalities
```

#### Unit tests

```
cd mle-challenge
git checkout challenge_2_3

// If you are using Windows O.S. it is recommended to execute these commands by using PowerShell
// PD: if you want to execute unit tests you can do it! (change ${pwd} with $(pwd) if you are using a unix-based O.S.)
docker run -v ${pwd}:/app challenge_2_3 sh -c "poetry install; pytest"
```

#### Documentation

There is already a `public` folder with an `index.html` file with the documentation of the code (You can open this html file right now on your favourite browser to take a look at it!). All code related to documentation is already placed in `docs` folder. It was created by using `sphinx` python library. If you change the source code and want to generate new documentation (It can be implemented in a CI/CD pipeline as well) please execute:

```
cd mle-challenge
git checkout challenge_2_3

// If you are using Windows O.S. it is recommended to execute these commands by using PowerShell
//(change ${pwd} with $(pwd) if you are using a unix-based O.S.)
docker run -v ${pwd}:/app challenge_2_3 sh -c "poetry install; sphinx-apidoc -e -M -f -o docs/source src; sphinx-build -b html docs/source/ public"

// At this point you will see that documentation ('public' folder) has been updated
```

## Longer way with explanation

This project was implemented by using VSCode IDE, so it is easy to dive in and test more hidden features.

#### Devcontainer

Devcontainer feature was used to implement and test this code (you can take a look at `.devcontainer` folder). This way I can be sure that if my code works inside a container then I can hand off my project to other collegue. So, if you are using VSCode you can create a container in VSCode environment just installing "Dev container" pluging, going to this repository (cd /path/to/mle-challenge), clicking on bottom-left green button and clicking on "Reopen in container". This way VSCode will create a Docker container by using `.devcontainer/devcontainer.json` and it will lead you inside the container. So every code change inside the container it will be seen in your local host.

IMPORTANT: If you are using a unix-based O.S. please change `USERPROFILE` value in `.devcontainer/devcontainer.json` with `HOME`. In addition, you need to have Docker installed in order to use devcontainer.

Some of the features added in `.devcontainer/devcontainer.json` are:

- Automatically applies "black" & "isort" when you save a file with "ctrl+s" (So your code will be formatted automatically)
- Gitlens installed: You will see the tipycal blamer to see who changed one specific line of code. Apart from this blamer you can apply git commands by using the VSCode UI

#### Poetry

Poetry is a python package manager. It can be used to create virtual environments as well, but due to a Docker container is a virtual environment per se we wont create a virtual environment inside a docker container. So we will use poetry just as a package manager. `poetry.lock` & `pyproject.toml` are the two files related to this tool.

With Poetry and devcontainer you can notice that Dockerfile is not a complex file. In our case we want to have a generic Dockerfile.

#### Documentation

Documentation has been created by using sphinx python library. The `docs` folder is a generic folder which will be used by `sphinx` to create all needed documentation.

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
Once we have explained all folders and script which support our development let's tackle our code structure. Code related to API implementation is placed in `src` folder. Code related to functionality and model management is placed in `category_prediction` folder:

- `src`: There you will find a `predictor.py` which contains our API implementation. It supports `/ping` and `/invocations` functionalities.
- `category_prediction`: This folder contains all code related to our model (Instantiation, management, preprocess, prediction, postprocess...).

If any other model has to be added to this microservice then we can follow this structure: We just need to create another folder (At the same level as `category_prediction`) and implement inside taht folder all functionalities related to this new model. We will need to change then `prediction.py` script to instantiate our model and use it.

For more information about structure inside `category_prediction` or how to execute server inside devcontainer please refer to `solution.md` placed in `category_prediction/solution.md`

#### Gettting response from API locally
At the root of the project there is a `python_post_request.py` script which can be used to send requests to the server if `curl` command does not work.
```
python python_post_request.py
```

#### Conclusion of this Longer way
As we are developing using devcontainer we are actually developing inside a container, so every time we change code it is not necessary to re-build the image and re-run the container, we are actually changing stuff inside the container. So if you execute the server (using devcontainer) and you find an error you just kill the server (ctl+c), change your code and start the server again, you do not need to re-build the image and re-run the container. You only build your image once during you development (or during a hot-fix): When you finish your development.

## Comments

Related to the `ai_models` folder it is not a good practice to save the model inside the repository. In this case model has been saved inside the repository to ease this example implementation. A good practice would be to use a data version control like DVC. Each time this microservice is starting then and external service can be used DVC information in the repository and bring the model from any remote storage (S3, MinIO, GCP...) during microservice setting up. This way, our model (artifact, datasets...) can be versioned and available in a remote storage.
