from sklearn import datasets
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
import matplotlib.pyplot as plt
import numpy as np


loaded_data = datasets.load_boston()
# data_X = loaded_data.data
# data_y = loaded_data.target

data_X = [[137.97, 3], [104.50, 2], [100.00, 2], [124.32, 3], [79.20, 1], [99.00, 2], [124.00, 3], [114.00, 2],
                   [106.69, 2], [138.05, 3], [53.75, 1], [46.91, 1], [68.00, 1], [63.02, 1], [81.26, 2], [86.21, 2]]
data_y = [[145.00], [110.00], [93.00], [116.00], [65.32], [104.00], [118.00], [91.00],
                   [62.00], [133.00], [51.00], [45.00], [78.50], [69.65], [75.69], [95.30]]

# data_X = preprocessing.scale(data_X)

model = LinearRegression()
model.fit(data_X,data_y)
print(model.coef_)          #输出权重W
print(model.intercept_)     #输出截距b
print(model.score(data_X,data_y))
