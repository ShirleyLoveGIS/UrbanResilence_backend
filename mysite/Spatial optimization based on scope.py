from pulp import *
import numpy as np
import geopandas as gp
import pandas as pd
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
#读入shp文件
geo_shp = gp.read_file("D:\data\世界地图shp\世界地图_空间优化1.shp")
bl_df = pd.read_csv('D:\data\世界地图shp\总表虚填.csv')
shp_df =geo_shp.merge(bl_df,left_on="CH",right_on="国家名")
print(shp_df.shape)


demand = np.arange(0,148,1)
facilities = np.arange(0,148,1)
#以孔子学院的传播热度的倒数值，构建距离矩阵
#意味着：传播热度越低的国家越需要建设孔子文化传播设施
coords =list(zip(shp_df.xx,shp_df.yy))
d = cdist(coords,coords)
# 设置的孔子文化传播设施的覆盖范围（左右10度）
Dc = 20 
a = np.zeros(d.shape)
a[d <= Dc] = 1
a[d > Dc] = 0
X = LpVariable.dicts('X_%s',(facilities),cat='Binary')
#创建该条件下的孔子文化传播
prob = LpProblem('Set_Covering', LpMinimize)
#最小化放置孔子文化传播设施的数量
prob += sum([X[j] for j in facilities])
for i in demand:
    prob += sum(a[i][j]*X[j] for j in facilities) >= 1
# 求解文化传播的最佳传播设施位置
prob.solve()
rslt = []
for v in prob.variables():
    subV = v.name.split('_')
    if subV[0] == "X" and v.varValue == 1:
        rslt.append(int(subV[1]))
# 获取求解的孔子文化传播设施的几何信息
fac_loc =shp_df.iloc[rslt,:]
#求解结果展示
fig, ax = plt.subplots(figsize=(15,15))
shp_df.plot(ax=ax)
fac_loc.centroid.plot(ax=ax,color="red",markersize=30,marker="*")
plt.title('孔子文化传播设施最佳空间排列图-以影响范围为约束')
plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False
plt.tight_layout()
plt.savefig('孔子文化传播设施最佳空间排列图-以影响范围为约束.png',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
plt.show()
plt.close()
#预测点x坐标
print(fac_loc.centroid.x)
#预测点y坐标
print(fac_loc.centroid.y)

