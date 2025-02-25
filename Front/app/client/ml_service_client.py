from typing import List

import httpx


class MLServiceClient:
    _instance = None

    def __new__(cls, base_url=None):

        if cls._instance is None:
            if base_url is None:
                raise ValueError("base_url must be provided on the first initialization.")
            cls._instance = super(MLServiceClient, cls).__new__(cls)
            cls._instance.base_url = base_url
        return cls._instance

    def __init__(self, base_url=None):
        if hasattr(self, 'base_url'):
            return
        self.base_url = base_url

    def _get_url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def model_upload(self, model_file) -> None:
        url = self._get_url('/api/v1/model/upload')
        response = httpx.post(url, files=model_file, timeout=None)
        response.raise_for_status()

    def get_models_list(self) -> List[str]:
        url = self._get_url('/api/v1/model/get_models_list')
        response = httpx.post(url, timeout=None)
        response.raise_for_status()

        return response.json()['models']

    def get_anomalies_report(self, file, model):
        url = self._get_url('/api/v1/report/generate')
        payload = {'uploaded_model': model}
        response = httpx.post(url, files=file, data=payload, timeout=None)
        response.raise_for_status()

        return response.json()