from fastapi import APIRouter
from api.v1.endpoints import flows_processor, model_upload, generate_report

api_v1_router = APIRouter()

api_v1_router.include_router(flows_processor.router, prefix="/processor")
api_v1_router.include_router(generate_report.router, prefix="/report")
api_v1_router.include_router(model_upload.router, prefix="/model")