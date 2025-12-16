import numpy as np
from corrosion_model import CorrosionModel

X = np.array([
    [5, 0.7],   # лет, агрессивность
    [10, 0.9],
    [15, 1.2]
])

y = np.array([10, 25, 45])  # глубина %

model = CorrosionModel()
model.train(X, y)

print(model.predict([[20, 1.0]]))
