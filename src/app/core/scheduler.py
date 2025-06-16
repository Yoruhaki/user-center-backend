from apscheduler.schedulers.asyncio import AsyncIOScheduler
from functools import lru_cache

from redis.asyncio import Redis

from src.app.jobs import do_cache_recommend_users


@lru_cache
def get_scheduler():
    return AsyncIOScheduler()


scheduler = get_scheduler()


def start_scheduler(redis: Redis):
    # test
    # scheduler.add_job(
    #     do_cache_recommend_users,
    #     'interval',
    #     seconds=10,
    #     id='cache_recommend_users',
    #     args=[redis]
    # )
    scheduler.add_job(
        do_cache_recommend_users,
        'cron',
        day_of_week='*',
        hour=23,
        minute=58,
        second=59,
        id='cache_recommend_users',
        args=[redis]
    )
    scheduler.start()


def shutdown_scheduler():
    scheduler.shutdown()
