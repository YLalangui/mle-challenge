from typing import Dict

from fastapi import HTTPException

from category_prediction.listing import ListingInfo


def select_features(listing: ListingInfo, feature_list: list) -> Dict:
    """Selects specific features for model inference
    Args:
        listing: listing for inference
        feature_list: list of features which will take into account to infer
    Returns:
        Dict: Selected features with their values
    """
    selected_features = {}
    for feature in feature_list:
        selected_features[feature] = listing.__getattribute__(feature)
    return selected_features


def convert_str_to_categorical(listing: Dict, features_str_to_cat: Dict) -> Dict:
    """Converts specific features from str to num.
    Args:
        listing: listing to transform
        features_str_to_cat: List of features to transform their values from string to num
    Returns:
        Dict: transformed listing
    """
    for key, value in features_str_to_cat.items():
        try:
            listing[key] = value[listing[key]]
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"{key} field not valid. '{listing[key]}' {key} not supported")

    return listing
