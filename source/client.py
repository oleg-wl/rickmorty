import requests
import pandas as pd

from database.schema import engine


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

        return pd.concat(l)

    def create_df(self) -> pd.DataFrame:
        
            data = self.get_all()
            df = data.explode(self.col)
            df = df.loc[df[self.col].notnull(), ['id', 'name', self.col]]
            df[self.col+'_id'] =  df[self.col].str.extract(r'(\d+)').astype(dtype=int, errors='ignore')

            df.to_sql('locations', con=engine)
            

class Episodes(Client):
    def __init__(self) -> None:
        super().__init__()
        self.url = self.url + 'episode'
        self.col = 'characters'

class Characters(Client):
    def __init__(self) -> None:
        super().__init__()
        self.url = self.url + 'character'

class Locations(Client):
    def __init__(self) -> None:
        super().__init__()
        self.url = self.url + 'location'
        self.col = 'residents'
