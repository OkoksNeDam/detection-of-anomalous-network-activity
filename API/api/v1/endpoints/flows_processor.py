import os
import shutil
import zipfile
from io import BytesIO

from fastapi import APIRouter, UploadFile, File, HTTPException, status

from exceptions.file_exceptions import FileExtensionException
from services.flow_directory_processor_service import FlowDirectoryProcessorService
from services.flow_file_processor_service import FlowPCAPProcessorService

router = APIRouter()


@router.post("/process_flow", description='Обработать поток из zip файла и сохранить в csv файл.')
async def process_flow(uploaded_file: UploadFile = File(...)):
    # Путь к файлу на выходе.
    output_filepath = "processed_data.csv"
    # Куда распаковывать архив.
    extracted_zip_folder_filepath = "."

    # Вытаскиваем имя zip файла, которое становится именем для папки с данными.
    uploaded_dir_path = os.path.splitext(uploaded_file.filename)[0]
    try:
        with zipfile.ZipFile(BytesIO(await uploaded_file.read()), 'r') as zip_file:
            zip_file.extractall(extracted_zip_folder_filepath)

        flow_directory_processor = FlowDirectoryProcessorService(directory_path=uploaded_dir_path,
                                                                 flow_processor=FlowPCAPProcessorService)
        flow_directory_processor.process()
        csv_streaming_response = flow_directory_processor.save_csv(output_filepath)
        return csv_streaming_response

    except (zipfile.BadZipFile, FileExtensionException) as e:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=str(e)) from e
    finally:
        if os.path.isdir(uploaded_dir_path):
            # Удаляем папку с распакованным ZIP-архивом.
            shutil.rmtree(uploaded_dir_path)
