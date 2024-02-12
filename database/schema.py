from sqlalchemy import create_engine, text
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime

engine = create_engine("postgresql+psycopg2://postgres:postgres@postgres:5432/rickmorty")

class Database:

    def test(self):
        with engine.connect() as conn:

            result = conn.execute(text("select version()"))
            print(result.all())

    def loc():
        

        metadata = MetaData()

        location = Table('location', metadata,
              Column('location_id', Integer, ForeignKey('residency.id')),
              Column('residents_id', Integer, primary_key=True)
              )

        episodes = Table('episodes', metadata,
                    Column('air_date', DateTime),
                    Column('episode', String),
                    Column('characters_id', Integer, ForeignKey('location.residents_id')),
                    )

        residency = Table('residency', metadata,
                    Column('id', primary_key=True),
                    Column('name', String),
                    )
        metadata.create_all(engine)