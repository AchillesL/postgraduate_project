import torch
import numpy as np

net = torch.nn.Sequential(
    torch.nn.Linear(3,1),
    torch.nn.Sigmoid()
)

X_data = torch.tensor([[0,0,1],[0,1,1],[1,0,1],[1,1,1]],dtype=torch.float32)
y_data = torch.tensor([[0],[1],[1],[0]],dtype=torch.float32)

c = torch.nn.MSELoss()
g = torch.optim.Adam(net.parameters(),lr = 0.01)

for e in range(10000):
    p = net(X_data)
    loss = c(p,y_data)

    g.zero_grad()
    loss.backward()
    g.step()

print(net(torch.from_numpy(np.array([[1,0,0]],dtype=np.float32))))


