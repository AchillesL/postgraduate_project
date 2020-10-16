# 用KNN算法做鸢尾花的分类预测

import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris = datasets.load_iris()
iris_X = iris.data
iris_y = iris.target

# print(iris_X[:2,:])   #花的属性
# print(iris_y)         #花的类别-0，1，2，3

#测试集占30%的比例
X_train,X_test,y_train,y_test = train_test_split(iris_X,iris_y,test_size=0.3)

# print(y_train)

knn = KNeighborsClassifier()
knn.fit(X_train,y_train)

print(knn.predict(X_test))
print(y_test)
