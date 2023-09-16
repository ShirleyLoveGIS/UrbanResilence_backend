import numpy as np
import math
import pandas as pd
from jenkspy import JenksNaturalBreaks
from database_connect import df,y_df
import pymysql

conn = pymysql.connect(
	user='root',
	password='rootuser123',
	port=3306,
	database='ugc_events',
	host='localhost',
)

#等间隔法分类
def equal_interval(df, n:int , factors):
    #行数
    ylength = df.shape[0]

    #读取数据
    factor_df = pd.read_sql('select * from factor',con=conn)
    #建立y_dataframe
    y_df1 = pd.DataFrame(index=range(ylength) , columns=['Y','name'], dtype="float32")
    #填入数据
    for i in range(0, df.shape[0]):
        y_df1.loc[i, ['Y']]= factor_df.iat[i,list(factor_df).index('Y')]   
        y_df1.loc[i, ['name']]= factor_df.iat[i,list(factor_df).index('name')]

    #建立dataframe
    out_df = pd.DataFrame(index=range(ylength), columns=factors, dtype="float32")
    #列数
    length = len(factors)

    for j in range(0, length):
        #取出值
        list1= []
        for value in df[factors[j]].to_list():
            list1.append(value)
        a = np.array(list1)
         
        #最大值
        maxi=max(a)
        #最小值
        mini=min(a)
        #间隔值
        nn=(maxi-mini) / n
        #mi-ma
        interval=[]
        for i in range(n):
            interval.append(mini+i*nn)
        interval.append(maxi)

        #改变值
        for i in range(0, ylength):
            for k in range(n):  
                if list1[i]>=interval[k] and list1[i]<interval[k+1]:
                    out_df.loc[i, factors[j]]= k+1
                    break
            if k==n-1:
                out_df.loc[i, factors[j]]= 5 
    #合并
    all_df = pd.concat([y_df1,out_df],axis = 1)  
    return all_df

#分位法处理数据
def quantile(df, n:int , factors):
    #行数
    ylength = df.shape[0]

    #读取数据
    factor_df = pd.read_sql('select * from factor',con=conn)
    #建立y_dataframe
    y_df1 = pd.DataFrame(index=range(ylength) , columns=['Y','name'], dtype="float32")
    #填入数据
    for i in range(0, df.shape[0]):
        y_df1.loc[i, ['Y']]= factor_df.iat[i,list(factor_df).index('Y')]   
        y_df1.loc[i, ['name']]= factor_df.iat[i,list(factor_df).index('name')]

    #建立dataframe
    out_df = pd.DataFrame(index=range(ylength), columns=factors, dtype="float32")
    #列数
    length = len(factors)

    for j in range(0, length):
        #取出值
        list1= []
        for value in df[factors[j]].to_list():
            list1.append(value)
        a = np.array(list1)
        #最大值
        maxi=max(a)
        #按数值排序
        a.sort()
        #mi-ma
        rs=[]
        interval=[]
        for i in range(n):
            one_list=a[math.floor(i / n * len(a)):math.floor((i + 1) / n * len(a))]
            rs.append(one_list)
            interval.append(rs[i][0])
        interval.append(maxi)
        for i in range(0, ylength):
            for k in range(n):  
                if list1[i]>=interval[k] and list1[i]<interval[k+1]:
                    out_df.loc[i, factors[j]]= k+1
                    break
            if k==n-1:
                out_df.loc[i, factors[j]]= 5 
    #合并
    all_df = pd.concat([y_df1,out_df],axis = 1)  
    return all_df

#自然法处理数据
def naturalbreaks(df, n:int , factors):
    #行数
    ylength = df.shape[0]

    #读取数据
    factor_df = pd.read_sql('select * from factor',con=conn)
    #建立y_dataframe
    y_df1 = pd.DataFrame(index=range(ylength) , columns=['Y','name'], dtype="float32")
    #填入数据
    for i in range(0, df.shape[0]):
        y_df1.loc[i, ['Y']]= factor_df.iat[i,list(factor_df).index('Y')]   
        y_df1.loc[i, ['name']]= factor_df.iat[i,list(factor_df).index('name')]

    #建立dataframe
    out_df = pd.DataFrame(index=range(ylength), columns=factors, dtype="float32")
    #列数
    length = len(factors)

    for j in range(0, length):
        #取出值
        list1= []
        for value in df[factors[j]].to_list():
            list1.append(value)
        a = np.array(list1)
        #分n类
        jnb = JenksNaturalBreaks(n)
        #根据a值进行分类
        jnb.fit(a)
        #按自然断点法分好的数组
        interval=jnb.breaks_
        #改变值
        for i in range(0, ylength):
            for k in range(n):  
                if list1[i]>=interval[k] and list1[i]<interval[k+1]:
                    out_df.loc[i, factors[j]]= k+1
                    break
            if k==n-1:
                out_df.loc[i, factors[j]]= 5 
    #合并
    all_df = pd.concat([y_df1,out_df],axis = 1)  
    return all_df 

