import pytest
from tortoise.contrib.test import initializer, finalizer


@pytest.fixture(scope="class", autouse=True)
def initialize_tests(request):
    initializer(["src.app.models.users"], db_url="sqlite://:memory:", app_label="models")
    request.addfinalizer(finalizer)
