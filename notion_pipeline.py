import dlt
from notion import notion_databases
from models import create_models


def load_databases() -> None:
    """Loads all databases from a Notion workspace which have been shared with
    an integration.
    """
    pipeline = dlt.pipeline(
        pipeline_name="notion",
        destination="duckdb",
        dataset_name="notion_data",
    )
    selected_database_ids = [
        {"id": "66861714ea264e4cb4c65e1b0f278dde"},
        {"id": "17d6afc9ad648062a313c378efefbf70"},
        {"id": "c7682d38bf184583b6d7306ccbb31b99"},
    ]

    data = notion_databases(database_ids=selected_database_ids)

    info = pipeline.run(data)
    print(info)


if __name__ == "__main__":
    # load_databases()
    create_models()
