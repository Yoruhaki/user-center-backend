from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "id" TYPE INT USING "id"::INT;
        ALTER TABLE "users" ADD "deleted_at" TIMESTAMPTZ;
        COMMENT ON COLUMN "users"."is_deleted" IS '软删除标记';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "id" TYPE BIGINT USING "id"::BIGINT;
        ALTER TABLE "users" DROP COLUMN "deleted_at";
        COMMENT ON COLUMN "users"."is_deleted" IS '是否删除';"""
