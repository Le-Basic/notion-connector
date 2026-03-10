import duckdb
import pandas as pd
from typing import Dict

TASKS_COLUMNS = {
    "_dlt_id": "dlt_id",
    "id": "notion_task_id",
    "url": "notion_task_url",
    "properties__niveau_de_t_che__formula__string": "notion_task_level",
    "properties__etat__status__name": "notion_task_status",
    "properties__p_riode__date__start": "notion_task_start_date",
    "properties__p_riode__date__end": "notion_task_end_date",
    "properties__jours_pass_s__number": "notion_task_days_passed",
    "properties__jours_allou_s__number": "notion_task_days_allocated",
}


def create_models() -> None:
    con = duckdb.connect("notion.duckdb")

    df_tasks = fetch_and_rename("t_ches", TASKS_COLUMNS, con)

    df_roles = fetch_roles(con)
    df_roles_relation = fetch_and_rename(
        "t_ches__properties__r_le_r_esponsable__relation",
        {"id": "notion_role_id", "_dlt_parent_id": "task_dlt_id"},
        con,
    )
    df_tasks = df_tasks.merge(
        df_roles_relation.loc[:, ["task_dlt_id", "notion_role_id"]],
        left_on="dlt_id",
        right_on="task_dlt_id",
        how="left",
    ).merge(
        df_roles.loc[:, ["notion_id", "role_title"]],
        left_on="notion_role_id",
        right_on="notion_id",
        how="left",
    )

    # joindre avec les rôles


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


ROLES_COLUMNS = {"id": "notion_id", "_dlt_id": "dlt_id"}
ROLES_ROLLUP_COLUMNS = {}
ROLES_TITLE_COLUMNS = {"plain_text": "role_title", "_dlt_parent_id": "dlt_parent_id"}


def fetch_roles(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    df_roles = fetch_and_rename("r_les", ROLES_COLUMNS, con)
    # df_role_relation = fetch_and_rename(
    #     "t_ches__properties__r_le_r_esponsable__relation", ROLES_ROLLUP_COLUMNS
    # )
    df_role_titles = fetch_and_rename(
        "r_les__properties__r_le__title", ROLES_TITLE_COLUMNS, con
    )
    df_roles = df_roles.merge(
        df_role_titles, left_on="dlt_id", right_on="dlt_parent_id", how="inner"
    )
    return df_roles.loc[:, ["notion_id", "dlt_id", "role_title"]]
