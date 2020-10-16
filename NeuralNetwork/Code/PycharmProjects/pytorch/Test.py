import torch

# 定义LiearModel，继承父类torch.nn.Module
# __init__与forward方法必须实现
class LinearModel(torch.nn.Module):
    def __init__(self):
        super(LinearModel, self).__init__()
        # 输入特征数为2，输出特征数为1
        self.linear = torch.nn.Linear(2, 1)

    def forward(self, x):
        y_pred = self.linear(x)

        return y_pred

model = LinearModel()
x_data = torch.Tensor([[137.97, 3], [104.50, 2], [100.00, 2], [124.32, 3], [79.20, 1], [99.00, 2], [124.00, 3],[114.00, 2],
                       [106.69, 2], [138.05, 3], [53.75, 1],  [46.91, 1],  [68.00, 1], [63.02, 1], [81.26, 2], [86.21, 2]])

y_data = torch.Tensor([[145.00], [110.00], [93.00], [116.00], [65.32], [104.00], [118.00], [91.00],
                        [62.00], [133.00], [51.00], [45.00], [78.50], [69.65], [75.69],[95.30]])

criterion = torch.nn.MSELoss(size_average = False)
optimizer = torch.optim.SGD(model.parameters(),lr=0.0001)

for epoch in range(10):
    y_pred = model(x_data)
    loss = criterion(y_pred,y_data)
    print(epoch,loss.item())

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

print('w = ', model.linear.weight.item())
print('b = ', model.linear.bias.item())




