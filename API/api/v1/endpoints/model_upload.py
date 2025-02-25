import os.path
import shutil

from fastapi import APIRouter, UploadFile, File

import config

router = APIRouter()


@router.post("/upload", description='Загрузить обученную модель.')
async def upload_model(model_file: UploadFile = File(...)):
    file_location = os.path.join(config.SAVED_MODELS_PATH, model_file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(model_file.file, buffer)

    return {"message": "Модель была успешно загружена."}