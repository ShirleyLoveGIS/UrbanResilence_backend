import pandas as pd
import numpy as np
from scipy.stats import f #F检验
from scipy.stats import t #T检验
from scipy.stats import ncf #非中心F分布
from typing import Sequence


#检查y及factors值是否规范
def check_data(df, y, factors):
    for factor in factors:
        if not factor in df.columns:
            raise ValueError('Factor [{}] is not in data')
    
    if y not in df.columns:
        raise ValueError('Factor [{}] is not in data')
        
    for factor in factors:
        if y==factor:
            raise ValueError("Y variable should not in Factor variables. ")
    
    has_null = df.isnull().values.any()
    if has_null:
        raise ValueError("data hava some objects with value NULL")


#计算ssw值
def cal_ssw(df: pd.DataFrame, y, factor, extra_factor=None):
    def _cal_ssw(df: pd.DataFrame, y):
        length = df.shape[0]#行数
        if length==1:
            strataVar = 0
            lamda_1st = np.square(df[y].values[0])#第0行0列数的平方
            lamda_2nd = df[y].values[0]#第0行0列的数
        else:
            ######
            strataVar = (length-1) * df[y].var(ddof=1)#（行数-1）*y的方差
            lamda_1st = np.square(df[y].values.mean())#y均值的平方
            lamda_2nd = np.sqrt(length) * df[y].values.mean()#根号行数*y均值
        return strataVar, lamda_1st, lamda_2nd
    if extra_factor==None:
        df2 = df[[y, factor]].groupby(factor).apply(_cal_ssw, y=y)#分组计算
    else:
        df2 = df[[y]+list(set([factor, extra_factor]))].groupby([factor, extra_factor]).apply(_cal_ssw, y=y)
    df2 = df2.apply(pd.Series)#一列拆成多列
    df2 = df2.sum()#总和
    strataVarSum, lamda_1st_sum, lamda_2nd_sum = df2.values
    return strataVarSum, lamda_1st_sum, lamda_2nd_sum


#计算q值
def cal_q(df, y, factor, extra_factor=None):
    strataVarSum, lamda_1st_sum, lamda_2nd_sum = cal_ssw(df, y, factor, extra_factor)
    #####
    TotalVar = (df.shape[0]-1)*df[y].var(ddof=1)#ddof=1 样本，ddof=0 总体
    q = 1 - strataVarSum/TotalVar
    return q, lamda_1st_sum, lamda_2nd_sum


#因子探测器
def factor_detector(df, y: str, factors: Sequence):
    check_data(df, y, factors=factors)

    out_df = pd.DataFrame(index=["q value", "p value"], columns=factors, dtype="float32")
    N_var = df[y].var(ddof=1)#方差
    N_popu = df.shape[0]#行数
    for factor in factors:
        N_stra = df[factor].unique().shape[0]
        q, lamda_1st_sum, lamda_2nd_sum = cal_q(df, y, factor)

        #lamda value
        lamda = (lamda_1st_sum - np.square(lamda_2nd_sum) / N_popu) / N_var
        #F value
        F_value = (N_popu - N_stra)* q / ((N_stra - 1)* (1 - q))
        #p value
        if lamda < 0.0001: 
            p_value = f.sf(F_value, N_popu-1, N_popu-N_stra)
        else:
            p_value = ncf.sf(F_value, N_stra-1, N_popu-N_stra, lamda)
        
        out_df.loc["q value", factor] = q
        out_df.loc["p value", factor] = p_value
        
    return out_df

#交互关系
def interaction_relationship(df):
    out_df = pd.DataFrame(index=df.index, columns=df.columns)
    length = len(df.index)
    for i in range(length):
        for j in range(i+1, length):
            factor1, factor2 = df.index[i], df.index[j]
            i_q = df.loc[factor2, factor1]
            q1 = df.loc[factor1, factor1]
            q2 = df.loc[factor2, factor2]

            if (i_q <= q1 and i_q <= q2):
                outputRls = "Weaken, nonlinear"
            elif (i_q < max(q1, q2) and i_q > min(q1, q2)):
                outputRls = "Weaken, uni-"
            elif (i_q == (q1 + q2)):
                outputRls = "Independent"
            elif (i_q > (q1 + q2)):
                outputRls = "Enhance, nonlinear"
            elif (i_q > max(q1, q2)):
                outputRls = "Enhance, bi-"

            out_df.loc[factor2, factor1] = outputRls
            out_df=out_df.replace(np.nan, '')
    return out_df


#交互探测器
def interaction_detector(df, y: str, factors: Sequence, relationship=False):
    check_data(df, y, factors=factors)

    out_df = pd.DataFrame(index=factors, columns=factors, dtype="float32")
    length = len(factors)

    for i in range(0, length):
        for j in range(0, i+1):
            q, _, _ = cal_q(df, y, factors[i], factors[j])
            out_df.loc[factors[i], factors[j]] = q

    if relationship:
        out_df2 = interaction_relationship(out_df)
        return out_df, out_df2
    return out_df

#生态探测器
def ecological_detector(df, y: str, factors: Sequence):
    check_data(df, y, factors=factors)

    out_df = pd.DataFrame(index=factors, columns=factors, dtype="float32")
    length = len(factors)

    for i in range(1, length):
        ssw1, _, _ = cal_ssw(df, y, factors[i])
        dfn = df[factors[i]].notna().sum()-1#非空处和减一
        for j in range(0, i):
            ssw2, _, _ = cal_ssw(df, y, factors[j])
            dfd = df[factors[j]].notna().sum()-1
            fval = (dfn*(dfd-1)*ssw1)/(dfd*(dfn-1)*ssw2)
            if fval<f.ppf(0.05, dfn, dfn):
                out_df.loc[factors[i], factors[j]] = 'Y'
            else:
                out_df.loc[factors[i], factors[j]] = 'N'
        out_df=out_df.replace(np.nan, '')
    return out_df

