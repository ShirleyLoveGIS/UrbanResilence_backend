import pymysql
import pandas as pd
from sqlalchemy import create_engine
from geodetector1 import (
    factor_detector, 
    interaction_detector, 
    ecological_detector
)
from classifymethod import (
    equal_interval, 
    quantile, 
    naturalbreaks
)
conn = pymysql.connect(
	user='root',
	password='rootuser123',
	port=3306,
	database='ugc_events',
	host='localhost',
)

def calriskvalue(front,method,n):
    #front=[{"id":"10001","factor name":"roaddensity","factor kind":"X","weight":"20"},{"id":"10002","factor name":"popudensity","factor kind":"X","weight":"20"},{"id":"10003","factor name":"clusterdegree","factor kind":"X","weight":"20"},{"id":"10004","factor name":"elevationmean","factor kind":"X","weight":"20"},{"id":"10005","factor name":"elevationstandard","factor kind":"X","weight":"20"},{"id":"10006","factor name":"soilmiscibility","factor kind":"X","weight":"0"},{"id":"10007","factor name":"maxiareapropo","factor kind":"X","weight":"0"}]
        
    #前台获得权重数组
    weight = []
    for i in range(0,len(front)):
        weight.append(int(front[i]['weight']))
    print(weight)
    #前台获得因子数组
    factor = []
    for j in range(0,len(front)):
        factor.append(front[j]['name'])
    print(weight)
    #获取城市名称数组
    city = []
    city_df = pd.read_sql('select city from factor group by city',con=conn)
    for i in city_df['city']:
        city.append(i)
    #城市个数
    length = len(city)
    #创建城市dataframe
    city_df = pd.DataFrame(index=range(length) , columns=['city','riskvalue'], dtype="float32")
    #计算各城市的q值
    for j in range(0,length):
        # 读取数据
        df = pd.read_sql('select * from `factor` where (`factor`.`city` = '+"'"+city[j]+"'"+')',con=conn)
        #因子探测器计算得到q值
        if(method == "equal_interval"):
            all_df = equal_interval(df , n , factor)
        elif(method == "quantile"):
            all_df = quantile(df , n , factor)
        elif(method == "naturalbreaks"):
            all_df = naturalbreaks(df , n , factor)
        result_df=factor_detector(all_df, 'Y', factor)
        #计算风险值
        risk_value = 0
        for i in range(0,len(front)):
            risk_value += result_df.iloc[0][i]*weight[i]*0.01
        city_df.loc[j, ['city']]= city[j]
        city_df.loc[j, ['riskvalue']]= risk_value 
        print(risk_value) 
    #将DataFrame数据插入表中
    engine = create_engine('mysql+mysqldb://root:rootuser123@localhost/ugc_events')
    city_df.to_sql('risk_value', engine, index=False, if_exists="replace")
    #增加主键

