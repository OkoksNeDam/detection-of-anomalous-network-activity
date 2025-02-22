from fastapi import APIRouter
from api.v1.endpoints import flows_processor

api_v1_router = APIRouter()

api_v1_router.include_router(flows_processor.router, prefix="/flows_processor", tags=["flows_processor"])