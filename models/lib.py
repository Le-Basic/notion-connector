import duckdb
import pandas as pd
from typing import Dict


def fetch_and_rename(
    table_name: str, columns: Dict[str, str], con: duckdb.DuckDBPyConnection
) -> pd.DataFrame:
    return (
        con.execute(f"SELECT * FROM notion_data.{table_name}")
        .fetchdf()
        .rename(columns=columns)
    ).loc[
        :,
        list(columns.values()),
    ]
