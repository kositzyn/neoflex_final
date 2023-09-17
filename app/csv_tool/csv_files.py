from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import os

csv_files_route = APIRouter(
    prefix='/csv_files',
)


def create_temporary():
    """
    Check existing of /temporary. If not, create it
    and add .gitignore file for this directory

    /temporary is directory for uploaded files
    """
    if not os.path.exists('temporary'):
        os.mkdir('temporary')
        with open('temporary/.gitignore', 'w+') as git_ignore_file:
            git_ignore_file.writelines('*')


@csv_files_route.post(
    '/upload',
    summary='Upload and save csv file',
    description='This API provides to upload and save csv file on server'
)
async def upload_and_save_csv(csv_file: UploadFile = File(...)):
    create_temporary()
    try:
        contents = await csv_file.read()
        with open('temporary/' + csv_file.filename, "wb") as file:
            file.write(contents)
    except Exception:
        return {
            "message": "Something is going wrong"
        }
    finally:
        await csv_file.close()

    return {
        "message": f"Successfully uploaded file: {csv_file.filename}"
    }
