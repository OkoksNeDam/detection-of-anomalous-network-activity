from fastapi import FastAPI

from api.v1.api import api_v1_router

app = FastAPI()

app.include_router(api_v1_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}