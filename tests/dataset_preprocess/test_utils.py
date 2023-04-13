import numpy as np
import pandas as pd
import pytest

from src.dataset_preprocess.preprocess import (
    convert_string_num_column,
    convert_string_to_categorical,
    create_amenities_columns,
    create_bathroom_column,
    create_category_column,
    filter_by_price,
    remove_nan_rows,
    rename_columns,
    select_columns,
)


@pytest.mark.parametrize(
    ('bathrooms_text', 'bathroom_expected'),
    [
        pytest.param(['1 bath', '1 shared bath', '2.5 baths'], [1, 1, 2.5], id='---- Normal case ----'),
        pytest.param(['1 bath', 'shared bath', '2.5 baths'], [1, np.NaN, 2.5], id='---- With NaN ----'),
    ],
)
def test_create_bathroom_column(bathrooms_text, bathroom_expected):
    # ARRANGE
    d = {'bathrooms_text': bathrooms_text}
    df = pd.DataFrame(data=d)
    bathroom_expected = bathroom_expected

    # ACT
    df_new = create_bathroom_column(df)

    # ASSERT
    bathroom_list = df_new['bathrooms'].to_list()
    np.testing.assert_equal(bathroom_list, bathroom_expected)


def test_select_columns():
    # ARRANGE
    d = {'field_1': [], 'field_2': [], 'field_3': [], 'field_4': []}
    df = pd.DataFrame(data=d)
    columns = ['field_1', 'field_3']

    # ACT
    df_new = select_columns(df, columns)

    # ASSERT
    new_columns = df_new.columns.to_list()
    assert new_columns == columns


def test_rename_columns():
    # ARRANGE
    d = {'field_1': [], 'field_2': [], 'field_3': [], 'field_4': []}
    df = pd.DataFrame(data=d)
    column_mapping = {'field_3': 'field_31', 'field_4': 'field_41'}

    expected_columns = ['field_1', 'field_2', 'field_31', 'field_41']

    # ACT
    df_new = rename_columns(df, column_mapping)

    # ASSERT
    new_columns = df_new.columns.to_list()
    assert new_columns == expected_columns


def test_remove_nan_rows():
    # ARRANGE
    d = {'field_1': [1, 2, 3, 4], 'field_2': [4, np.NaN, 6, 6], 'field_3': [7, 8, 9, 7], 'field_4': [np.NaN, 11, 12, 1]}
    df = pd.DataFrame(data=d)

    # ACT
    df_new = remove_nan_rows(df)

    # ASSERT
    assert df_new.isnull().values.any() == False
    assert df_new.shape == (2, 4)


def test_convert_string_num_column():
    # ARRANGE
    d = {'field_1': ['1.4', '2.4', '5.6'], 'field_2': [5.3, 3.2, 5.2], 'field_3': ['5.3', '3.2', '5.2']}
    df = pd.DataFrame(data=d)
    columns_to_transform = ['field_1', 'field_3']

    # ACT
    df_new = convert_string_num_column(df, columns_to_transform)

    # ASSERT
    for column in columns_to_transform:
        assert df_new[column].dtype == int


def test_filter_by_price():
    # ARRANGE
    d = {'price': [10, 20, 50], 'field_2': ['a', 'b', 'c']}
    df = pd.DataFrame(data=d)
    min_price = 20

    d_expected = {'price': [20, 50], 'field_2': ['b', 'c']}
    df_expected = pd.DataFrame(data=d_expected)

    # ACT
    df_new = filter_by_price(df, min_price)

    # ASSERT
    df_new = df_new.reset_index(drop=True)
    pd.testing.assert_frame_equal(df_new, df_expected)


def test_create_category_column():
    # ARRANGE
    d = {'price': [15, 20, 50, 100, 150]}
    df = pd.DataFrame(data=d)
    bins = [10, 30, 110, np.inf]
    labels = [0, 1, 2]
    categories_expected = [0, 0, 1, 1, 2]

    # ACT
    df_new = create_category_column(df, bins, labels)

    # ASSERT
    categories = df_new['category'].to_list()
    assert categories == categories_expected


def test_create_amenities_columns():
    # ARRANGE
    d = {'amenities': ["['TV', 'Internet']", "['Air_conditioning', 'Kitchen']"]}
    df = pd.DataFrame(data=d)
    amenities = ['TV', 'Internet', 'Air_conditioning', 'Kitchen']

    d_expected = {
        'TV': [1, 0],
        'Internet': [1, 0],
        'Air_conditioning': [0, 1],
        'Kitchen': [0, 1],
    }
    df_expected = pd.DataFrame(data=d_expected)

    # ACT
    df_new = create_amenities_columns(df, amenities)

    # ASSERT
    pd.testing.assert_frame_equal(df_new, df_expected)


def test_convert_string_to_categorical():
    # ARRANGE
    d = {'field_1': ['value1', 'value2', 'value3'], 'field_2': ['value4', 'value5', 'value6']}
    df = pd.DataFrame(data=d)
    column_string_to_categorical = {
        'field_1': {'value1': 1, 'value2': 2, 'value3': 3},
        'field_2': {'value4': 4, 'value5': 5, 'value6': 6},
    }

    d_expected = {'field_1': [1, 2, 3], 'field_2': [4, 5, 6]}
    df_expected = pd.DataFrame(data=d_expected)

    # ACT
    df_new = convert_string_to_categorical(df, column_string_to_categorical)

    # ASSERT
    pd.testing.assert_frame_equal(df_new, df_expected)
