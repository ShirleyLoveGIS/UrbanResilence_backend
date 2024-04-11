#导入传播数据及影响因素数据线性回归分析需要的库包
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from pylab import*
#导入读取因变量数据
input_url = "D:\data\世界地图shp/redu_export.csv"
input = pd.read_csv(input_url)
shp_url = "D:\data\世界地图shp\世界地图.shp"
shp = gpd.read_file(shp_url)


#使用公共建合并shp属性表及外置表格
shp_df = shp.merge(input,left_on="CH",right_on="国家名")
shp_df.plot(column="redu_2021",cmap="bwr_r",vmin=0,vmax=100,legend=True,figsize=(10,10))
plt.title('传播热度红蓝图')
plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False
plt.tight_layout()
plt.savefig('传播热度红蓝图.png',bbox_inches='tight',pad_inches=0.0)
plt.show()
plt.close()

#导入线性回归模型分析需要的库包
#并输出散点图
import statsmodels.formula.api as smf
print(shp_df.columns)
#模型一：选择传播热度作为因变量，传播热度作为因变量
plt.scatter(shp_df.redu_2021, shp_df.export_2021)
plt.xlabel("孔子文化传播热度")
plt.ylabel("中国对外出口额")
plt.Text(0, 0.5, '孔子文化传播热度')
plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False
plt.tight_layout()
plt.savefig('孔子文化传播热度.png',bbox_inches='tight',pad_inches=0.0)
plt.show()

#指定模型一
from scipy.stats import pearsonr
#print('即将输出模型一的相关参数：')
print(pearsonr(shp_df.export_2021, shp_df.redu_2021))#简单解释模型，一个自变量和一个因变量
model_1 = smf.ols(formula='redu_2021 ~ 1 + export_2021', data=shp_df).fit()#设置线性回归的表达式模型，~1表示添加截距
print(model_1.summary())
#获取预测值
pred_1 = model_1.fittedvalues

#预测图
resid = model_1.resid


#qq图
import scipy.stats as stats
plt.figure()
stats.probplot(resid, dist="norm", plot=plt)
plt.title('传播热度分布图')
plt.xlabel('')
plt.ylabel('')
plt.tight_layout()
plt.savefig('传播热度分布图.png',bbox_inches='tight',pad_inches=0.0)
plt.show()
plt.close()
 
#得出模型的线性函数图像
from sklearn.linear_model import LinearRegression  
x=shp_df.redu_2021
y=shp_df.export_2021
regressor = LinearRegression()
regressor = regressor.fit(np.reshape(x,(-1, 1)),np.reshape(y,(-1, 1)))
print(regressor.coef_, regressor.intercept_) 
plt.scatter(shp_df.redu_2021, shp_df.export_2021)
plt.plot(np.reshape(x,(-1,1)), regressor.predict(np.reshape(x,(-1,1))))
plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False
plt.xlabel('孔子文化传播热度')
plt.ylabel('中国对外出口额')
plt.tight_layout()
plt.savefig('孔子文化传播热度图.png',bbox_inches='tight',pad_inches=0.0)
plt.show()
#print(x.values)
#print(y.values)
