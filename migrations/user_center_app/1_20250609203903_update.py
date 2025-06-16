from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_tag_tag_nam_66e60f" ON "tag" ("tag_name");
        CREATE INDEX IF NOT EXISTS "idx_tag_user_id_0d7792" ON "tag" ("user_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "idx_tag_user_id_0d7792";
        DROP INDEX IF EXISTS "uid_tag_tag_nam_66e60f";"""
