from sklearn.metrics import mean_absolute_error, mean_squared_error
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import LSTM, Dense, Dropout # type: ignore
from sklearn.model_selection import train_test_split
from processData import *
import os


data = downloadData()

if data is None:
    quit()

scaled_data = getScaler().fit_transform(data)
    
X, y = create_dataset(scaled_data, 60)
X = X.reshape(X.shape[0], X.shape[1], 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)


model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(1)
])


model.compile(optimizer="adam", loss="mean_squared_error", metrics=["accuracy"])
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
model.save(os.path.join("modelFiles", "my_model.keras"))

# IMPLEMENTAR AS MÉTRICAS AQUI