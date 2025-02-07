from tensorflow.keras.models import load_model # type: ignore
from processData import modelFiles, getScaler
from processData import *
import mlflow
import os

# Modelo de dado para predição.
xData = [
    23.3007,
    23.3082,
    23.1652,
    22.9243,
    23.0824,
    22.7887,
    22.6382,
    22.8490,
    23.3082,
    23.2329,
    23.4136,
    23.0297,
    22.5930,
    21.8025,
    22.0735,
    22.2090,
    22.3370,
    21.9531,
    21.2153,
    21.3884,
    21.4261,
    21.5541,
    20.9593,
    21.0948,
    20.8690,
    21.0873,
    21.0722,
    21.1701,
    21.0271,
    21.4431,
    21.6246,
    21.9120,
    21.7608,
    21.7305,
    21.4280,
    21.6549,
    21.6322,
    21.6851,
    21.9498,
    21.5263,
    21.5263,
    21.6549,
    21.6246,
    21.6549,
    21.7834,
    21.9120,
    22.0709,
    22.1389,
    22.1541,
    22.2146,
    22.4112,
    22.3961,
    22.3810,
    22.3885,
    22.6003,
    22.4264,
    22.6986,
    22.4339,
    22.3810,
    22.5171
]

model = None

def laodModel():
    global model
    
    model = load_model(os.path.join(modelFiles, "my_model.keras"))
    model.summary()
        
        
def modelPredict(xData:list) -> int:
    global model
    

    if len(xData) == 60:
        
        if model is None:
            laodModel()
            
        xData = np.array(xData).reshape(-1, 1)
        xDataScaled = getScaler().transform(xData)
        xData = np.array(xDataScaled).reshape(1, 60, 1)

        prediction = model.predict(xData)
        prediction = getScaler().inverse_transform(prediction)[0][0]

        return int(round(prediction, 2))