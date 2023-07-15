from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "cargo" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "cargo_type" VARCHAR(64) NOT NULL,
    "rate" DOUBLE PRECISION NOT NULL,
    "date" DATE NOT NULL,
    CONSTRAINT "uid_cargo_cargo_t_c87b9d" UNIQUE ("cargo_type", "date")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
