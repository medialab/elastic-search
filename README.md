# `Elastic Search` for local host

## Requirements
- Python 3.10
- elastic search, installed and running in terminal
- Python dependencies (installed in an activated virtual environment)

```shell
$ pip install -r requirements
```

## Configuration
```json
{
    "ELASTIC_PASS":"Password for the elastic user",
    "ELASTIC_USER":"elastic",
    "ELASTIC_CERT_FINGERPRINT":"HTTP CA certificate SHA-256 fingerprint",
    "ELASTIC_HOST":"https://localhost:9200/"
}
```

## Run

```python
python index.py DATA_FILE INDEX_NAME
```
