import csv
import json
import os

import click
from elasticsearch import Elasticsearch


@click.command()
@click.argument("index")
def main(index):
# CONFIGURATION FOR ELASTIC SEARCH CLIENT
    PERSONAL_CONFIG = "config.json"
    EXAMPLE_CONFIG = "example.config.json"

    config = EXAMPLE_CONFIG
    if os.path.isfile(PERSONAL_CONFIG):
        config = PERSONAL_CONFIG

    with open(config, "r") as f:
        config = json.load(f)
        ELASTIC_PASSWORD = config["ELASTIC_PASSWORD"]
        CERT_FINGERPRINT = config["CERT_FINGERPRINT"]
        DATA = os.path.join("data", config["DATA_FILE"])

    # CREATE CLIENT
    client = Elasticsearch(
        "https://localhost:9200",
        ssl_assert_fingerprint=CERT_FINGERPRINT,
        basic_auth=("elastic", ELASTIC_PASSWORD)
        )

    with open("db_mappings.json", "r") as f:
        mapping = json.load(f)

    # CREATE INDEX WITH MAPPING
    if not client.indices.exists(index=index):
        client.indices.create(index=index, **mapping)

    # ADD DOCUMENTS
    with open(DATA, "r") as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            client.index(index=index, id=row.pop("unique_id"), document=row)

if __name__ == "__main__":
    main()