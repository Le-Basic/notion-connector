import duckdb
from .tasks import fetch_bricks
from .roles import populate_role_title
from .business_days import add_business_days_count, compute_tasks_days


def create_models() -> None:
    con = duckdb.connect("notion.duckdb")

    df_bricks = fetch_bricks(con)
    df_bricks = populate_role_title(df_bricks, con)

    df_bricks = add_business_days_count(df_bricks)

    df_bricks_days = compute_tasks_days(df_bricks)

    df_bricks.to_parquet("bricks.parquet", index=False)
    df_bricks_days.to_parquet("bricks_days.parquet", index=False)
