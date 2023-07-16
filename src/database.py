from typing import List

from tortoise import Tortoise


async def db_init(
        database_url: str,
        models_path: List[str] = None,
        generate_schema: bool = True):
    if models_path is None:
        models_path = [
            "src.cargo.models"
        ]

    await Tortoise.init(
        db_url=database_url,
        modules={
            "models": models_path
        }
    )

    if generate_schema:
        await Tortoise.generate_schemas()


async def drop_databases():
    await Tortoise._drop_databases()


async def close_db():
    await Tortoise.close_connections()


async def clean_up():
    await drop_databases()
    await close_db()
