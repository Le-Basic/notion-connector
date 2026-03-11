import duckdb
import pandas as pd
from .tasks import fetch_tasks
from .roles import populate_role_title
from .business_days import add_business_days_count, compute_tasks_days


def create_models() -> None:
    con = duckdb.connect("notion.duckdb")

    df_tasks = fetch_tasks(con)
    df_tasks = populate_role_title(df_tasks, con)

    df_tasks = add_business_days_count(df_tasks)

    df_tasks_days = compute_tasks_days(df_tasks)

    df_tasks.to_parquet("tasks.parquet", index=False)
    df_tasks_days.to_parquet("tasks_days.parquet", index=False)
