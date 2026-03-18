import duckdb
import pandas as pd
from .lib import fetch_and_rename

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


def fetch_bricks(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    df_tasks = fetch_and_rename("t_ches", TASKS_COLUMNS, con)

    df_bricks = df_tasks[df_tasks["notion_task_level"] == "Brique"].drop(
        ["notion_task_level"], axis=1
    )
    df_bricks = df_bricks.astype(
        {
            "notion_task_start_date": "datetime64[ns]",
            "notion_task_end_date": "datetime64[ns]",
        }
    )
    return _add_brick_name(df_bricks, con)


def _add_brick_name(
    df_bricks: pd.DataFrame, con: duckdb.DuckDBPyConnection
) -> pd.DataFrame:
    df_names = (
        fetch_and_rename(
            "t_ches__properties__nom__title",
            {"plain_text": "task_name", "_dlt_parent_id": "task_dlt_id"},
            con,
        )
        .groupby(["task_dlt_id"])
        .apply(lambda row: "".join(row["task_name"]))
        .reset_index(name="task_name")
    )
    df_bricks = df_bricks.merge(
        df_names, left_on="dlt_id", right_on="task_dlt_id", how="left"
    )

    return df_bricks.loc[:, ~df_bricks.columns.isin(["task_dlt_id"])]
