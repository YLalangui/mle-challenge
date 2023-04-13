import pickle
import shutil

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def split_train_test(df, feature_names, test_size, random_state):
    """Splits dataset into train and test sets

    Args:
        df: dataframe to split
        feature_names: features to take into account during splitting
        test_size: Size of test set
        random_state: Seed for randomness

    Returns:
        tuple: Tuple of X_train, X_test, y_train, y_test
    """
    X = df[feature_names]
    y = df['category']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    return (X_train, X_test, y_train, y_test)


def train_model(X_train, y_train, n_estimators, random_state, class_weight, n_jobs):
    """Trains model

    Args:
        X_train: Feature data for training
        y_train: Objective feature to inference during training
        n_estimators: Number of estimators
        random_state: Seed for randomness
        class_weight: Classes usage strategy during training
        n_jobs: Jobs used during training

    Returns:
        sklearn.ensemble.RandomForestClassifier: Trained model
    """
    clf = RandomForestClassifier(
        n_estimators=n_estimators, random_state=random_state, class_weight=class_weight, n_jobs=n_jobs
    )
    clf.fit(X_train, y_train)

    return clf


def save_model(clf, experiment_path):
    """Saves trained model

    Args:
        clf: Model to save
        experiment_path: Path used to save model
    """
    pickle.dump(clf, open(f'{experiment_path}/simple_classifier.pkl', 'wb'))


def save_config(config_path, experiment_path):
    """Saves config used for model training

    Args:
        experiment_path: Path used to save config
    """
    shutil.copyfile(config_path, f'{experiment_path}/config.py')
