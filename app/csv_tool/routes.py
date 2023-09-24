import numpy as np
from fastapi import APIRouter, Depends
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException
from fastapi import status
from sqlalchemy import update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.csv_tool.validation import is_csv_valid
from app.csv_tool.validation import create_temporary

import os

from app.database import get_async_session
from app.user.config import fastapi_users
from app.user.models import User
from models.models import user, booking

from app.booking.utils import booking_date

import pandas as pd

current_user = fastapi_users.current_user()

csv_files_route = APIRouter(
    prefix='/csv_files',
    tags=['CSV Files Tools'],
    dependencies=[Depends(current_user)]
)


@csv_files_route.post(
    '/upload',
    summary='Upload and save csv file',
    description='This API provides to upload and save csv file on server',
    status_code=status.HTTP_201_CREATED
)
async def upload_and_save_csv(csv_file: UploadFile = File(...)):
    create_temporary()
    first_line = csv_file.file.readline()
    if not is_csv_valid(first_line):
        raise HTTPException(status_code=400,
                            detail="File haven't validated. Try again")

    try:
        contents = await csv_file.read()
        with open('temporary/' + csv_file.filename, "wb") as file:
            file.write(first_line)
            file.write(contents)
    except Exception:
        raise HTTPException(status_code=400,
                            detail="Can't upload this file. Try again or ask your system administrator for help")
    finally:
        await csv_file.close()

    return {
        "message": f"Successfully uploaded file: {csv_file.filename}"
    }


@csv_files_route.get(
    '/list',
    summary='List of all uploaded csv files',
    description='This API provides to get list of all uploaded and saved csv files on server',
    status_code=status.HTTP_200_OK
)
async def get_all_csv():
    if not os.path.exists('temporary'):
        raise HTTPException(status_code=404,
                            detail="No any files have been uploaded yet")
    else:
        uploaded_files_lst = []
        for root, dirs, files in os.walk("temporary"):
            for filename in files:
                if filename != '.gitignore':
                    uploaded_files_lst.append(filename)
        return {
            "status": "200 - OK",
            "Message": f"You have {len(uploaded_files_lst)} files",
            "files": uploaded_files_lst
        }


@csv_files_route.delete(
    '/delete/all',
    summary='Delete all uploaded csv files',
    description='This API provides to delete all uploaded and saved csv files on server',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_all_uploaded_files():
    if not os.path.exists('temporary'):
        HTTPException(status_code=404,
                      detail="You have no any uploaded files")
    count = 0
    try:
        for root, dirs, files in os.walk("temporary"):
            for filename in files:
                if filename != '.gitignore':
                    os.remove("temporary/" + filename)
                    count += 1

        return {"message": f"All {count} file(s) have been deleted"}
    except Exception:
        raise HTTPException(status_code=500,
                            detail="Can't do this operation. Ask your system administrator")


@csv_files_route.delete(
    '/delete/{filename}',
    summary='Delete uploaded csv files named as \'filename\'',
    description='This API provides to delete uploaded and saved csv file with name "filename" on server',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_csv_file(filename: str):
    filename = filename.replace('/', '')  # Little basic safety
    try:
        os.remove("temporary/" + filename)
        return {"message": f"File {filename}  has been deleted"}
    except Exception:
        raise HTTPException(status_code=404,
                            detail="File not found!")


@csv_files_route.post(
    '/set/{filename}',
    summary='Set uploaded csv as file for analysis',
    description='This API provides to set uploaded csv file for analysing (ability to use /bookings... endpoints)',
    status_code=status.HTTP_201_CREATED
)
async def set_file_for_analysis(filename: str,
                                _user: User = Depends(current_user),
                                session: AsyncSession = Depends(get_async_session)):
    filename = filename.replace('/', '')  # Little basic safety
    if os.path.isfile("temporary/" + filename):
        try:
            stmt = update(user).where(user.c.id == _user.id).values(csvfile=filename)
            await session.execute(stmt)

            stmt = delete(booking)
            await session.execute(stmt)

            new_df = pd.DataFrame()

            df = pd.read_csv('demo/hotel_booking_data.csv')

            new_df['booking_date'] = np.vectorize(booking_date)(df['arrival_date_day_of_month'],
                                                                df['arrival_date_month'],
                                                                df['arrival_date_year'],
                                                                df['lead_time'])
            new_df['length_of_stay'] = df['stays_in_week_nights'] + df['stays_in_weekend_nights']
            new_df['guest_name'] = df['name']
            new_df['daily_rate'] = df['adr']

            result = new_df.to_dict()

            for i in range(len(new_df)):
                stmt = insert(booking).values(booking_date=result['booking_date'][i],
                                              length_of_stay=result['length_of_stay'][i],
                                              guest_name=result['guest_name'][i],
                                              daily_rate=result['daily_rate'][i])
                await session.execute(stmt)

            await session.commit()

            return {"message": f"File {filename} has been set as file for analysing",
                    "db": f'Table "booking" in database has been filled'}
        except Exception:
            raise HTTPException(status_code=400,
                                detail="Something is going wrong. Try again")

    else:
        raise HTTPException(status_code=404,
                            detail="File not found!")


@csv_files_route.get(
    '/get_current',
    summary='Get current csv file to be set for analysing',
    description='This API provides to get current csv file which be set for analysing',
    status_code=status.HTTP_200_OK
)
async def get_current_file(_user: User = Depends(current_user)):
    return {"file": _user.csvfile}
