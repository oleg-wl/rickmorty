import logging

import requests
import pandas as pd

from sqlalchemy.types import Integer, String

from database.schema import engine

logger = logging.getLogger('client')

class Client():
    def __init__(self) -> None:
        self.url = "https://rickandmortyapi.com/api/"
        self.col = ''

        self.sess = requests.Session()

    def get_all(self) -> pd.DataFrame:

        pages = self.sess.get(url=self.url).json()["info"]["pages"]

        l = [
            pd.DataFrame(
                self.sess.get(url=self.url, params={"page": i}).json()["results"]
            )
            for i in range(1, int(pages) + 1)
        ]

        logger.info('Data retrieved: {} col, {} pages'.format(self.col, pages))
        return pd.concat(l)

    def df_to_sql(self, df: pd.DataFrame = None, name: str = None, ):

        df = df.to_sql(name=name, con=engine, if_exists='append', index=True, index_label='id')
        logger.info('Inserted %s rows' %(df))

class Episodes(Client):
    def __init__(self) -> None:
        super().__init__()
        self.url = self.url + 'episode'
        self.col = 'characters'

    def to_df(self) -> pd.DataFrame:
        pass

class Residency(Client):
    def __init__(self) -> None:
        super().__init__()
        self.url = self.url + 'location'

    def to_df(self) -> pd.DataFrame:
        pass


class Locations(Client):
    def __init__(self) -> None:
        super().__init__()
        self.url = self.url + 'location'
        self.col = 'residents'

    def to_df(self) -> pd.DataFrame:

        data = self.get_all()
        df = data.explode(self.col)
        df = df.loc[df[self.col].notnull(), ['id', 'name', self.col]]
        df[self.col+'_id'] =  df[self.col].str.extract(r'(\d+)').astype(dtype=int, errors='ignore')

        df = (df.reset_index()
              .rename(columns={'id':'location_id'})
              .drop(['index', 'name', 'residents'], axis=1))

        return df

        