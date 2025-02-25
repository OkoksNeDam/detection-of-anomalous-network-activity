from dotenv import load_dotenv
import os

load_dotenv()

IRE = float(os.getenv('IRE'))
SAVED_MODELS_PATH = os.getenv('SAVED_MODELS_PATH')
SAVED_SCALER_PATH = os.getenv('SAVED_SCALER_PATH')