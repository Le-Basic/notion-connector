import pandas as pd
import duckdb
from .lib import fetch_and_rename


def populate_project_fields(
    df_tasks: pd.DataFrame, con: duckdb.DuckDBPyConnection
) -> pd.DataFrame:
    df_projects = fetch_projects(con)
    df_projets_relations = fetch_and_rename(
        "t_ches__properties__projet__relation",
        {
            "_dlt_parent_id": "task_dlt_id",
            "id": "notion_project_id",
        },
        con,
    )

    df_tasks_with_projects = df_tasks.merge(
        df_projets_relations, left_on="dlt_id", right_on="task_dlt_id", how="left"
    ).merge(
        df_projects,
        left_on="notion_project_id",
        right_on="notion_id",
        how="left",
    )

    # Remove join columns
    return df_tasks_with_projects.loc[
        :,
        ~df_tasks_with_projects.columns.isin(
            ["task_dlt_id", "notion_project_id", "notion_id"]
        ),
    ]


PROJETS_COLUMN = {
    "id": "notion_id",
    "_dlt_id": "dlt_id",
    "properties___tat__status__name": "project_status",
    "url": "project_url",
}
PROJETS_TITLE_COLUMNS = {
    "plain_text": "project_title",
    "_dlt_parent_id": "dlt_parent_id",
}


def fetch_projects(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    df_projects = fetch_and_rename("projets", PROJETS_COLUMN, con)
    df_project_titles = fetch_and_rename(
        "projets__properties__nom__title", PROJETS_TITLE_COLUMNS, con
    )
    df_projects = df_projects.merge(
        df_project_titles, left_on="dlt_id", right_on="dlt_parent_id", how="inner"
    )
    return df_projects.loc[
        :, ["notion_id", "project_title", "project_url", "project_status"]
    ]
