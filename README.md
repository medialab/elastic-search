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
    "ELASTIC_PASSWORD":"Password for the elastic user",
    "USR_LOGIN":"elastic",
    "CERT_FINGERPRINT":"HTTP CA certificate SHA-256 fingerprint",
    "DATA_FILE":"example.csv",
    "URL":"https://localhost:9200/"
}
```

## Run

```python
python index.py
```
