# Category prediction

## Introduction

This folder contains necessary code to inference category based on AirBnB dataset. The structure is as follows:

- `agent`: This agent is the one responsable for calling preprocess, predict and postprocess functions.
- `config`: General configuration related to model inference
- `listing`: ModelClass (pydantic) related to input and output of the inference service
- `preprocess`: Functions related to preprocess functionality used by the agent.

## How model is executed

When model is instantiated it is instantiated as an agent (Class). If we want to do some inference the only thing we have to do is to call the agent (To call the class) and, from that point, the agent will call preprocess, predict and postprocess functions to process the input and give us an output.

To start our server please execute:
```
uvicorn src.predictor:app --host 0.0.0.0 --port 80
```
This way you will have the server up waiting for requests

## Error handlers

In order to be sure that correct data is processed by our inference service we have used pydantic library. In our case fastapi has an integration with pydantic so if any field of the input has not the correct format then pydantic will let us know and fastapi will be able to handle that response. We have used pydantic as well to be sure that the inference service has the correct format.

Apart from that, errors related to fields which have to be converted from str to num (room_type, neighbourhood) have been taken into account.

## Tests

To execute tests please refer to `solution.md` at the root of this project

## Documentation

To create documentation (`index.html` file) please refer to `solution.md` at the root of this project

## Comments

This structure has been selecting keeping in mind that more than one ai model can be implemented in this microservice. So, for example, if a model which predicts price has to be implemented we can add another folder at the root of the project with the name of the model and then follow then same agent-like structure. This way, the only thing we need to add in our `predictor.py` script is the agent related to the new model and call the new agent.
