import redis

from app.core.config import get_settings


class RedisConnector:
    def __init__(self, url, port):
        self.url = url
        self.port = port

    async def connect(self):
        self.connection = redis.Redis(host=self.url, port=self.port)

    async def disconnect(self):
        if self.connection:
            self.connection.close()

    async def get(self, key: str):
        return await self.connection.get(key)

    async def set(self, key: str, value: str, exp: int = None):
        if exp:
            await self.connection.set(key, value, ex=exp)
        else:
            await self.connection.set(key, value)

    async def delete(self, key: str):
        await self.connection.delete(key)


settings = get_settings()
redis_manager = RedisConnector(settings.REDIS_HOST, settings.REDIS_PORT)
