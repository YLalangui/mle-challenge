from unittest.mock import patch

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.train.train import split_train_test, train_model, save_model


@patch('src.train.train.train_test_split')
def test_split_train_test(mock_train_test_split):
    # ARRANGE
    d = {'field1': [1], 'category': [1]}
    df = pd.DataFrame(data=d)
    feature_names = ['field1']
    test_size = 0.1
    random_state = 0
    mock_train_test_split_return_value = (
        pd.DataFrame({'field1': [1], 'category': [1]}),
        pd.DataFrame({'field1': [1], 'category': [1]}),
        pd.DataFrame({'field1': [1], 'category': [1]}),
        pd.DataFrame({'field1': [1], 'category': [1]}),
    )
    mock_train_test_split.return_value = mock_train_test_split_return_value

    # ACT
    X_train, X_test, y_train, y_test = split_train_test(df, feature_names, test_size, random_state)

    # ASSERT
    assert (X_train, X_test, y_train, y_test) == mock_train_test_split_return_value
    assert mock_train_test_split.called


@patch('src.train.train.RandomForestClassifier')
def test_train_model(mock_randomforest_fit):
    # ARRANGE
    X_train = pd.DataFrame({'field1': [1], 'category': [1]})
    y_train = pd.DataFrame({'field1': [1], 'category': [1]})
    n_estimators = 1
    random_state = 1
    class_weight = 'hi'
    n_jobs = 1

    # ACT
    clf = train_model(X_train, y_train, n_estimators, random_state, class_weight, n_jobs)

    # ASSERT
    assert clf.fit.called
    assert mock_randomforest_fit.called
