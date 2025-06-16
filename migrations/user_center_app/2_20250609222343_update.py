from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "tags" TYPE VARCHAR(1024) USING "tags"::VARCHAR(1024);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "tags" TYPE JSONB USING "tags"::JSONB;"""
