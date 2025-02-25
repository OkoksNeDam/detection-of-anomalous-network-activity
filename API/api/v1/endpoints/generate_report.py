import io

import httpx
import numpy as np
import pandas as pd
import torch
import joblib
from fastapi import APIRouter, UploadFile, File, HTTPException
from torch.utils.data import DataLoader

import config
from ml.datasets.datasets import PandasDataset
from ml.models.autoencoders import AE

from config import IRE

router = APIRouter()


@router.post("/generate", description='Получить отчет об аномалиях в загруженных потоках.')
async def generate_report(uploaded_file: UploadFile = File(...)):
    flow_processor_path = "http://localhost:8000/api/v1/processor/process_flow"
    try:
        client = httpx.AsyncClient()
        response = await client.post(flow_processor_path, files={'uploaded_file': (uploaded_file.filename,
                                                                                   uploaded_file.file)})
        response.raise_for_status()
        df = pd.read_csv(io.BytesIO(response.content))
        df = df.dropna()
        loaded_model = AE()
        loaded_model.load_state_dict(torch.load("trained/saved_models/saved_model.pickle", weights_only=True))
        loaded_model.eval()
        scaler = joblib.load('trained/saved_scalers/saved_scaler.pkl')
        scaled_data = scaler.transform(np.array(df))
        dataset = PandasDataset(scaled_data)
        dataloader = DataLoader(dataset, batch_size=1)

        ire_list = []

        loss_function = torch.nn.MSELoss()
        for feat in dataloader:
            ire = loss_function(feat, loaded_model(feat)).detach().numpy()
            ire_list += [float(ire)]

        return {"trained_ire": config.IRE, "ire_list": ire_list}

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail=str(e.response.json()["detail"])) from e
