
# coding: utf-8

# In[120]:


import pandas as pd #导入pandas数据处理库
from sklearn.preprocessing import StandardScaler #导入标准差标准化函数
from sklearn.cluster import KMeans #导入聚类函数
from display import plot    # 导入自定义的绘图模块
from datetime import datetime


#1.1数据探索：展示原始数据的尺寸
data1 = pd.read_csv('data1.csv', encoding='gb18030')  # 以指定格式读取数据
data2 = pd.read_csv('data2.csv', encoding='gb18030')  # 以指定格式读取数据
print('data1原始数据的尺寸为：',data1.shape) #显示原始数据的行数和列数
print('data2原始数据的尺寸为：',data2.shape) #显示原始数据的行数和列数


# In[14]:


exp1 = data2['Money'].notnull()
#exp2 = data[''].notnull()
data2_notnull = data2[exp1 ]
print('删除缺失记录后数据的尺寸为：',data2_notnull.shape)


# In[130]:


'''
处理异常值1.2.1： 清除消费金额为负数的消费记录
'''
index1 = data2['Money'] < 0
data3 = data2[-(index1)]
print('删除消费金额为负数常记录后数据的尺寸为：',data3.shape)


# In[131]:


print(data3.head())


# In[138]:


print(data3['Date'].dtype)

#更改DATE的数据类型为时间时间类型
data3['Date']=pd.to_datetime(data3['Date'])
data3['hour']=data3['Date'].dt.hour
print(data3['hour'])
print(data3.columns)

#创建小时数作为特征
data3['hour']=data3['Date'].dt.hour
print(data3['hour'])
print(data3.columns)


# In[164]:


'''
处理异常值1.2.2： 清除消费时间为半夜（23:00——06:00）的消费记录
'''
data4=data3[(data3['hour']>=6) & (data3['hour']<23)]


# In[165]:


print(data4)


# In[166]:


df =data4.to_csv('task1_1.csv')
print(df)



# In[170]:


data5 = pd.merge(data1,data4,how='outer',left_on='CardNo',right_on='CardNo')
data5


# In[171]:


df2 =data5.to_csv('task1_1_1.csv')
print(df2)
