import logging
import os

from sqlalchemy import create_engine, text
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime

from sqlalchemy.exc import DBAPIError, ProgrammingError

logger = logging.getLogger("database")

class Database:
    def __init__(self):

        cred = {
    'db_user':os.getenv('DB_USER', 'postgres'),
    'db_password':os.getenv('DB_PASSWORD', 'postgres'),
    'db_host':os.getenv('DB_HOST', 'postgres'),
    'db_port':os.getenv('DB_PORT', 5432),
    'database':os.getenv('DATABASE', 'rickmorty'),
    }

        echo = bool(os.getenv('DEBUG', False))
        c = 'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{database}'.format(**cred)
        self.engine = create_engine(c, echo=echo)


    @staticmethod
    def connector(command):
        engine = Database().engine
        try:
            with engine.connect() as conn:
                transaction = conn.begin()
                try:
                    conn.execute(text(command))
                    transaction.commit()
                    logger.info("Command OK")
                except Exception as e:
                    transaction.rollback()
                    logger.error("Error during execution command %s" % e)
        except DBAPIError as dberr:
                logger.error("Database error %s" % dberr)
        except Exception as e:
            logger.error("Connection error %s" % e)

    def test(self):
        Database.connector('select version()')

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

        metadata.create_all(self.engine, checkfirst=True)

    def create_view(self):
        view = """
        DO
        $$
        BEGIN
            IF NOT EXISTS (SELECT 1 from information_schema.views 
                WHERE table_name = 'characters_from_earth_count_by_month') THEN
                CREATE VIEW characters_from_earth_count_by_month AS
                SELECT DATE_TRUNC('month', air_date) AS date,
                    COUNT(l.id) AS count
                FROM episodes e
                JOIN origin o ON e.characters_id = o.id
                JOIN locations l ON o.id = l.id
                WHERE l."name" LIKE 'Earth%'
                GROUP BY DATE_TRUNC('month', air_date)
                ORDER BY date DESC;
            END IF;
        END
        $$;
        """
        Database.connector(view)
        logger.info('View OK')

    def delete_table(self, tablename:str):
        sql = f'DELETE FROM {tablename};'
        Database.connector(sql)