import logging

import requests
import pandas as pd

from sqlalchemy.types import Integer, String

from database.schema import Database

logger = logging.getLogger('client')

class Client():
    def __init__(self) -> None:
        self.url = "https://rickandmortyapi.com/api/"
        self.col = ''

        self.sess = requests.Session()
        self.engine = Database().engine

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

        df = df.to_sql(name=name, con=self.engine, if_exists='append', index=True, index_label='id')
        logger.info('Inserted %s rows' %(df))

class Episodes(Client):
    def __init__(self) -> None:
        super().__init__()
        self.url = self.url + 'episode'
        self.col = 'characters'

    def to_df(self) -> pd.DataFrame:
        data = self.get_all()
        df = data.explode(column=self.col)
        df = df.loc[df[self.col].notnull(), ['id', 'name', 'episode', 'air_date', self.col]]
        df[self.col+'_id'] =  df[self.col].str.extract(r'(\d+)').astype(dtype=int, errors='ignore')
        df = (df.reset_index(drop=True)
              .rename({'id':'episode_id'}, axis=1)
              .drop(self.col, axis=1))

        return df
class Locations(Client):
    def __init__(self) -> None:
        super().__init__()
        self.url = self.url + 'location'

    def to_df(self) -> pd.DataFrame:
        
        data = self.get_all()
        data = data.set_index('id')['name']
        data[999] = 'unknown'
        return data


class Residents(Client):
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

class Characters(Client):
    def __init__(self) -> None:
        super().__init__()
        self.url = self.url + 'character'
        self.col = 'origin'

    def to_df(self) -> pd.DataFrame:
        data = self.get_all()

        def extract_url(row):
            val =  row.get('url')
            if len(val) == 0: return '999' 
            else: return val
        
        data[self.col+'_id'] = (data['origin'].apply(lambda x: extract_url(x))
                                .str.extract(r'(\d+)')
                                .astype(dtype=int, errors='ignore')
                                )
        data = data.set_index('id', drop=True).loc[:,['name', self.col+'_id']]
        return data

        