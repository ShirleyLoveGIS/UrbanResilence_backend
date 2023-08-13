import pymysql
import pandas as pd

conn = pymysql.connect(
	user='root',
	password='rootuser123',
	port=3306,
	database='ugc_events',
	host='localhost',
)

#读取数据
df = pd.read_sql('select * from factor',con=conn)
#建立y_dataframe
y_df = pd.DataFrame(index=range(df.shape[0]) , columns=['Y'], dtype="float32")
#填入数据
for i in range(0, df.shape[0]):
    y_df.loc[i, ['Y']]= df.iat[i,list(df).index('Y')]   


