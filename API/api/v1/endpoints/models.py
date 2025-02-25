import glob
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


@router.post("/get_models_list", description='Получить список загруженных моделей.')
async def get_models_list():
    files = []
    for f in os.listdir(config.SAVED_MODELS_PATH):
        if os.path.isfile(os.path.join(config.SAVED_MODELS_PATH, f)) and not f.startswith('.'):
            files += [f]
    return {"models": files}
