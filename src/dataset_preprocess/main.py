import json
import os
from pathlib import Path
from typing import NoReturn

import click
import pandas as pd
from config import (
    AMENITIES,
    CATEGORY_BINS,
    CATEGORY_LABELS,
    COLUMN_MAPPING,
    COLUMN_SELECTION,
    COLUMN_STRING_TO_CATEGORICAL,
    COLUMNS_STR_TO_NUM,
    MIN_PRICE,
)
from preprocess import (
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


@click.command()
@click.option('--read-csv-path', type=str, required=True)
@click.option('--save-csv-path', type=str, required=True)
@click.option('--origin-storage-options', type=str, required=False, default='{}')
@click.option('--dest-storage-options', type=str, required=False, default='{}')
def preprocess_dataset(
    read_csv_path: str, save_csv_path: str, origin_storage_options: str, dest_storage_options: str
) -> NoReturn:
    """Preprocess a csv dataset and save it.

    Args:
        read_csv_path: dataset path which will be read
        save_csv_path: path to save the preprocessed dataset
    """
    os.makedirs(Path(save_csv_path).parent.absolute(), exist_ok=True)
    df = pd.read_csv(read_csv_path, storage_options=json.loads(origin_storage_options))

    # Dataset preprocess
    df = create_bathroom_column(df)

    df = select_columns(df, columns=COLUMN_SELECTION)
    df = rename_columns(df, column_mapping=COLUMN_MAPPING)
    df = convert_string_num_column(df, columns=COLUMNS_STR_TO_NUM)

    df = filter_by_price(df, min_price=MIN_PRICE)
    df = create_category_column(df, bins=CATEGORY_BINS, labels=CATEGORY_LABELS)
    df = create_amenities_columns(df, amenities=AMENITIES)

    df = convert_string_to_categorical(df, COLUMN_STRING_TO_CATEGORICAL)

    df = remove_nan_rows(df)

    df.to_csv(save_csv_path, storage_options=json.loads(dest_storage_options))


if __name__ == "__main__":
    preprocess_dataset()
