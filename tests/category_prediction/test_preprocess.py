import fastapi
import pytest

from category_prediction.config import FEATURES_STRING_TO_CATEGORICAL
from category_prediction.listing import ListingInfo
from category_prediction.preprocess import convert_str_to_categorical, select_features


def test_select_features():
    # ARRANGE
    input_model = {
        "id": 1001,
        "accommodates": 4,
        "room_type": "Entire home/apt",
        "beds": 2,
        "bedrooms": 1,
        "bathrooms": 2,
        "neighbourhood": "Brooklyn",
        "tv": 1,
        "elevator": 1,
        "internet": 0,
        "latitude": 40.71383,
        "longitude": -73.9658,
    }
    listing = ListingInfo(**input_model)
    list_features = ['accommodates', 'beds', 'bathrooms']
    expected_dict = {"accommodates": 4, "beds": 2, "bathrooms": 2}

    # ACT
    result_dict = select_features(listing, list_features)

    # ARRANGE
    assert result_dict == expected_dict


def test_convert_str_to_categorical():
    # ARRANGE
    listing = {"accommodates": 4, "room_type": "Entire home/apt", "neighbourhood": "Brooklyn"}
    expected_dict = {"accommodates": 4, "room_type": 3, "neighbourhood": 4}

    # ACT
    result_dict = convert_str_to_categorical(listing, FEATURES_STRING_TO_CATEGORICAL)

    # ARRANGE
    assert result_dict == expected_dict


@pytest.mark.parametrize(
    ('listing'),
    [
        pytest.param(
            {"accommodates": 4, "room_type": "Entire blabla", "neighbourhood": "Brooklyn"},
            id='---- room type error ----',
        ),
        pytest.param(
            {"accommodates": 4, "room_type": "Entire home/apt", "neighbourhood": "Parla"},
            id='---- neighbourhood error ----',
        ),
    ],
)
def test_convert_str_to_categorical_key_error(listing):
    # ACT
    with pytest.raises(fastapi.exceptions.HTTPException):
        convert_str_to_categorical(listing, FEATURES_STRING_TO_CATEGORICAL)
