# Create the engine once and yield one session per request
# Dont use a global session for all request, causes issues under load

import configparser
from .config import DatabaseConfig
from configparser_crypt import ConfigParserCrypt
from .base import *
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker
from app.db.base import Base
from app.core.config import DB_KEY, DB_ENCRYPTED_INI



class Database:

    def __init__(self):
        self.session: async_sessionmaker[AsyncSession] | None = None


    def create_session_objects(self) -> DatabaseConfig:
        with open(DB_KEY, 'rb') as f:
            db_key = f.read()
        conf = ConfigParserCrypt()
        conf.aes_key = db_key
        conf.read_encrypted(DB_ENCRYPTED_INI)

        pg_config = DatabaseConfig(
            conf['database']['drivername'],
            conf['database']['username'],
            conf['database']['password'],
            conf['database']['host'],
            int(conf['database']['port']),
            conf['database']['database']
        )


        pg_engine = pg_config.create_engine(
            pool_size=7,
            max_overflow=7,
            pool_recycle=3600,
            pool_pre_ping=True,
            echo=True)
        self.session = async_sessionmaker(
            bind=pg_engine,
            expire_on_commit=False)
        return pg_config


    async def get_db(self):
        if self.session is None:
            raise RuntimeError("Database session factory not initalized.")
        async with self.session() as pg_session:
            yield pg_session




database = Database()
db_conf = database.create_session_objects()