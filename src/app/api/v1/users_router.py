from fastapi import APIRouter, Path

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users_list():
    return {"users": ["all_users"]}


@router.get("/{user_id}")
async def get_user_by_id(user_id: int = Path(...)):
    return {"user": user_id}


@router.post("/")
async def create_user(user):
    return {"user": user}


@router.put("/{user_id}")
async def update_user_by_id(user_id, user):
    return {"user": user}


@router.delete("/{user_id}")
async def delete_user_by_id(user_id):
    return {"message": "success"}
