from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from src.app.models import Users

UsersPydantic = pydantic_model_creator(Users)
UsersPydanticList = pydantic_queryset_creator(Users)
