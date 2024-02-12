from sqlalchemy import create_engine, text

engine = create_engine("postgresql+psycopg2://postgres:postgres@postgres:5432/rickmorty")

class Database:

    def test(self):
        with engine.connect() as conn:

            result = conn.execute(text("select version()"))
            print(result.all())