from database.schema import Database
import source.client as client

Database().init_db()

for i in ['locations', 'origin', 'episodes']:
    Database().delete_table(i)            
    match i:
        case 'locations':
            locs = client.Locations().to_df()
            client.Client().df_to_sql(df=locs, name='locations')
        case 'origin':
            res = client.Characters().to_df()
            client.Client().df_to_sql(df=res, name='origin')
        case 'episodes':
            eps = client.Episodes().to_df()
            client.Client().df_to_sql(df=eps, name='episodes')
            
Database().create_view()