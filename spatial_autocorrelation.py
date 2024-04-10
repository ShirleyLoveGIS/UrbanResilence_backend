#引入与孔子传播热度空间自相关功能相关的代码库
import esda
import os
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.plot import show as rshow
import seaborn as sns
from geopandas import GeoDataFrame
import libpysal as lps
import numpy 
import matplotlib.pyplot as plt
from shapely.geometry import Point
import matplotlib.image as mpimg
from matplotlib import animation
from pylab import*
import warnings
# 忽略警告信息，使输出更清楚
warnings.filterwarnings("ignore")

def mainref(df, y: str, factors: Sequence, relationship=False):
    
#传播热度及地图数据导入与处理
#读取世界地图.shp文件转出,读取的文件命名为变量gdf（geogataframe）
gdf = gpd.read_file('D:\data\世界地图shp\世界地图.shp')
bl_df = pd.read_csv('D:\data\世界地图shp\总表.csv')
geometry = [Point(xy) for xy in zip(bl_df.Longitude, bl_df.Latitude)]
crs = {'init': 'epsg:4326'}
bl_gdf = GeoDataFrame(bl_df, crs=crs, geometry=geometry)
bl_gdf['redu_2020'] = bl_gdf['redu_2020'].astype('float32')
sj_gdf = gpd.sjoin(gdf, bl_gdf, how='inner', op='intersects', lsuffix='left', rsuffix='right')
median_redu_2020_gb = sj_gdf['redu_2020'].groupby([sj_gdf['国家名']]).mean()
print('谷歌热度值为：')
print(median_redu_2020_gb)
gdf = gdf.join(median_redu_2020_gb, on='CH')
gdf.rename(columns={'redu_2020': 'redu'}, inplace=True)
#print(gdf.head(15))
# 处理缺失值
# 用0填充缺失的传播热度
#因为缺失数据的国家一般是因为其网名数量为0，其孔子文化传播热度也会相应为0
gdf['redu'].fillna((0), inplace=True)



# 利用分级方法展示孔子传播热度的空间分布
basemap = rasterio.open('D:\data/basemap/basemap911.tif')
fig,ax = plt.subplots(figsize=(12,10),subplot_kw={'aspect':'equal'})
rshow(basemap,ax=ax)
gdf.plot(column='redu', scheme='Quantiles', k=5, cmap='GnBu', legend=True, ax=ax)
plt.title('各国孔子传播热度分布图',fontname="SimHei")
plt.tight_layout()
plt.savefig('各国孔子传播热度分布图.png',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
plt.show()
plt.close()

# 绘制孔子搜索热度的空间滞后值分布图
#即：（每个国家的传播热度较其相邻国家的排名等级图）
df = gdf
wq =  lps.weights.Queen.from_dataframe(df)
wq.transform = 'r'
y = df['redu']
ylag = lps.weights.lag_spatial(wq, y)
#print(ylag)
import mapclassify as mc
ylagq5 = mc.Quantiles(ylag, k=5)
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=ylagq5.yb).plot(column='cl', categorical=True, \
        k=5, cmap='GnBu', linewidth=0.1, ax=ax, \
        edgecolor='white', legend=True)
ax.set_axis_off()
plt.title('各国孔子传播热度较其相邻国家排名图',fontname="SimHei")
plt.tight_layout()
plt.savefig('各国孔子传播热度较其相邻国家排名图.png',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
plt.show()
plt.close()


#同时绘制各国传播热度值图、领域排名值图进行对比
df['lag_redu'] = ylag
f,ax = plt.subplots(1,2,figsize=(2.16*4,4))
df.plot(column='redu', ax=ax[0], edgecolor='k',
        scheme="quantiles",  k=5, cmap='GnBu')
ax[0].axis(df.total_bounds[numpy.asarray([0,2,1,3])])
ax[0].set_title('各国孔子传播热度值图',fontname="SimHei")
df.plot(column='lag_redu', ax=ax[1], edgecolor='k',
        scheme='quantiles', cmap='GnBu', k=5)
ax[1].axis(df.total_bounds[numpy.asarray([0,2,1,3])])
ax[1].set_title('各国孔子传播热度较其相邻国家排名图',fontname="SimHei")
ax[0].axis('off')
ax[1].axis('off')
plt.tight_layout()
plt.savefig('传播热度分布图.png',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
plt.show()
plt.close()

# 绘制各国孔子传播热度的二值图（黑色为高热度地区、白色为低热度地区）
y.median()
print(y.median())
yb = y > y.median()
sum(yb)
print(sum(yb))
yb = y > y.median()
labels = ['0低于中位数','1高于中位数']
yb = [labels[i] for i in 1*yb] 
df['yb'] = yb
fig, ax = plt.subplots(figsize=(12,10), subplot_kw={'aspect':'equal'})
df.plot(column='yb', cmap='binary', edgecolor='grey', legend=True, ax=ax)
plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False
plt.title('传播热度二值图')
plt.tight_layout()
plt.savefig('传播热度二值图.png',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
plt.show()
plt.close()

#输出传播热度的p值（p<0.05）和莫兰指数值（值非0，正值正相关，负值负相关）
#用于判断全球的孔子文化传播热度是否具有全局自相关性
import esda 
yb = 1 * (y > y.median()) # convert back to binary
wq =  lps.weights.Queen.from_dataframe(df)
wq.transform = 'b'
numpy.random.seed(12345)
jc = esda.join_counts.Join_Counts(yb, wq)
#print(jc.bb," ",jc.ww," ",jc.bw," ",jc.bb + jc.ww + jc.bw," ",jc.mean_bb)
import seaborn as sbn
sbn.kdeplot(jc.sim_bb, shade=True)
plt.vlines(jc.bb, 0, 0.075, color='r')
plt.vlines(jc.mean_bb, 0,0.075)
plt.xlabel('连接计数',fontname="SimHei")
plt.ylabel('概率值',fontname="SimHei")
plt.Text(0.5, 0, '连接计数',fontname="SimHei")
plt.tight_layout()
plt.savefig('概率分布图.png',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
plt.show()
plt.close()
jc.p_sim_bb
print(jc.p_sim_bb)
wq.transform = 'r'
y = df['redu']
numpy.random.seed(12345)
mi = esda.moran.Moran(y, wq)
mi.I
print(mi.I)

#绘制多次随机空间分布的孔子文化传播热度的随机性期望值和实际值
#发现两者差距太大，因此判断其具有强空间自相关性
import seaborn as sbn
sbn.kdeplot(mi.sim, shade=True)
plt.vlines(mi.I, 0, 1, color='r')
plt.vlines(mi.EI, 0,1)
plt.xlabel('莫兰指数期望值与实际值对比',fontname="SimHei")
plt.ylabel('概率值',fontname="SimHei")
plt.Text(0.5, 0, '莫兰指数',fontname="SimHei")
plt.tight_layout()
plt.savefig('莫兰指数结果.png',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
plt.show()
plt.close()
mi.p_sim
print(mi.p_sim)


#局部自相关分析
#空间值，属性值在总体空间均值中的相对大小
#空间滞后值，属性值相对该属性对象的空间邻接对象的大小关系
#绘制莫兰散点图，横坐标为属性值，纵坐标为其滞后值
numpy.random.seed(12345)
import esda
wq.transform = 'r'
lag_redu_2020 = lps.weights.lag_spatial(wq, df['redu'])
redu_2020 = df['redu']
b, a = numpy.polyfit(redu_2020, lag_redu_2020, 1)
f, ax = plt.subplots(1, figsize=(12, 10))
plt.plot(redu_2020, lag_redu_2020, '.', color='firebrick')
plt.vlines(redu_2020.mean(), lag_redu_2020.min(), lag_redu_2020.max(), linestyle='--')
plt.hlines(lag_redu_2020.mean(), redu_2020.min(), redu_2020.max(), linestyle='--')
plt.plot(redu_2020, a + b*redu_2020, 'r')
plt.title('传播热度莫兰散点图',fontname="SimHei")
plt.ylabel('传播热度较空间滞后值',fontname="SimHei")
plt.xlabel('传播热度值',fontname="SimHei")
plt.tight_layout()
plt.savefig('传播热度莫兰散点图.png',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
plt.show()
plt.close()



#局部自相关分析结果展示
#冷热点图展示
li = esda.moran.Moran_Local(y, wq)
(li.p_sim < 0.05).sum()
sig = 1 * (li.p_sim < 0.05)
hotspot = 1 * (sig * li.q==1)
coldspot = 3 * (sig * li.q==3)
doughnut = 2 * (sig * li.q==2)
diamond = 4 * (sig * li.q==4)
spots = hotspot + coldspot + doughnut + diamond
spot_labels = [ '0 无关区域', '1 传播热点区域', '2 传播正常区域', '3 传播冷点区域', '4 传播异常区域']
labels = [spot_labels[i] for i in spots]
from matplotlib import colors
hmap = colors.ListedColormap([ 'lightgrey', 'red', 'lightblue', 'blue', 'pink'])
f, ax = plt.subplots(1, figsize=(12, 10))
df.assign(cl=labels,fontname="SimHei").plot(column='cl', categorical=True, \
        k=2, cmap=hmap, linewidth=0.1, ax=ax, \
        edgecolor='white', legend=True)
ax.set_axis_off()
plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False
plt.tight_layout()
plt.savefig('冷热点结果图.png',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
plt.show()
plt.close()
