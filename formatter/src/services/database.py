from typing import Any, Self
from logging import info, error
from psycopg.connection_async import AsyncConnection
from psycopg.abc import Query, Params


class MovieDatabase:
    def __init__(
        self,
        host: str = 'localhost',
        port: str = '6543',
        user: str = 'postgres',
        password: str = 'postgres',
        database: str = 'postgres',
    ) -> None:
        self._host = host
        self._port = int(port)
        self._user = user
        self._password = password
        self._database = database
        self._connection: AsyncConnection | None = None

    async def connect(self) -> Self:
        info(f'connecting to {self._host}:{self._port}')
        self._connection = await AsyncConnection.connect(
            dbname=self._database,
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
        )
        return self

    async def close(self) -> Self:
        info(f'closing connection to {self._host}:{self._port}')
        if self._connection:
            await self._connection.close()
        return self

    async def insert_into(self, params: Params) -> Any | None:
        q: Query = '''
        INSERT INTO "movie_format"
        (job_id, movie_scraper_id, title, synopsis, where_to_watch, info)
        VALUES
        (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        '''
        if not self._connection:
            error('No active connection. Call "connect" first.')
            raise ValueError("No active connection. Call 'connect' first.")
        
        async with self._connection.transaction():
            cur = await self._connection.execute(q, params=params)
            result = await cur.fetchone()
            return result[0] if result is not None else None
            
