import logging

from sqlalchemy import create_engine, text
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime

from sqlalchemy.exc import DBAPIError

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:15432/rickmorty", echo=True
)

logger = logging.getLogger("database")


class Database:

    def test(self):

        try:

            with engine.connect() as conn:

                result = conn.execute(text("select version()"))
                logger.info("Connection OK. PG ver %s" % result.all())

        except DBAPIError as dberr:
            logger.exception("Database error %s" % dberr)
        except Exception as e:
            logger.exception("An error occured %s" % e)

    def init_db(self):

        metadata = MetaData()

        locations = Table(
            "locations",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
        )

        origin = Table(
            "origin",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("origin_id", Integer, ForeignKey('locations.id', ondelete='cascade')),
        )

        episodes = Table(
            "episodes",
            metadata,
            Column('id', Integer, primary_key=True),
            Column("episode_id", String),
            Column("name", String),
            Column("episode", String),
            Column("air_date", DateTime),
            Column("characters_id", Integer, ForeignKey("origin.id", ondelete='cascade')),
        )

        episodes.drop(engine, checkfirst=True)
        origin.drop(engine, checkfirst=True)
        locations.drop(engine, checkfirst=True)

        metadata.create_all(engine)
