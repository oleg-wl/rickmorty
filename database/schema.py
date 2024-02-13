import logging

from sqlalchemy import create_engine, text
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime

from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles

from sqlalchemy.exc import DBAPIError

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@postgres:5432/rickmorty", echo=True)
logger = logging.getLogger("database")

@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"
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
            Column(
                "origin_id", Integer, ForeignKey("locations.id", ondelete="cascade")
            ),
        )

        episodes = Table(
            "episodes",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("episode_id", String),
            Column("name", String),
            Column("episode", String),
            Column("air_date", DateTime),
            Column(
                "characters_id", Integer, ForeignKey("origin.id", ondelete="cascade")
            ),
        )

        
        episodes.drop(engine, checkfirst=True)
        origin.drop(engine, checkfirst=True)
        locations.drop(engine, checkfirst=True)

        metadata.create_all(engine)

    def create_view(self):
        drop_sql = "DROP VIEW IF EXISTS characters_from_earth_count_by_month CASCADE;"
        create_sql = """
            CREATE VIEW characters_from_earth_count_by_month AS
            SELECT DATE_TRUNC('month', air_date) AS month_year,
                COUNT(l.id) AS episode_count
            FROM episodes e
            JOIN origin o ON e.characters_id = o.id
            JOIN locations l ON o.id = l.id
            WHERE l."name" LIKE 'Earth%'
            GROUP BY DATE_TRUNC('month', air_date)
            ORDER BY month_year DESC;
        """

        with engine.connect() as conn:
            trans = conn.begin()
            try:
                conn.execute(text(drop_sql))
                conn.execute(text(create_sql))
                trans.commit()
            except Exception as e:
                trans.rollback()
                raise e