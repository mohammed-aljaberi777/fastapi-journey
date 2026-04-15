from fastapi import APIRouter, HTTPException, status
from database.connection import Database
from models.users import User, UserSignIn

user_router = APIRouter()

user_db = Database(User)


@user_router.post("/signup")
async def sign_up(user: User):
    existing = await User.find_one(User.email == user.email)

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    await user_db.save(user)
    return {"message": "User created successfully"}


@user_router.post("/signin")
async def sign_in(user: UserSignIn):
    existing = await User.find_one(User.email == user.email)

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if existing.password == user.password:
        return {"message": "User signed in successfully"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )