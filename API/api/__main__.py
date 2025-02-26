import uvicorn
from fastapi import FastAPI

from api.v1.api import api_v1_router

app = FastAPI()

app.include_router(api_v1_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("api.__main__:app", host="0.0.0.0", port=8000)
