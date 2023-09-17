from fastapi import FastAPI

from app.csv_tool.csv_files import csv_files_route


app = FastAPI()

app.include_router(csv_files_route)

