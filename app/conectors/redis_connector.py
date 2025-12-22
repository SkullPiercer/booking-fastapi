import redis.asyncio as redis

from app.core.config import get_settings


class RedisConnector:
    def __init__(self, url, port):
        self.url = url
        self.port = port
        self.redis = None

    async def connect(self):
        self.redis = await redis.Redis(host=self.url, port=self.port)

    async def disconnect(self):
        if self.redis:
            await self.redis.close()

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: str, exp: int = None):
        if exp:
            await self.redis.set(key, value, ex=exp)
        else:
            await self.redis.set(key, value)

    async def delete(self, key: str):
        await self.redis.delete(key)


settings = get_settings()
redis_manager = RedisConnector(settings.REDIS_HOST, settings.REDIS_PORT)
