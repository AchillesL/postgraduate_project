import numpy as np

# 1.定义数组
a = np.array([[1, 2, 3], [4, 5, 6]])
print(a)
# 1.1维度
print('number of dim:', a.ndim)
# 1.2形状
print('shape:', a.shape)
# 1.3总共有的元素
print('size:', a.size)
# 1.4默认值
b = np.ones((3, 4), dtype=np.int16)
c = np.zeros((3, 4), dtype=np.int16)
d = np.empty((3, 4))
# 1.5 重定义形状
e = np.arange(12).reshape(2, 6)
# 1.6生成线段
f = np.linspace(1, 10, 5)
# 1.7 arange的使用
print(a + np.arange(3))
# 1.8 数组每个元素平方
print('a^2:', a ** 2)
# 1.9判断数组某个元素小于某个值
print('a<5:', a < 5)
# 1.10矩阵元素乘法&矩阵乘法
print('矩阵元素乘法:', a * np.arange(1, 7).reshape(2, 3))
print('矩阵乘法:', a.dot(np.arange(1, 7).reshape(3, 2)))

# 2.最小值，最大值等运算
a = np.array([[1, 2, 3], [4, 5, 6]])
# 2.1最大值、最小值
print('max:', a.max(), 'min:', a.min())
# 2.2平均值
print('mean:', a.mean())
# 2.3 最大值的索引、最小值的索引
print('argmax:', a.argmax(), 'argmin:', a.argmin())
# 2.4 中位数
print('median:', np.median(a))
# 2.5 元素逐步累加、累差
print('累加:', a.cumsum(), '累差:', np.diff(a))
# 2.6 排序
print(np.sort(a))
# 2.7 举证转置
print('转置:', a.T)
# 2.8 截
print('截断:', a.clip(2, 5))

# 3.索引
print('索引:', a[1][2], a[1, 2])
# 3.1 从x到x，主要是以，为界限
print('索引2:', a[1, 0:2])
# 3.1.1 ':'号前省略默认为0，':'号后省略默认为1
print('索引省略:', a[1, :])
# 3.2 迭代行
for row in a:
    print('迭代行:', row)
# 3.3迭代列
for col in a.T:
    print('迭代列:', col)
# 3.4迭代元素
print('flat:', a.flatten())
for item in a.flat:
    print(item)

# 4. 合并
array1 = np.array([1, 1, 1])
array2 = np.array([2, 2, 2])
print('array垂直合并:', np.vstack((array1, array2)))
print('array水平合并:', np.hstack((array1, array2)))

