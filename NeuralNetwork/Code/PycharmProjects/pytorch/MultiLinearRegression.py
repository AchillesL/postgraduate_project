import numpy as np
import torch

# 创建NetModel类，继承自torch.nn.Module，必须实现__init__与forward方法
class NetModel(torch.nn.Module):
    def __init__(self):
        super(NetModel, self).__init__()
        # 输入数据特征数2，输出特征数为1
        self.linear1 = torch.nn.Linear(2, 1)

    def forward(self, x):
        x = self.linear1(x)
        return x

netModel = NetModel()

x_data = np.array([[137.97, 3], [104.50, 2], [100.00, 2], [124.32, 3], [79.20, 1], [99.00, 2], [124.00, 3], [114.00, 2],
                   [106.69, 2], [138.05, 3], [53.75, 1], [46.91, 1], [68.00, 1], [63.02, 1], [81.26, 2], [86.21, 2]],
                  dtype=np.float32)

y_data = np.array([[145.00], [110.00], [93.00], [116.00], [65.32], [104.00], [118.00], [91.00],
                   [62.00], [133.00], [51.00], [45.00], [78.50], [69.65], [75.69], [95.30]], dtype=np.float32)

x_train = torch.from_numpy(x_data)
y_train = torch.from_numpy(y_data)

# L1范数损失
# criterion = torch.nn.L1Loss()
# 使用均方损失函数
criterion = torch.nn.MSELoss()
# 训练所有参数、学习率0.01，L2正则化系数1e-5
optimizer = torch.optim.Adam(netModel.parameters(), lr=0.01)

for epoch in range(10000):
    prediction = netModel(x_train)
    loss = criterion(prediction, y_train)
    loss_value = loss.data.cpu().numpy()

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print('Epoch:{}, loss:{:.6f}'.format(epoch, loss_value))

print('prediction:{},real:{}'.format(netModel(x_train), y_data))
print('w:{},b:{}'.format(netModel.linear1.weight,netModel.linear1.bias))
