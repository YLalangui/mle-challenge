import logging
import pickle
from typing import List

from category_prediction.config import CATEGORIES, FEATURES_STRING_TO_CATEGORICAL
from category_prediction.listing import ListingInfo, ServiceResponse
from category_prediction.preprocess import convert_str_to_categorical, select_features

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CategoryPrediction:
    """Category prediction based on AirBnb dataset"""

    __version__ = "0.0.1"

    def __init__(self, model_path):
        logger.info("Loading model...")

        with open(model_path, "rb") as f:
            pickle_info = pickle.load(f)

        self.model = pickle_info
        logger.info("Model loaded!")

    def __call__(self, listing: ListingInfo) -> ServiceResponse:
        """Main method to call each function to process the dataframe image and to output category.

        Args:
            listing: List of house features for inference

        Returns:
            ServiceResponse: Response from the service
        """
        logger.info("Preprocessing in progress...")
        features = self.preprocess(listing)

        logger.info("Prediction in progress...")
        category = self.predict(features)

        logger.info("Postprocessing in progress...")
        response = self.postprocess(listing.id, category)

        logger.info("Sending final response!")
        return response

    def preprocess(self, listing: ListingInfo) -> List:
        """This method preprocesses input listing to inference.

        Args:
            listing: listing which contains information of the house

        Returns:
            List: Correct format of features for inference
        """

        selected_features_listing = select_features(listing, list(self.model.feature_names_in_))
        str_to_cat_listing = convert_str_to_categorical(selected_features_listing, FEATURES_STRING_TO_CATEGORICAL)

        features = [value for _, value in str_to_cat_listing.items()]
        return features

    def predict(self, features: List) -> int:
        """Predicts category

        Args:
            features: List of features to inference

        Returns:
            int: Category obtained based of listing information
        """
        category = int(self.model.predict([features])[0])
        return category

    def postprocess(self, listing_id: int, category: int) -> ServiceResponse:
        """Postprocesses result given by model to create a correct server response

        Args:
            listing_id: Id of the listing
            category: category obtained from model inference

        Returns:
            ServiceResponse: Server response in a correct format

        """
        return ServiceResponse(**{'id': listing_id, "price_category": CATEGORIES[category]})
