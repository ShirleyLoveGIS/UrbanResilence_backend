from pulp import *
import numpy as np
import geopandas as gp
import pandas as pd
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt


#读入shp文件,并展示
geo_shp = gp.read_file("D:\data\世界地图shp\世界地图_空间优化1.shp")
bl_df = pd.read_csv('D:\data\世界地图shp\总表虚填.csv')
shp_df =geo_shp.merge(bl_df,left_on="CH",right_on="国家名")
print(shp_df.shape)


#以孔子学院的传播热度的倒数值，构建距离矩阵
#意味着：传播热度越低的国家越需要建设孔子文化传播设施
demand = np.arange(0,148,1)
facilities = np.arange(0,148,1)
coords = list(zip(shp_df.xx,shp_df.yy))
d = cdist(coords,coords)
h =101/(shp_df.redu_2020.values+1)
X = LpVariable.dicts('X_%s',(facilities),cat='Binary')
Y = LpVariable.dicts('Y_%s_%s', (demand,facilities),cat='Binary')
#要建设的孔子文化传播设施数量
p = 20 
#构建孔子学院建设的空间优化问题
prob = LpProblem('P_Median', LpMinimize)
prob += sum(sum(h[i] * d[i][j] * Y[i][j] for j in facilities) for i in demand)
prob += sum([X[j] for j in facilities]) == p
for i in demand:
    prob += sum(Y[i][j] for j in facilities) == 1
for i in demand:
    for j in facilities:
        prob +=  Y[i][j] <= X[j]
prob.solve()
rslt=[]
for v in prob.variables():
    subV = v.name.split('_')
    if subV[0] == "X" and v.varValue == 1:
        rslt.append(int(subV[1]))
# 获取孔子文化传播设施的几何信息，构建几何对象
fac_loc =shp_df.iloc[rslt,:]
#设施位置预测求解结果展示
fig, ax = plt.subplots(figsize=(15,15))
shp_df.plot(ax=ax)
fac_loc.centroid.plot(ax=ax,color="red",markersize=30,marker="*")
plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False
plt.title('孔子文化传播设施最佳空间排列图-以设施个数为约束')
plt.tight_layout()
plt.savefig('孔子文化传播设施最佳空间排列图-以设施个数为约束.png',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
plt.show()
plt.close()
#预测点x坐标
print(fac_loc.centroid.x)
#预测点y坐标
print(fac_loc.centroid.y)

