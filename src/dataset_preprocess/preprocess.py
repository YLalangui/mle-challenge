from typing import Dict, List

import numpy as np
import pandas as pd


def create_bathroom_column(df: pd.DataFrame) -> pd.DataFrame:
    """Creates bathroom column from bathroom_text column.

    Args:
        df: dataframe to transform

    Returns:
        pd.DataFrame: transformed dataframe
    """

    def num_bathroom_from_text(text):
        try:
            if isinstance(text, str):
                bath_num = text.split(" ")[0]
                return float(bath_num)
            else:
                return np.NaN
        except ValueError:
            return np.NaN

    df['bathrooms'] = df['bathrooms_text'].apply(num_bathroom_from_text)

    return df


def select_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Selects specific columns in a dataframe.

    Args:
        df: dataframe to transform
        columns: List of columns to select in a dataframe

    Returns:
        pd.DataFrame: transformed dataframe
    """
    df = df[columns].copy()
    return df


def rename_columns(df: pd.DataFrame, column_mapping: Dict[str, str]) -> pd.DataFrame:
    """Renames columns in a dataframe.

    Args:
        df: dataframe to transform
        column_mapping: Dictionary which consists of old_name: new_name

    Returns:
        pd.DataFrame: transformed dataframe
    """
    for key, value in column_mapping.items():
        df = df.rename(columns={key: value})
    return df


def remove_nan_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Removes rows which contains any NaN value.

    Args:
        df: dataframe to transform

    Returns:
        pd.DataFrame: transformed dataframe
    """
    df = df.dropna(axis=0)
    return df


def convert_string_num_column(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Removes rows which contains any NaN value.

    Args:
        df: dataframe to transform
        columns: List of columns to transform their values from string to num

    Returns:
        pd.DataFrame: transformed dataframe
    """
    for column in columns:
        df[column] = df[column].str.extract(r"(\d+).")
        df[column] = df[column].astype(int)
    return df


def filter_by_price(df: pd.DataFrame, min_price: int) -> pd.DataFrame:
    """Filters dataframe rows based on price.

    Args:
        df: dataframe to transform
        min_price: Min price to take into account while filtering

    Returns:
        pd.DataFrame: transformed dataframe
    """
    df = df[df['price'] >= min_price]
    return df


def create_category_column(df: pd.DataFrame, bins: List, labels: List[int]) -> pd.DataFrame:
    """Creates category column based on price column.

    Args:
        df: dataframe to transform
        bins: List of thresholds to create bins
        labels: List of labels assigned to each bin (in order)

    Returns:
        pd.DataFrame: transformed dataframe
    """
    df['category'] = pd.cut(df['price'], bins=bins, labels=labels)
    return df


def create_amenities_columns(df: pd.DataFrame, amenities: List[str]) -> pd.DataFrame:
    """Creates different amenities columns based on amenities column. It removes amenities column itself

    Args:
        df: dataframe to transform
        amenities: List of amenities used to create new columns

    Returns:
        pd.DataFrame: transformed dataframe
    """
    for amenity in amenities:
        df[amenity] = df['amenities'].str.contains(amenity)
        df[amenity] = df[amenity].astype(int)

    df = df.drop('amenities', axis=1)
    return df


def convert_string_to_categorical(df: pd.DataFrame, column_string_to_categorical: Dict[str, Dict]) -> pd.DataFrame:
    """Converts column values from string to categorical

    Args:
        df: dataframe to transform
        column_string_to_categorical: Dict of Dicts in which main key is the name of the colum and the value contains mapping Dicts

    Returns:
        pd.DataFrame: transformed dataframe
    """
    for key, value in column_string_to_categorical.items():
        df[key] = df[key].map(value)

    return df
