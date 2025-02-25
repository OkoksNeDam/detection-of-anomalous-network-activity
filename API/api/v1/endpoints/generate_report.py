import io
import os.path

import httpx
import numpy as np
import pandas as pd
import torch
import joblib
from fastapi import APIRouter, UploadFile, File, HTTPException, Form

import config
from ml.models.autoencoders import AE


router = APIRouter()


@router.post("/generate", description='Получить отчет об аномалиях в загруженных потоках.')
async def generate_report(uploaded_flow: UploadFile = File(...), uploaded_model: str = Form(...)):
    flow_processor_path = "http://localhost:8000/api/v1/processor/process_flow"
    try:
        client = httpx.AsyncClient()
        response = await client.post(url=flow_processor_path,
                                     files={'uploaded_file': (uploaded_flow.filename, uploaded_flow.file)},
                                     timeout=None)
        response.raise_for_status()
        df = pd.read_csv(io.BytesIO(response.content))
        df = df.dropna().reset_index(drop=True)
        flow_filenames = list(df['flow_name'])
        df = df.drop(columns=['flow_name'])
        loaded_model = AE()
        loaded_model.load_state_dict(torch.load(f=os.path.join(config.SAVED_MODELS_PATH, uploaded_model),
                                                weights_only=True,
                                                map_location=torch.device('cpu')))
        loaded_model.eval()
        scaler = joblib.load(config.SAVED_SCALER_PATH)
        scaled_data = scaler.transform(df)

        ire_list = []
        loss_function = torch.nn.MSELoss()
        for feat in scaled_data:
            feat = torch.Tensor(feat)
            ire = loss_function(feat, loaded_model(feat)).detach().numpy()
            ire_list += [float(ire)]

        return {"trained_ire": config.IRE, "ire_list": ire_list, "flow_filenames": flow_filenames}

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail=str(e.response.json()["detail"])) from e
