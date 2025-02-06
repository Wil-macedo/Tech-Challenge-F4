from sklearn.metrics import r2_score, mean_squared_error
from tensorflow.keras.models import Sequential, load_model # type: ignore
from tensorflow.keras.layers import LSTM, Dense, Dropout # type: ignore
from sklearn.model_selection import train_test_split
from processData import *
import mlflow
import math
import os

mlflow.set_experiment("Tech Challenge F4")


data = downloadData()

if data is None:
    quit()

scaled_data = getScaler().fit_transform(data)
    
x, y = create_dataset(scaled_data, 60)
x = x.reshape(x.shape[0], x.shape[1], 1)
xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2, shuffle=False)


# parameters = {
#     "epochs":10, 
#     "batch_size":32
# }
with mlflow.start_run():
    
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(xTrain.shape[1], 1)),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(1)
    ])
    
    # mlflow.tensorflow.log_model(model, "modeltensorflow")
    mlflow.tensorflow.autolog()  # Ativa o AutoLogging


    model.compile(optimizer="adam", loss="mean_squared_error", metrics=["accuracy"])
    model.fit(xTrain, yTrain, epochs=15, batch_size=32, validation_data=(xTest, yTest))
    model.save(os.path.join("modelFiles", "my_model.keras"))

    predicts = model.predict(xTest)
    
    mse = mean_squared_error(yTest, predicts)
    rmse = math.sqrt(mse)
    r2s = r2_score(yTest, predicts)

    mlflow.log_metric("mse", mse)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2s", r2s)