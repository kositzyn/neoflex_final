from fastapi import FastAPI

from app.csv_tool.routes import csv_files_route
from app.booking.routes import bookings_routes
from app.user.config import auth_backend
from app.user.config import fastapi_users
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


