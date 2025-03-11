
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncConnection

class AsyncDatabaseClient:

    def __init__(
        self,
        connection_string: str = "postgresql+asyncpg://postgres:postgres123@localhost:5432/toy",
        pool_size: int = 10,
        max_overflow: int = 5,
        pool_timeout: int = 30,
        pool_recycle: int = 1800
    ):
        print("initialise database pooling")
        self.engine = create_async_engine(
            connection_string,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout,
            pool_recycle=pool_recycle,
            echo=False  # Passez à True pour voir les requêtes SQL dans la console
        )
        self.sessionFactory = async_sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
    
    def session(self) -> AsyncSession:
        return self.sessionFactory()
    
    def connection(self) -> AsyncConnection:
        return self.engine.connect()
    
    def get_engine(self):
        return self.engine
    