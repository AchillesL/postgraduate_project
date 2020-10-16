import numpy as np
import torch
from matplotlib import pyplot as plt

num_input = 2
num_examples = 1000

true_w = [2, -3.4]
true_b = 4.2

# normal用法: numpy.random.normal(loc=0,scale=1e-2,size=shape)
features = torch.from_numpy(np.random.normal(0, 1, (num_examples, num_input)))

labels = true_w[0] * features[:, 0] + true_w[1] * features[:, 1] + true_b
labels += torch.from_numpy(np.random.normal(0, 0.01, size=labels.size()))

plt.scatter(features[:, 1].numpy(), labels.numpy(), 1)
