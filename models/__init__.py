import duckdb
import pandas as pd
from .tasks import fetch_bricks
from .roles import populate_role_title
from .business_days import add_business_days_count, compute_tasks_days
from .projects import populate_project_titles
from .people import populate_accountables
from .precomputed import compute_bricks_precomputed_fields


def create_models() -> None:
    con = duckdb.connect("notion.duckdb")

    df_bricks = fetch_bricks(con)
    df_bricks = populate_role_title(df_bricks, con)

    df_bricks = add_business_days_count(df_bricks)
    df_bricks_with_people = populate_accountables(df_bricks, con)
    df_bricks_with_project = populate_project_titles(df_bricks_with_people, con)
    df_bricks_filtered = filter_over_bricks(df_bricks_with_project)
    df_bricks_with_all_fields = compute_bricks_precomputed_fields(df_bricks_filtered)
    df_bricks_days = compute_tasks_days(df_bricks_with_all_fields)

    export_to_csv(df_bricks_with_all_fields, "bricks")
    export_to_csv(df_bricks_days, "bricks_days")


def export_to_csv(df: pd.DataFrame, file_name: str) -> None:
    df.loc[
        :,
        ~df.columns.isin(["dlt_id"]),
    ].to_csv(f"exports/{file_name}.csv", index=False)


def filter_over_bricks(df_bricks: pd.DataFrame) -> pd.DataFrame:
    return df_bricks[~(df_bricks["notion_task_status"].isin(["Annulé", "Terminé"]))]
