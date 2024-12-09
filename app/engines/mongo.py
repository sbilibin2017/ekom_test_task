from logging import Logger
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.logger import get_logger
from app.core.settings import Settings, settings

log: Logger = get_logger()


class MongoEngine:
    def __init__(
        self,
        settings: Settings = settings,
    ):
        client: AsyncIOMotorClient = AsyncIOMotorClient(
            host=settings.DOCKER_MONGO_HOST,
            port=settings.MONGO_PORT,
            username=settings.MONGO_INITDB_ROOT_USERNAME,
            password=settings.MONGO_INITDB_ROOT_PASSWORD,
            authSource=settings.MONGO_INITDB_DATABASE,
        )
        self.db: AsyncIOMotorDatabase = client[settings.MONGO_DB]

    async def execute(self, collection: str, statement: str) -> Any:
        try:
            c = self.db[collection]  # noqa
            return eval(f"c.{statement}")
        except Exception as exc:
            log.error(f"Mongo engine error: {exc}")
            return None


mongo_engine: MongoEngine = MongoEngine()
