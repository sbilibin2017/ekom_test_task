from typing import AsyncGenerator

from app.engines.mongo import MongoEngine, mongo_engine


class FormTemplateRepository:
    def __init__(
        self,
        mongo_engine: MongoEngine = mongo_engine,
    ):
        self.mongo_engine = mongo_engine

    async def generate_form_template(self) -> AsyncGenerator:
        async for template in await self.mongo_engine.execute(
            collection="form_templates",
            statement="find()",
        ):
            yield template


form_template_repository = FormTemplateRepository()
