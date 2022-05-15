import click
import json
from app import app, mongo_client, elastic_client
from app.db_operator import mongo_operator, elastic_operator


runtemplate = "{} elapsed for {} ms"


@app.cli.command("insert_data")
@click.argument("path")
def insert_data(path):
    with open(path, "r") as f:
        records = f.read().splitlines()
        records = [json.loads(record) for record in records]
    
    mongo_result, mongo_elapsed = mongo_operator.common_insert(records)
    elastic_result, elastic_elapsed = elastic_operator.common_insert(records)

    click.echo(runtemplate.format("MongoDB", mongo_elapsed))
    click.echo(runtemplate.format("Elastic", elastic_elapsed))


@app.cli.command("drop_collections")
def drop_collections():
    mongo_client.drop_collections()
    elastic_client.drop_collections()


@app.cli.command("update_data")
@click.option("--query", type=json.loads)
@click.option("--update", type=json.loads)
@click.option("--how")
def update_data(query, update, how):
    mongo_result, mongo_elapsed = mongo_operator.common_update(
        filters=query, update=update, how=how
    )
    elastic_result, elastic_elapsed = elastic_operator.common_update(
        query=query, update=update, how=how
    )
    click.echo(runtemplate.format("MongoDB", mongo_elapsed))
    click.echo(runtemplate.format("Elastic", elastic_elapsed))


@app.cli.command("delete_data")
@click.option("--query", type=json.loads)
@click.option("--how")
def delete_data(query, how):
    mongo_result, mongo_elapsed = mongo_operator.common_delete(filters=query, how=how)
    elastic_result, elastic_elapsed = elastic_operator.common_delete(
        query=query, how=how
    )
    click.echo(runtemplate.format("MongoDB", mongo_elapsed))
    click.echo(runtemplate.format("Elastic", elastic_elapsed))
