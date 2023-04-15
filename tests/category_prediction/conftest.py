import pathlib
from unittest.mock import patch

import pytest


@pytest.fixture(scope='module')
def process_manager():
    from category_prediction.agent import CategoryPrediction

    return CategoryPrediction(
        f'{pathlib.Path(__file__).parent.parent.parent.absolute()}/ai_models/category_prediction/simple_classifier.pkl'
    )
