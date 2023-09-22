# Booking Analyser App
Final project assignment. FastAPI, SQLAlchemy, Pandas and NumPy is used for solving this task.


How to start:

1. Install all requirements:
```
pip install -r requirements.txt
```
2. Use alembic for creating database and tables (Now it's not nessesary
due to existing hotel.db.)
```
alembic init alembic
alembic revision --autogenerate -m "Create database"
alembic upgrade head
```
3. Then start ASGI-server. I used uvicorn
```
uvicorn main:app
```
4. Run "setup.py" for creating user "root" (Not nessesary. Only in case if you create a new database with alembic)

5. Open http://localhost:8000/docs in your browser and check API


### Or use Docker:

Create container:
```
docker build . -t neo_hotel
```
Run Container:
```
docker run -d -p 8000:8000 neo_hotel
```
Then, Open http://localhost:8000/docs in your browser and check API


## Structure of project
*** IN PROGRESS ***
* ### /alembic


* ### /app

* ### /demo
    * hotel_booking_data.csv - Valid demo file for checking functionalities of app.
  

* ### /models

* ### /
    * main.py - The main file of application. Run it via uvicorn, gunicorn etc..
    * requirements.txt - All necessary requirements for running application