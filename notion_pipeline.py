import dlt

from notion import notion_databases


def load_databases() -> None:
    """Loads all databases from a Notion workspace which have been shared with
    an integration.
    """
    pipeline = dlt.pipeline(
        pipeline_name="notion",
        destination='duckdb',
        dataset_name="notion_data",
    )
    selected_database_ids = [{"id": "66861714ea264e4cb4c65e1b0f278dde"}]

    data = notion_databases(
        database_ids=selected_database_ids
    )

    info = pipeline.run(data)
    print(info)


if __name__ == "__main__":
    load_databases()
