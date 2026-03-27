import duckdb
import pandas as pd
from .lib import fetch_and_rename


ROLES_COLUMNS = {"id": "notion_id", "_dlt_id": "dlt_id"}
ROLES_TITLE_COLUMNS = {"plain_text": "role_title", "_dlt_parent_id": "dlt_parent_id"}


def populate_role_title(
    df_tasks: pd.DataFrame, con: duckdb.DuckDBPyConnection
) -> pd.DataFrame:
    df_roles = fetch_roles(con)
    df_roles_relation = fetch_and_rename(
        "t_ches__properties__r_le_r_esponsable__relation",
        {"id": "notion_role_id", "_dlt_parent_id": "task_dlt_id"},
        con,
    )

    df_with_roles = df_tasks.merge(
        df_roles_relation,
        left_on="dlt_id",
        right_on="task_dlt_id",
        how="left",
    ).merge(
        df_roles,
        left_on="notion_role_id",
        right_on="notion_id",
        how="left",
    )

    # Remove join columns
    return df_with_roles.loc[
        :,
        ~df_with_roles.columns.isin(["task_dlt_id", "notion_role_id", "notion_id"]),
    ]


def fetch_roles(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    df_roles = fetch_and_rename("r_les", ROLES_COLUMNS, con)
    df_role_titles = fetch_and_rename(
        "r_les__properties__r_le__title", ROLES_TITLE_COLUMNS, con
    )
    df_roles = df_roles.merge(
        df_role_titles, left_on="dlt_id", right_on="dlt_parent_id", how="inner"
    )
    return df_roles.loc[:, ["notion_id", "role_title"]]
