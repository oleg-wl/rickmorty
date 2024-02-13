

from database.schema import Database
import source.client as client

Database().test()
Database().init_db()

locs = client.Locations().to_df()
client.Client().df_to_sql(df=locs, name='locations')

res = client.Characters().to_df()
client.Client().df_to_sql(df=res, name='origin')

eps = client.Episodes().to_df()
client.Client().df_to_sql(df=eps, name='episodes')

Database().create_view()