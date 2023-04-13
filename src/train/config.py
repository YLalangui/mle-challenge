# Training params
EXPERIMENT_NAME = 'experiment1'
FEATURE_NAMES = ['neighbourhood', 'room_type', 'accommodates', 'bathrooms', 'bedrooms']
READ_CSV_PATH = '/app/data/processed/processed_listings.csv'
SAVE_MODEL_PATH = '/app/models'
EVALUATE_MODEL = True
CONFIG_PATH = '/app/src/train/config.py'

# Split train/test
RANDOM_STATE_SPLIT = 1
TEST_SIZE = 0.15

# Hyperparams
N_ESTIMATORS = 300
RANDOM_STATE_TRAIN = 0
CLASS_WEIGHT = 'balanced'
N_JOBS = 5
