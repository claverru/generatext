from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Dropout


def lstm_model():
	model = Sequential()
	model.add(Embedding())
	model.add(LSTM())
	model.add(LSTM())
	model.add(Dropout(0.2))
	model.add(Dense())
	model.add(Dropout(0.2))
	model.add(Dense())
	model.compile()
	return model