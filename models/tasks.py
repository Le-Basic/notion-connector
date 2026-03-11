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


def fetch_tasks(con: duckdb.DuckDBPyConnection) -> pd.Dataframe:
    df_tasks = fetch_and_rename("t_ches", TASKS_COLUMNS, con)

    df_tasks = df_tasks.astype(
        {
            "notion_task_start_date": "datetime64[ns]",
            "notion_task_end_date": "datetime64[ns]",
        }
    )
    return df_tasks
