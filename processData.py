from sklearn.preprocessing import MinMaxScaler
from typing import Tuple
import yfinance as yf
import pandas as pd
import numpy as np
import joblib
import os


scaledFile:str = os.path.join("modelFiles", "scaler.pkl")
modelFiles:str = "modelFiles"


def downloadData() -> pd.DataFrame:
    data = yf.download('MSFT', start='2010-01-01', end='2025-01-01')
    data = data[['Close']]
    return data   # Apenas preço de fechamento

    
def getScaler() -> MinMaxScaler:
    
    if os.path.exists(scaledFile):
        scaler = joblib.load(scaledFile)
    else:
        scaler = MinMaxScaler(feature_range=(0, 1))
        joblib.dump(scaler, scaledFile)

    return scaler


def create_dataset(data, time_step=60) -> Tuple[np.ndarray, np.ndarray]:
    
    x, y = [], []
    for i in range(len(data) - time_step - 1):
        x.append(data[i:(i + time_step), 0])
        y.append(data[i + time_step, 0])
    
    return np.array(x), np.array(y)