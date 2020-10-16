import numpy as np
from sklearn.preprocessing import normalize

data = np.array([ [1000, 1, 0.5],[765, 5, 0.35], [800, 7, 0.09], ])
data = normalize(data, axis=0, norm='max')

print(data)