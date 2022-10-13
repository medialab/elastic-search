import csv
import json
import os

import click
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm


@click.command()
@click.argument("index")
def main(index):

    # ----------------------------------------------------#
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

    # ----------------------------------------------------#
    # CREATE CLIENT
    client = Elasticsearch(
        "https://localhost:9200",
        ssl_assert_fingerprint=CERT_FINGERPRINT,
        basic_auth=("elastic", ELASTIC_PASSWORD)
        )

    # ----------------------------------------------------#
    # CREATE INDEX WITH MAPPING
    with open("db_mappings.json", "r") as f:
        mapping = json.load(f)

    if not client.indices.exists(index=index):
        client.indices.create(index=index, **mapping)

    # ----------------------------------------------------#
    # ADD DOCUMENTS
    with open(DATA, "r") as f:
        csv_reader = csv.DictReader(f)

        total = len(list(csv_reader))
        f.seek(0)
        csv_reader.__next__()

        pbar = tqdm(total=total, desc="Progress Bar", dynamic_ncols=True)

        for row in csv_reader:
            client.index(index=index, id=row.pop("unique_id"), document=row)
            pbar.update(len(row)/10)

        pbar.close()


if __name__ == "__main__":
    main()