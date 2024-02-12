
from sqlalchemy import Table, Column, MetaData, Integer, Computed

metadata = MetaData()

locations = Table(
    "locations",
    metadata,
    Column(
        "id",
        Integer,
    ),
)
