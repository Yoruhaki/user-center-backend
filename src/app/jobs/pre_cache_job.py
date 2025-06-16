from asyncio import gather
from functools import partial

from fastapi import FastAPI
from redis.asyncio import Redis

from src.app.models import User
from math import ceil
from src.app.schemas import SafetyUser
from src.app.common import Pagination
from datetime import timedelta

main_user_id_list = [1]


async def cache_recommend_user(redis: Redis, user_id: int) -> None:
    redis_key = f"compare-friends:user:recommend:{user_id}"

    total = await User.all().count()
    users = await User.all().offset(0).limit(20)
    pages = ceil(total / 20)
    safety_users_list = list(map(SafetyUser.model_validate, users))
    safety_users_pagination = Pagination[SafetyUser](
        total=total,
        pages=pages,
        current=1,
        size=20,
        records=safety_users_list,
    )
    await redis.setex(redis_key, timedelta(days=1), safety_users_pagination.model_dump_json())


async def do_cache_recommend_users(redis: Redis) -> None:
    cache_user_func = partial(cache_recommend_user, redis)
    tasks = list(map(cache_user_func, main_user_id_list))
    await gather(*tasks)
