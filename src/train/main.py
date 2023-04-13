import os

import pandas as pd
from config import (
    CLASS_WEIGHT,
    EVALUATE_MODEL,
    EXPERIMENT_NAME,
    FEATURE_NAMES,
    N_ESTIMATORS,
    N_JOBS,
    RANDOM_STATE_SPLIT,
    RANDOM_STATE_TRAIN,
    READ_CSV_PATH,
    SAVE_MODEL_PATH,
    TEST_SIZE,
    CONFIG_PATH
)
from evaluation import (
    save_dataframe_scores,
    save_plot_classification_report,
    save_plot_confusion_matrix,
    save_plot_feature_importance,
)
from train import save_config, save_model, split_train_test, train_model


def train():
    """Trains a model and save artifacts related to that model."""

    df = pd.read_csv(READ_CSV_PATH, index_col=0)

    X_train, X_test, y_train, y_test = split_train_test(df, FEATURE_NAMES, TEST_SIZE, RANDOM_STATE_SPLIT)
    clf = train_model(X_train, y_train, N_ESTIMATORS, RANDOM_STATE_TRAIN, CLASS_WEIGHT, N_JOBS)

    if EVALUATE_MODEL:
        experiment_path = f'{SAVE_MODEL_PATH}/{EXPERIMENT_NAME}'
        os.makedirs(experiment_path, exist_ok=True)

        save_dataframe_scores(clf, X_test, y_test, experiment_path)
        save_plot_feature_importance(clf, X_train, experiment_path)

        y_pred = clf.predict(X_test)
        save_plot_confusion_matrix(y_test, y_pred, experiment_path)
        save_plot_classification_report(y_test, y_pred, experiment_path)

    save_model(clf, experiment_path)
    save_config(CONFIG_PATH, experiment_path)


if __name__ == "__main__":
    train()
