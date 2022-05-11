import click
import json
from app import app, mongo_client, elastic_client

@app.cli.command("insert_data")
@click.argument("path")
def insert_data(path):
    with open(path, "r") as f:
        records = f.readlines()
        records = [json.loads(record) for record in records]
        for record in records:
            elastic_client.insert_data(record)
        mongo_client.insert_data(records)
            
            


@app.cli.command("drop_collections")
def drop_collections():
    mongo_client.drop_collections()
    elastic_client.drop_collections()