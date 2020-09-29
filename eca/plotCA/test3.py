import matplotlib.pyplot as plt
from sklearn import datasets

X_train, y_train = datasets.load_breast_cancer(return_X_y=True)  # 载入数据集
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, marker='o', s=40,
            cmap=plt.cm.Spectral)  # c--color，s--size,marker点的形状
plt.show()
