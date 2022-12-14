import csv
import json
import os

import click
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm


@click.command()
@click.argument("filename")
@click.argument("index")
def main(filename, index):

    # ----------------------------------------------------#
    # CONFIRM DATA SOURCE

    if not os.path.isfile(filename):
        raise FileNotFoundError(f"\n    The data file was not found. The path given was: {filename}")
    else:
        DATA = filename

    # ----------------------------------------------------#
    # CONFIGURATION FOR ELASTIC SEARCH CLIENT

    PERSONAL_CONFIG = "config.json"
    EXAMPLE_CONFIG = "example.config.json"

    config = EXAMPLE_CONFIG
    if os.path.isfile(PERSONAL_CONFIG):
        config = PERSONAL_CONFIG

    with open(config, "r") as f:
        config = json.load(f)
        ELASTIC_PASSWORD = config.get("ELASTIC_PASS")
        ELASTIC_USER = config.get("ELASTIC_USER")
        CERT_FINGERPRINT = config.get("ELASTIC_CERT_FINGERPRINT")
        ELASTIC_HOST = config["ELASTIC_HOST"]

    # ----------------------------------------------------#
    # CREATE CLIENT
    if ELASTIC_PASSWORD:
        client = Elasticsearch(
            ELASTIC_HOST,
            ssl_assert_fingerprint=CERT_FINGERPRINT,
            basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD)
            )
    else:
        client = Elasticsearch(ELASTIC_HOST)

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

        for row in csv_reader: pass
        total = csv_reader.line_num
        f.seek(0)
        next(csv_reader)

        for row in tqdm(csv_reader, total=total, desc="Progress Bar", dynamic_ncols=True):
            client.index(index=index, id=row.pop("unique_id"), document=row)


if __name__ == "__main__":
    main()
