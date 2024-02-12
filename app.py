from database.schema import Database
from source.client import Locations

Database().test()
Locations().create_df()