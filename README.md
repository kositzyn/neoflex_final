# Booking Analyser App
Final project assignment. FastAPI, SQLAlchemy, Pandas and NumPy is used for solving this task.


How to start:

1. Install all requirements:
```
pip install -r requirements.txt
```

2. Run start ASGI-server. I used uvicorn
```
uvicorn main:app
```

3. Open http://localhost:8000/docs in your browser and check API

<b>Important!</b> You need to log in for using API. You can use:
```
username: root
password: root
```
Or create new user. Use "auth" section of API

### Or use Docker:

Create container:
```
docker build . -t neo_hotel
```
Run Container:
```
docker run -d -p 8000:8000 neo_hotel
```
Then, Open http://localhost:8000/docs in your browser and check API.
You need to log in either.


## Structure of project

* ### /app
  * user - Authentication, register, login and logout
  * csv_tool - Validation, upload, delete csv-file for analysing on server
  * booking - Endpoints for necessary functionalities. Descriptions of endpoints
  in Swagger or ReDoc

* ### /demo
    * hotel_booking_data.csv - Valid demo file for checking functionalities of app.
  

* ### /models
  * Models for SQLAlchemy and Alembic. I use alembic for creating database.
  If you want, you can create empty hotel.db like this:
  ```
  alembic init alembic
  alembic revision --autogenerate -m "Create db"
  alembic upgrade head
  ```

* ### /
    * main.py - The main file of application. Run it via uvicorn, gunicorn etc..
    * requirements.txt - All necessary requirements for running application
    * hotel.db - sqlite database which is ready for testing 
    * alembic.ini - configuration file for alembic
    * Dockerfile - configuration file for creating docker-container