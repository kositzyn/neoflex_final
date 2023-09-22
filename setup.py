import requests
import json

url = 'http://127.0.0.1:8000/auth/register/'

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

