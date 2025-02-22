import os
import shutil
import zipfile
from io import BytesIO
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.responses import JSONResponse

router = APIRouter()


@router.post("/upload/", description='Обработать поток из папки и сохранить в csv файл.')
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != 'application/zip':
        return {"error": "File type not supported. Please upload a ZIP file."}

    try:
        # Читаем содержимое ZIP-архива.
        with zipfile.ZipFile(BytesIO(await file.read())) as zip_file:
            zip_file.extractall('.')

        current_directory = os.getcwd()

        # Получаем список файлов и папок в текущей директории
        files_and_folders = os.listdir(current_directory)

        # Выводим файлы и папки
        for item in files_and_folders:
            print(item)

        return {"message": "1"}

    finally:
        # Удаляем папку с распакованным ZIP-архивом.
        shutil.rmtree(os.path.splitext(file.filename)[0])

