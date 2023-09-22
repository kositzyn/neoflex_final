import requests
import json

from sqlalchemy import create_engine

from app.database import DATABASE_URL

url = 'http://localhost:8000/auth/register/'

data = {"username": "root",
        "email": "root",
        "csvfile": "demo",
        "password": "root",
        "is_active": False,
        "is_superuser": True,
        "is_verified": False}

response = requests.post(url, data=json.dumps(data))
if response.status_code == 201:
        print('User root has been created successfully')


