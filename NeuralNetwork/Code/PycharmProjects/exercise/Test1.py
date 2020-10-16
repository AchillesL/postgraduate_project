import numpy as np

X = np.array([[0,0,1],[1,1,1],[1,0,1],[0,1,1]])
y = np.array([[0,1,1,0]]).T

np.random.seed(1)
# 生成3行1列的权重W
weights = np.random.random((3,1)) * 2 -1

for it in range(50000):
    z = np.dot(X,weights)
    output = 1/(1+np.exp(-z))

    error = y - output
    slope = output * (1-output)
    delta = error * slope

    weights += np.dot(X.T,delta)
print(weights)

