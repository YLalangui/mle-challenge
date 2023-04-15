from unittest.mock import patch

from sklearn.ensemble import RandomForestClassifier

from category_prediction.listing import ListingInfo

from category_prediction.config import CATEGORIES


def test_init(process_manager):
    assert isinstance(process_manager.model, RandomForestClassifier)


@patch('category_prediction.agent.CategoryPrediction.preprocess', autospec=True)
@patch('category_prediction.agent.CategoryPrediction.predict', autospec=True)
@patch('category_prediction.agent.CategoryPrediction.postprocess', autospec=True)
def test_call(mock_postprocess, mock_predict, mock_preprocess, process_manager):
    # ASSERT
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

    # ACT
    process_manager(listing)

    # ASSERT
    assert mock_preprocess.called
    assert mock_predict.called
    assert mock_postprocess.called


@patch('category_prediction.agent.convert_str_to_categorical')
@patch('category_prediction.agent.select_features')
def test_preprocess(mock_select_features, mock_convert_str_to_categorical, process_manager):
    # ASSERT
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

    mock_select_features.return_value = {
        "neighbourhood": "Brooklyn",
        "bedrooms": 1,
        "bathrooms": 2,
        "room_type": "Entire home/apt",
        "accommodates": 4,
    }
    mock_convert_str_to_categorical.return_value = {
        "neighbourhood": 2,
        "bedrooms": 1,
        "bathrooms": 2,
        "room_type": 1,
        "accommodates": 4,
    }
    expected_list = [2, 1, 2, 1, 4]

    # ACT
    result_list = process_manager.preprocess(listing)

    # ASSERT
    assert result_list == expected_list

def test_predict(process_manager):
    # ASSERT
    example_list = [1, 2, 3, 4, 5]
    expected_category = 0

    # ACT
    result_category = process_manager.predict(example_list)

    # ASSERT
    assert expected_category == result_category

def test_postprocess(process_manager):
    # ASSERT
    example_listing_id = 1
    example_category = 0

    # ACT
    result_category = process_manager.postprocess(example_listing_id, example_category)

    # ASSERT
    assert result_category.id == example_listing_id
    assert result_category.price_category == CATEGORIES[example_category]
