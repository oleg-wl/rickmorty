#!/usr/bin python
import os
import logging
import click

import source.client as client
from database.schema import Database
from dotenv import load_dotenv


@click.group()
def cli():
    pass


@click.command()
def docker():
    """Команда для запуска скрипта в контейнере"""
    click.echo("CREATING DB")
    db = Database()
    db.init_db()
    db.create_view()
    click.echo("DOWNLOADING...")
    for i in ["locations", "origin", "episodes"]:
        Database().delete_table(i)
        match i:
            case "locations":
                locs = client.Locations().to_df()
                client.Client().df_to_sql(df=locs, name="locations")
            case "origin":
                res = client.Characters().to_df()
                client.Client().df_to_sql(df=res, name="origin")
            case "episodes":
                eps = client.Episodes().to_df()
                client.Client().df_to_sql(df=eps, name="episodes")

    click.echo("FINISHED")


@click.command()
def local():
    """Команда для запуска локально"""

    load_dotenv("config.env")
    click.echo("Загрузил конфиг")

    db = Database()
    db.init_db()
    click.echo("Создал базу данных")

    db.create_view()
    click.echo("Загружаю таблицу")
    for i in ["locations", "origin", "episodes"]:
        Database().delete_table(i)
        match i:
            case "locations":
                locs = client.Locations().to_df()
                client.Client().df_to_sql(df=locs, name="locations")
                click.echo("Загрузил локации")

            case "origin":
                res = client.Characters().to_df()
                client.Client().df_to_sql(df=res, name="origin")
                click.echo("Загрузил персонажей")

            case "episodes":
                eps = client.Episodes().to_df()
                client.Client().df_to_sql(df=eps, name="episodes")
                click.echo("Загрузил эпизоды")

    click.echo("ETL OK")


cli.add_command(local)
cli.add_command(docker)

if __name__ == "__main__":

    try:
        level = bool(int(os.getenv('DEBUG'))) 
    except: level = logging.WARNING
    
    logging.basicConfig(
        format="%(levelname)s - %(asctime)s: %(message)s LINE: (%(lineno)d) in %(name)s",
        datefmt="%x %X",
        level=level,
    )
    logging.getLogger('sqlalchemy').setLevel(level=level)
    cli()
