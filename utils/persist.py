from datetime import datetime
import json
from session import spark

CURRENT_DATETIME = datetime.now().strftime("%Y%m%d")
EXTRACT_FOLDER = 'extract'


def persist_json(data: object, path: str, suffix: str):
    file_name = f"{CURRENT_DATETIME}_{suffix}.json"
    with open(f'./data/{path}/{file_name}', 'w') as file:
        json.dump(data, file)


def spark_read_json(path: str, suffix: str):
    file_name = f"./data/{path}/{CURRENT_DATETIME}_{suffix}.json"
    df = spark.read.option("multiline", "true").json(file_name)
    return df
