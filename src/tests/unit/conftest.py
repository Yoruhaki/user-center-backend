from pytest import fixture
from tortoise.contrib.test import initializer, finalizer

from src.app.core import ORM_MODELS


@fixture(scope="session", autouse=True)
def initialize_tests(request):
    initializer(ORM_MODELS, db_url="sqlite://:memory:", app_label="models")
    request.addfinalizer(finalizer)
