from datetime import datetime
from genericpath import isfile
from elasticsearch import Elasticsearch
import json
import csv
import os

# CONFIGURATION FOR ELASTIC SEARCH CLIENT
PERSONAL_CONFIG = "config.json"
EXAMPLE_CONFIG = "example.config.json"

config = EXAMPLE_CONFIG
if os.path.isfile(PERSONAL_CONFIG):
    config = PERSONAL_CONFIG

with open(config, "r") as f:
    config = json.load(f)
    ELASTIC_PASSWORD = config["ELASTIC_PASSWORD"]
    USR_LOGIN = config["USR_LOGIN"]
    CERT_FINGERPRINT = config["CERT_FINGERPRINT"]
    INDEX_NAME = config["INDEX_NAME"]
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
if not client.indices.exists(index=INDEX_NAME):
    client.indices.create(index=INDEX_NAME, **mapping)

# ADD DOCUMENTS
with open(DATA, "r") as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        client.index(index=INDEX_NAME, id=row.pop("unique_id"), document=row)
