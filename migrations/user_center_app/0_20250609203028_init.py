from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "delete_time" TIMESTAMPTZ,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "create_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "username" VARCHAR(256),
    "user_account" VARCHAR(256),
    "avatar_url" VARCHAR(1024),
    "gender" SMALLINT,
    "user_role" INT NOT NULL DEFAULT 0,
    "user_password" VARCHAR(512) NOT NULL,
    "phone" VARCHAR(128),
    "email" VARCHAR(512),
    "user_status" INT NOT NULL DEFAULT 0,
    "tags" JSONB
);
COMMENT ON COLUMN "user"."is_deleted" IS '软删除标记';
COMMENT ON COLUMN "user"."delete_time" IS '删除时间';
COMMENT ON COLUMN "user"."create_time" IS '创建时间';
COMMENT ON COLUMN "user"."update_time" IS '更新时间';
COMMENT ON COLUMN "user"."username" IS '用户名';
COMMENT ON COLUMN "user"."user_account" IS '用户账号';
COMMENT ON COLUMN "user"."avatar_url" IS '用户头像';
COMMENT ON COLUMN "user"."gender" IS '性别';
COMMENT ON COLUMN "user"."user_role" IS '用户角色 0 - 普通用户; 1 - 管理员';
COMMENT ON COLUMN "user"."user_password" IS '密码';
COMMENT ON COLUMN "user"."phone" IS '电话';
COMMENT ON COLUMN "user"."email" IS '邮箱';
COMMENT ON COLUMN "user"."user_status" IS '状态 0 - 正常';
COMMENT ON COLUMN "user"."tags" IS '用户json标签';
COMMENT ON TABLE "user" IS '用户表';
CREATE TABLE IF NOT EXISTS "tag" (
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "delete_time" TIMESTAMPTZ,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "create_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "tag_name" VARCHAR(256),
    "user_id" BIGINT,
    "parent_id" BIGINT,
    "is_parent" BOOL
);
COMMENT ON COLUMN "tag"."is_deleted" IS '软删除标记';
COMMENT ON COLUMN "tag"."delete_time" IS '删除时间';
COMMENT ON COLUMN "tag"."create_time" IS '创建时间';
COMMENT ON COLUMN "tag"."update_time" IS '更新时间';
COMMENT ON COLUMN "tag"."tag_name" IS '标签名';
COMMENT ON COLUMN "tag"."user_id" IS '用户ID';
COMMENT ON COLUMN "tag"."parent_id" IS '父标签ID';
COMMENT ON COLUMN "tag"."is_parent" IS '是否为父标签';
COMMENT ON TABLE "tag" IS '标签表';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
