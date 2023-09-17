from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import os

csv_files_route = APIRouter(
    prefix='/csv_files',
    tags=['CSV Files Tools']
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


@csv_files_route.get(
    '/list',
    summary='List of all uploaded csv files',
    description='This API provides to get list of all uploaded and saved csv files on server'
)
async def get_all_csv():
    if not os.path.exists('temporary'):
        return {
            "status": "400 - No files found",
            "Message": "You have no any uploaded files"
        }
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
    description='This API provides to delete all uploaded and saved csv files on server'
)
async def delete_all_uploaded_files():
    if not os.path.exists('temporary'):
        return {
            "status": "400 - No files found",
            "Message": "You have no any uploaded files"
        }
    count = 0
    try:
        for root, dirs, files in os.walk("temporary"):
            for filename in files:
                if filename != '.gitignore':
                    os.remove("temporary/" + filename)
                    count += 1

        return {
            "status": "200 - OK",
            "message": f"All {count} file(s) have been deleted"
        }
    except Exception:
        return {
            "status": "500",
            "message": "Any problems with deleting files"
        }


@csv_files_route.delete(
    '/delete/{filename}',
    summary='Delete uploaded csv files named as \'filename\'',
    description='This API provides to delete uploaded and saved csv file with name "filename" on server'
)
async def delete_csv_file(filename: str):
    filename = filename.replace('/', '')  # Little basic safety
    try:
        os.remove("temporary/" + filename)
        return {
            "status": "200 - OK",
            "message": f"File {filename}  has been deleted"
        }
    except Exception:
        return {
            "status": "400",
            "message": "Any problems with deleting files. Check if it's correct filename"
        }
