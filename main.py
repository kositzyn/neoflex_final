from fastapi import FastAPI
from fastapi import Depends

from app.csv_tool.routes import csv_files_route
from app.booking.routes import bookings_routes
from app.user.config import auth_backend
from app.user.config import fastapi_users
from app.user.models import User
from app.user.schemas import UserRead, UserCreate

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(csv_files_route)
app.include_router(bookings_routes)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}. {user.is_superuser}"
