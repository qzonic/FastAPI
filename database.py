from tortoise.contrib.fastapi import register_tortoise

import settings


def connect_database(app):
    register_tortoise(
        app=app,
        config=settings.DATABASE_CONFIG
    )
