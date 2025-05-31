from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(256),
    "user_account" VARCHAR(256) UNIQUE,
    "avatar_url" VARCHAR(1024),
    "gender" SMALLINT,
    "user_password" VARCHAR(512) NOT NULL,
    "phone" VARCHAR(128),
    "email" VARCHAR(512),
    "user_status" INT NOT NULL DEFAULT 0,
    "create_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" BOOL NOT NULL DEFAULT False
);
COMMENT ON COLUMN "user"."username" IS '用户名';
COMMENT ON COLUMN "user"."user_account" IS '用户账号';
COMMENT ON COLUMN "user"."avatar_url" IS '用户头像';
COMMENT ON COLUMN "user"."gender" IS '性别';
COMMENT ON COLUMN "user"."user_password" IS '密码';
COMMENT ON COLUMN "user"."phone" IS '电话';
COMMENT ON COLUMN "user"."email" IS '邮箱';
COMMENT ON COLUMN "user"."user_status" IS '状态 0 - 正常';
COMMENT ON COLUMN "user"."create_time" IS '创建时间';
COMMENT ON COLUMN "user"."update_time" IS '更新时间';
COMMENT ON COLUMN "user"."is_deleted" IS '是否删除';
COMMENT ON TABLE "user" IS '用户表';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
