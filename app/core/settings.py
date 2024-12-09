from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
    )

    APP_TITLE: str = "e-com test task app"
    APP_WORKERS: int = 1
    APP_LOG_LEVEL: str = "debug"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    MONGO_HOST: str = "0.0.0.0"
    MONGO_PORT: int = 27017
    MONGO_DB: str = "ecom_test_task"
    MONGO_INITDB_ROOT_USERNAME: str = "test"
    MONGO_INITDB_ROOT_PASSWORD: str = "test"
    MONGO_INITDB_DATABASE: str = "ecom_test_task"

    DOCKER_MONGO_HOST: str = "db"
    DOCKER_APP_HOST: str = "app"

    @property
    def mongo_docker_uri(self) -> str:
        return f"mongodb://{self.DOCKER_MONGO_HOST}:{self.MONGO_PORT}"


settings: Settings = Settings()
