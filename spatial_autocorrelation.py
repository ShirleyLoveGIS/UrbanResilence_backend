#相关库的引入
import esda
import os
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import libpysal as lps
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from pylab import*
import warnings
from scipy.stats import f #F检验
from scipy.stats import t #T检验
from scipy.stats import ncf #非中心F分布
from typing import Sequence
warnings.filterwarnings("ignore")# 忽略警告信息，使输出更清晰

def mainref(df, y: str, factors: Sequence, relationship=False):

#文件准备阶段
#读取geojson文件,可以由.shp文件转出,读取的文件命名为变量gdf:geogataframe
    gdf = gpd.read_file('D:\data\世界地图shp\globol.geo.json')
#从CSV文件读取数据，并创建GeoDataFrame
    bl_df = pd.read_csv('D:\data\世界地图shp\谷歌趋势右连接浮点数.csv')
#将CSV文件中的经纬度数据转换为Point对象，并设置为GeoDataFrame的geometry属性
    geometry = [Point(xy) for xy in zip(bl_df.Longitude, bl_df.Latitude)]
#将坐标系设置为EPS:G4326其实就是WGS84
    crs = {'init': 'epsg:4326'}
    bl_gdf = GeoDataFrame(bl_df, crs=crs, geometry=geometry)

# 数据处理阶段
# 将价格列的数据类型转换为float32
    bl_gdf['value_2020'] = bl_gdf['value_2020'].astype('float32')
# 执行空间连接操作，以内连接的方式合并相交的地理空间数据
    sj_gdf = gpd.sjoin(gdf, bl_gdf, how='inner', op='intersects', lsuffix='left', rsuffix='right')
# 计算每个区域内的多年均值
    median_value_2020_gb = sj_gdf['value_2020'].groupby([sj_gdf['国家']]).mean()
##median_value_2020_gb
# 输出需要分析属性的均值
    print('谷歌趋势值为：')
    print(median_value_2020_gb)

# 将计算得到的平均房价添加到原始GeoDataFrame中，并重命名该列为median_pri
    gdf = gdf.join(median_value_2020_gb, on='name_zh')
    gdf.rename(columns={'value_2020': 'median_pri'}, inplace=True)
# 输出带有平均房价的GeoDataFrame的前15行，以检查数据
    print(gdf.head(15))

# 处理缺失值
# 统计并输出median_pri列中缺失值的数量
    pd.isnull(gdf['median_pri']).sum()#统计缺失值个数即数据中存在NAN
    print("数据中存在以下行数的缺失值：")
    print(pd.isnull(gdf['median_pri']).sum())

# 使用整个数据集中median_pri列的平均值填充缺失值
    gdf['median_pri'].fillna((0), inplace=True)
# 可视化处理后的数据
# 使用GeoDataFrame的plot方法绘制median_pri列的地图表示
    gdf.plot(column='median_pri')
    plt.show()


# 进一步使用分类方案和颜色映射绘制地图，以展示不同区域的房价分布
    fig, ax = plt.subplots(figsize=(12,10), subplot_kw={'aspect':'equal'})
    gdf.plot(column='median_pri', scheme='Quantiles', k=5, cmap='GnBu', legend=True, ax=ax)
#ax.set_xlim(150000, 160000)
#ax.set_ylim(208000, 215000)
    plt.show()

# 空间自相关分析
# 使用Queen方法构建空间权重
    df = gdf
    wq =  lps.weights.Queen.from_dataframe(df)
# 将空间权重矩阵转换为行标准化形式
    wq.transform = 'r'

# 计算空间滞后
    y = df['median_pri']
    ylag = lps.weights.lag_spatial(wq, y)
    print(ylag)
    
    # 使用mapclassify库对空间滞后的结果进行分位数分类
    import mapclassify as mc
    ylagq5 = mc.Quantiles(ylag, k=5)
    
    # 绘制空间滞后结果的地图表示，使用分位数分类和颜色映射
    f, ax = plt.subplots(1, figsize=(9, 9))
    df.assign(cl=ylagq5.yb).plot(column='cl', categorical=True, \
            k=5, cmap='GnBu', linewidth=0.1, ax=ax, \
            edgecolor='white', legend=True)
    ax.set_axis_off()
    plt.title("Spatial Lag Median value_2020 (Quintiles)")
    plt.show()
    #plt.close()
    
    #绘制空间值和空间滞后值的对比图
    #空间值，属性值在总体空间均值中的相对大小
    #空间滞后值，属性值相对该属性对象的空间邻接对象的大小关系
    df['lag_median_pri'] = ylag
    f,ax = plt.subplots(1,2,figsize=(2.16*4,4))
    df.plot(column='median_pri', ax=ax[0], edgecolor='k',
            scheme="quantiles",  k=5, cmap='GnBu')
    ax[0].axis(df.total_bounds[np.asarray([0,2,1,3])])
    ax[0].set_title("value_2020")
    df.plot(column='lag_median_pri', ax=ax[1], edgecolor='k',
            scheme='quantiles', cmap='GnBu', k=5)
    ax[1].axis(df.total_bounds[np.asarray([0,2,1,3])])
    ax[1].set_title("Spatial Lag value_2020")
    ax[0].axis('off')
    ax[1].axis('off')
    plt.show()
    #plt.close()
    
    # 进行空间自相关分析，使用Moran's I指数，绘制二值图
    y.median()
    print(y.median())
    yb = y > y.median()
    sum(yb)
    print(sum(yb))
    yb = y > y.median()
    labels = ["0 Low", "1 High"]
    yb = [labels[i] for i in 1*yb] 
    df['yb'] = yb
    fig, ax = plt.subplots(figsize=(12,10), subplot_kw={'aspect':'equal'})
    df.plot(column='yb', cmap='binary', edgecolor='grey', legend=True, ax=ax)
    plt.show()
    plt.close()
    #观察不同对象的连接计数值，即看二值图区域间是否存在聚集情况，显著性检验的过程之一
    #观察相邻多边形间的连接关系
    import esda 
    yb = 1 * (y > y.median()) # convert back to binary
    wq =  lps.weights.Queen.from_dataframe(df)
    wq.transform = 'b'
    np.random.seed(12345)
    jc = esda.join_counts.Join_Counts(yb, wq)
    print(jc.bb," ",jc.ww," ",jc.bw," ",jc.bb + jc.ww + jc.bw," ",jc.mean_bb)
    
    #通过多次生成随机空间分布，999次获取连接数的实验均值，并与实际的连接数对比，可以看到非常大的偏移，从而判断该值在空间上具有聚集性，而非随机
    import seaborn as sbn
    sbn.kdeplot(jc.sim_bb, shade=True)
    plt.vlines(jc.bb, 0, 0.075, color='r')
    plt.vlines(jc.mean_bb, 0,0.075)
    plt.xlabel('BB Counts')
    plt.Text(0.5, 0, 'BB Counts')
    plt.show()
    plt.close()
    #输出伪p值，如果莫兰指数I绝对值趋于1而和P值小于0.05，则可以表明该属性数据具有强烈的空间自相关
    #在此简述一下p值的意义，首先通过中心极限定理多个独立同分布事件的均值的分布趋于正态分布，通过获取二值化后的连接数的数学期望
    #将其与实际的值列出，p就是数值大于等于实际值时的概率密度。
    jc.p_sim_bb#输出伪p值，因为是999次基本就是可以代表p值
    print(jc.p_sim_bb)
    #将权重从二进制状态转换成行标准状态
    wq.transform = 'r'#莫兰指数：负值表示空间负相关，表现为分散，正值为空间正相关，表现为聚集
    y = df['median_pri']
    np.random.seed(12345)#随机种子算法
    mi = esda.moran.Moran(y, wq)
    mi.I
    print(mi.I)#输出莫兰指数的值，用于对全局连续自相关性进行检验，
    
    #为了确保莫兰指数的指示性，将多次随机分布统计分析的莫兰指数概率分布图给出，其期望与实际
    #的莫兰指数值相差很大，这种情况下的p值也具有显著性检验的指示效果
    import seaborn as sbn
    sbn.kdeplot(mi.sim, shade=True)
    plt.vlines(mi.I, 0, 1, color='r')
    plt.vlines(mi.EI, 0,1)
    plt.xlabel("Moran's I")
    plt.Text(0.5, 0, "Moran's I")
    plt.show()
    mi.p_sim
    print(mi.p_sim)#莫兰指数p值
    
    
    #局部自相关分析，冷热点分析及空间异常值分析展示
    np.random.seed(12345)
    import esda
    wq.transform = 'r'
    lag_value_2020 = lps.weights.lag_spatial(wq, df['median_pri'])
    value_2020 = df['median_pri']
    b, a = np.polyfit(value_2020, lag_value_2020, 1)
    f, ax = plt.subplots(1, figsize=(9, 9))
    plt.plot(value_2020, lag_value_2020, '.', color='firebrick')
     # dashed vert at mean of the value_2020
    plt.vlines(value_2020.mean(), lag_value_2020.min(), lag_value_2020.max(), linestyle='--')
     # dashed horizontal at mean of lagged value_2020 
    plt.hlines(lag_value_2020.mean(), value_2020.min(), value_2020.max(), linestyle='--')
    # red line of best fit using global I as slope
    plt.plot(value_2020, a + b*value_2020, 'r')
    plt.title('Moran Scatterplot')
    plt.ylabel('Spatial Lag of value_2020')
    plt.xlabel('value_2020')
    plt.show()#绘制莫兰散点图，横坐标为属性值，纵坐标为其滞后值
    #空间值，属性值在总体空间均值中的相对大小
    #空间滞后值，属性值相对该属性对象的空间邻接对象的大小关系
    
    
    #计算局部莫兰指数
    li = esda.moran.Moran_Local(y, wq)
    li.q#将数据进行分级，按照数据一定标准（一般是标准差或者其他）作为分界线划分级别
    print(li.q)#打印分级数组
    (li.p_sim < 0.05).sum()#定义分级标准，将概率p值为0.05对应的属性值作为分级标准
    sig = li.p_sim < 0.05
    hotspot = sig * li.q==1#热点区域，表现为聚集
    coldspot = sig * li.q==3#冷点区域，表现为分散
    doughnut = sig * li.q==2#环形区域（甜甜圈区域），表现为环绕
    diamond = sig * li.q==4#钻石区域（异常区域），表现为异常
    spots = ['n.sig.', 'hot spot']
    labels = [spots[i] for i in hotspot*1]
    df = df
    from matplotlib import colors
    hmap = colors.ListedColormap(['red', 'lightgrey'])
    f, ax = plt.subplots(1, figsize=(9, 9))
    df.assign(cl=labels).plot(column='cl', categorical=True, \
            k=2, cmap=hmap, linewidth=0.1, ax=ax, \
            edgecolor='white', legend=True)
    ax.set_axis_off()
    plt.show()#刻画热点区域
    
    spots = ['n.sig.', 'cold spot']
    labels = [spots[i] for i in coldspot*1]
    df = df
    from matplotlib import colors
    hmap = colors.ListedColormap(['blue', 'lightgrey'])
    f, ax = plt.subplots(1, figsize=(9, 9))
    df.assign(cl=labels).plot(column='cl', categorical=True, \
            k=2, cmap=hmap, linewidth=0.1, ax=ax, \
            edgecolor='white', legend=True)
    ax.set_axis_off()
    plt.show()#刻画冷点区域
    
    spots = ['n.sig.', 'doughnut']
    labels = [spots[i] for i in doughnut*1]
    df = df
    from matplotlib import colors
    hmap = colors.ListedColormap(['lightblue', 'lightgrey'])
    f, ax = plt.subplots(1, figsize=(9, 9))
    df.assign(cl=labels).plot(column='cl', categorical=True, \
            k=2, cmap=hmap, linewidth=0.1, ax=ax, \
            edgecolor='white', legend=True)
    ax.set_axis_off()
    plt.show()#刻画环形区域，没有则表示为全色底图
    
    spots = ['n.sig.', 'diamond']
    labels = [spots[i] for i in diamond*1]
    df = df
    from matplotlib import colors
    hmap = colors.ListedColormap(['pink', 'lightgrey'])
    f, ax = plt.subplots(1, figsize=(9, 9))
    df.assign(cl=labels).plot(column='cl', categorical=True, \
            k=2, cmap=hmap, linewidth=0.1, ax=ax, \
            edgecolor='white', legend=True)
    ax.set_axis_off()
    plt.show()#刻画异常区域（钻石面）
    sig = 1 * (li.p_sim < 0.05)
    hotspot = 1 * (sig * li.q==1)
    coldspot = 3 * (sig * li.q==3)
    doughnut = 2 * (sig * li.q==2)
    diamond = 4 * (sig * li.q==4)
    spots = hotspot + coldspot + doughnut + diamond
    spots
    print(spots)#打印分级数组
    spot_labels = [ '0 ns', '1 hot spot', '2 doughnut', '3 cold spot', '4 diamond']
    labels = [spot_labels[i] for i in spots]
    
    from matplotlib import colors
    hmap = colors.ListedColormap([ 'lightgrey', 'red', 'lightblue', 'blue', 'pink'])
    f, ax = plt.subplots(1, figsize=(9, 9))
    df.assign(cl=labels).plot(column='cl', categorical=True, \
            k=2, cmap=hmap, linewidth=0.1, ax=ax, \
            edgecolor='white', legend=True)
    ax.set_axis_off()
    plt.show()#综合展示各类区域
    