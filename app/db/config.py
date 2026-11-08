from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from dataclasses import dataclass, field
from sqlalchemy import URL



@dataclass
class DatabaseConfig:
    drivername: str
    username: str
    password: str = field(repr=False)
    host: str 
    port: int
    database: str
    alembic_url: str = field(init=False)
    engine: AsyncEngine | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False
    )


    def _build_url(self) -> URL:
        self.alembic_url = URL.create(
            drivername=self.drivername,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )
        return self.alembic_url

    def create_engine(self, **kwargs) -> AsyncEngine:
        if self.engine is None:
            self.engine = create_async_engine(self._build_url(), **kwargs)
        return self.engine



