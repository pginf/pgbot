import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, DateTime, Text, String
import os
from pgbot.env import DATABASE_URL, DEBUG

engine = sqlalchemy.create_engine(DATABASE_URL, echo=DEBUG)
Base = declarative_base()


class PGStudent(Base):
    __tablename__ = "PGStudent"

    nr_albumu = Column(Integer, primary_key=True)
    imie = Column(String(30), nullable=False)
    nazwisko = Column(String(30), nullable=False)
    discord_id = Column(BigInteger, nullable=True)

    def __init__(self, nr_albumu: int, imie: str, nazwisko: str, discord_id: int = None):
        self.nr_albumu = nr_albumu
        self.imie = imie
        self.nazwisko = nazwisko
        self.discord_id = discord_id


Base.metadata.create_all(engine)
