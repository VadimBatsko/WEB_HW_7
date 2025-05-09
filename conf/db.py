import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

USER = config.get('DEV_DB', 'USER')
PASSWORD = config.get('DEV_DB', 'PASSWORD')
DB_NAME = config.get('DEV_DB', 'DB_NAME')
HOST = config.get('DEV_DB', 'HOST')
PORT = config.get('DEV_DB', 'PORT')

URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'

engine = create_engine(URI, echo=True, pool_size=5, max_overflow=0)
DBsession = sessionmaker(bind=engine)
session = DBsession()
