from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

motor = create_engine("sqlite+pysqlite:///:memory:", echo=True)

class Base(DeclarativeBase):
    pass