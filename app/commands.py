import click
import json
from app import app, mongo_client, elastic_client

@app.cli.command("insert_data")
@click.argument("path")
def insert_data(path):
    with open(path, "r") as f:
        records = f.readlines()
        for record in records:
            dict_record = json.loads(record)
            elastic_client.insert_data(dict_record)
            mongo_client.insert_data(dict_record)


@app.cli.command("drop_collections")
def drop_collections():
    mongo_client.drop_collections()
    elastic_client.drop_collections()