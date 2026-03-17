import pandas as pd
import duckdb
from .lib import fetch_and_rename


def populate_accountables(
    df_tasks: pd.DataFrame, con: duckdb.DuckDBPyConnection
) -> pd.DataFrame:
    df_accountable_relations = fetch_and_rename(
        "t_ches__properties___r_esponsable__people",
        {
            "_dlt_parent_id": "task_dlt_id",
            "name": "responsable",
        },
        con,
    )

    df_tasks_with_people = df_tasks.merge(
        df_accountable_relations, left_on="dlt_id", right_on="task_dlt_id", how="left"
    )

    # Remove join columns
    return df_tasks_with_people.loc[
        :,
        ~df_tasks_with_people.columns.isin(["task_dlt_id"]),
    ]
