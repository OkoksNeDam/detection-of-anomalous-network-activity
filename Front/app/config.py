import os

from client.ml_service_client import MLServiceClient

API_URL = os.getenv('API_URL', 'http://127.0.0.1:8000')
app_client = MLServiceClient(API_URL)


def get_app_client():
    return app_client
