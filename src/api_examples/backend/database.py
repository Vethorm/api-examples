# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter

from typing import Optional

import pandas as pd
import duckdb
from pathlib import Path

from loguru import logger


def create_data_folder():
    data_folder = Path("./data")
    if not data_folder.exists():
        logger.info(f"Setting up data folder at {data_folder}")
        data_folder.mkdir()
    else:
        logger.info(f"Data folder found at {data_folder}")


class USAHousing:
    def __init__(self, table: Optional[str] = "usa_housing"):
        db_file = f"./data/{table}.duckdb"
        self.table = table

        create_data_folder()

        if not Path(db_file).exists():
            self._initialize_db(table)

        self.conn = duckdb.connect(f"./data/{table}.duckdb", read_only=True)

    def _initialize_db(self, table):
        # Set the path to the file you'd like to load
        file_path = "usa_housing_kaggle.csv"

        # Load the latest version
        usa_housing_dataset = kagglehub.load_dataset(
            KaggleDatasetAdapter.PANDAS,
            "arnavgupta1205/usa-housing-dataset",
            file_path,
        )

        with duckdb.connect(f"./data/{table}.duckdb") as db:
            db.sql(f"CREATE TABLE {table} AS SELECT * FROM usa_housing_dataset")

    def stats(self) -> dict[str, str]:
        with self.conn.cursor() as cursor:
            result = cursor.sql(f"SELECT COUNT(*) as total_rows FROM {self.table}").pl()
            return result.to_dicts()[0]

    def metadata(self):
        with self.conn.cursor() as cursor:
            result = cursor.sql(f"SELECT * FROM {self.table} LIMIT 1").pl()
            columns = list(result.to_dict().keys())
            metadata = {}
            for column in columns:
                result = cursor.sql(
                    f"SELECT MAX({column}) AS max, MIN({column}) AS min FROM {self.table}"
                ).pl()
                result = result.to_dicts()
                metadata[column] = {"max": result[0]["max"], "min": result[0]["min"]}
            return metadata


db = USAHousing()
