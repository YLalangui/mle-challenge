# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

import logging
import pathlib
import time

from fastapi import FastAPI, Response

from category_prediction.agent import CategoryPrediction
from category_prediction.listing import ListingInfo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# The flask app for serving predictions
app = FastAPI()

category_prediction_model = CategoryPrediction(
    f'{pathlib.Path(__file__).parent.parent.absolute()}/ai_models/category_prediction/simple_classifier.pkl'
)


@app.get("/ping", status_code=200)
def ping():
    return Response(content="\n", media_type="application/json")


@app.post("/invocations/")
async def predict(data: ListingInfo):
    start = time.time()
    prediction = category_prediction_model(data)
    end = time.time()
    logger.info(f"Model execution time: {round(end - start, 2)}s")
    return prediction
