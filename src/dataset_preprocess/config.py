import numpy as np

COLUMN_SELECTION = [
    'id',
    'neighbourhood_group_cleansed',
    'property_type',
    'room_type',
    'latitude',
    'longitude',
    'accommodates',
    'bathrooms',
    'bedrooms',
    'beds',
    'amenities',
    'price',
]
COLUMN_MAPPING = {'neighbourhood_group_cleansed': 'neighbourhood'}
COLUMN_STRING_TO_CATEGORICAL = {
    'neighbourhood': {"Bronx": 1, "Queens": 2, "Staten Island": 3, "Brooklyn": 4, "Manhattan": 5},
    'room_type': {"Shared room": 1, "Private room": 2, "Entire home/apt": 3, "Hotel room": 4},
}

COLUMNS_STR_TO_NUM = ['price']
MIN_PRICE = 10

CATEGORY_BINS = [10, 90, 180, 400, np.inf]
CATEGORY_LABELS = [0, 1, 2, 3]

AMENITIES = ['TV', 'Internet', 'Air_conditioning', 'Kitchen', 'Heating', 'Wifi', 'Elevator', 'Breakfast']
