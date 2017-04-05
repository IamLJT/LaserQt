# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from mpl_toolkits.mplot3d import Axes3D
FONT = FontProperties(fname=("LaserQt_Font/wqy-microhei.ttc"), size=10)

dataframe = pd.read_csv('data.txt', header=None)
dataframe.dropna()

matrix = dataframe.as_matrix()
print(type(matrix))

fig = plt.figure()
fig.set_facecolor("white")
fig.set_edgecolor("black")
axes = Axes3D(fig)
axes.set_xlim([np.min(matrix[:, 0]), np.max(matrix[:, 0])])
axes.set_ylim([np.min(matrix[:, 1]), np.max(matrix[:, 1])])
axes.set_zlim([np.min(matrix[:, 2]), np.max(matrix[:, 2])])
axes.set_xticks([])
axes.set_yticks([])
axes.set_zticks([])
axes.set_xlabel("加工板X方向", fontproperties=FONT, fontsize=9)
axes.set_ylabel("加工板Y方向", fontproperties=FONT, fontsize=9)
axes.set_zlabel("加工板Z方向", fontproperties=FONT, fontsize=9)
axes.grid(True, which="both")
axes.scatter(matrix[::10, 0], matrix[::10, 1], matrix[::10, 2], c='red')
plt.show()
