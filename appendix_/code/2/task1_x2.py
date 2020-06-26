
# coding: utf-8

# In[61]:


import pandas as pd #导入pandas数据处理库
from sklearn.preprocessing import StandardScaler #导入标准差标准化函数
from sklearn.cluster import KMeans #导入聚类函数
from display import plot    # 导入自定义的绘图模块
from datetime import datetime
import matplotlib.pyplot as plt

#1.1数据探索：展示原始数据的尺寸
data1 = pd.read_csv('data1.csv', encoding='gb18030')  # 以指定格式读取数据
data2 = pd.read_csv('data2.csv', encoding='gb18030')  # 以指定格式读取数据
print('data1原始数据的尺寸为：',data1.shape) #显示原始数据的行数和列数
print('data2原始数据的尺寸为：',data2.shape) #显示原始数据的行数和列数


# In[11]:


exp1 = data2['Money'].notnull()
#exp2 = data[''].notnull()
data2_notnull = data2[exp1 ]
print('删除缺失记录后数据的尺寸为：',data2_notnull.shape)


# In[14]:


'''
处理异常值1.2.1： 清除消费金额为负数的消费记录
'''
index1 = data2['Money'] < 0
data3 = data2[-(index1)]
print('删除消费金额为负数常记录后数据的尺寸为：',data3.shape)


# In[15]:


print(data3.head())


# In[17]:


print(data3['Date'].dtype)


# In[20]:


data3['Date']=pd.to_datetime(data3['Date'])


# In[21]:


data3['hour']=data3['Date'].dt.hour
print(data3['hour'])
print(data3.columns)


# In[22]:


'''
处理异常值1.2.2： 清除消费时间为半夜（23:00——06:00）的消费记录
'''
data4=data3[(data3['hour']>=6) & (data3['hour']<23)]


# In[93]:


# print(data4)


# In[166]:


#df =data4.to_csv('task1_1.csv')
#print(df)


# In[23]:


data5 = pd.merge(data1,data4,how='outer',left_on='CardNo',right_on='CardNo')
data5


# In[171]:


#df2 =data5.to_csv('task1_1_1.csv')
#print(df2)


# In[24]:


print(data4.head(1))


# In[97]:


# 任务2.数据准备
# 1.增加一列"weekday",用以判断是否为工作日
data4['weekday'] = data4['Date'].apply(lambda x: x.weekday()+1) # 提取星期
data4


# In[29]:


# 任务2.1提取数据
# 2.1.1分组求和
data_gb = data4['CardCount'].groupby(data4['Dept']).sum()
print(data_gb)


# In[36]:


#2.1.2提取食堂的消费数据，可以用isin函数。
index=['第一食堂','第二食堂','第三食堂','第四食堂','第五食堂','教师食堂',]
data_st = data4.loc[data4['Dept'].isin(index)]
print(data_st.head(10))


# In[145]:


#2.1.3.分别提取早中晚各食堂就餐人数
#2..1.3.1提取早上7、8点的数据
data_morning = data_st.loc[(data4['hour'].apply(lambda x: x in [7, 8])),  :]
data_morning


# In[86]:


#2.1.3.2提取中午11.12.13点的数据
data_noon = data_st.loc[(data4['hour'].apply(lambda x: x in [11, 12, 13])),  :]
# data_noon 


# In[48]:


#2.1.3.3提取早上17,18,19点的数据
data_night = data_st.loc[(data4['hour'].apply(lambda x: x in [17,18,19])),  :]
# data_night


# In[90]:


# 2.2绘图
# 2.2.11早上食堂分组求和
st_gb_morning = data_morning['CardCount'].groupby(data_morning['Dept']).sum()
# st_gb_morning
# 2.2.12绘制食堂就餐饼图
plt.rcParams['font.sans-serif']='SimHei'   # 显示中文
plt.rcParams['axes.unicode_minus']=False  # 显示负号
fig=plt.figure(figsize=(6,6))
y = data_morning['CardCount'].groupby(data_morning['Dept']).sum()
x=y.index
plt.pie(y,labels=x,autopct='%.2f%%',)
plt.title('食堂早上就餐饼图')
plt.show()


# In[89]:


# 2.2.21中午食堂分组求和
st_gb_noon= data_noon['CardCount'].groupby(data_noon['Dept']).sum()
# st_gb_noon
# 2.2.22绘制食堂中午就餐饼图
plt.rcParams['font.sans-serif']='SimHei'   # 显示中文
plt.rcParams['axes.unicode_minus']=False  # 显示负号
fig=plt.figure(figsize=(6,6))
y = data_noon['CardCount'].groupby(data_noon['Dept']).sum()
x=y.index
plt.pie(y,labels=x,autopct='%.2f%%',)
plt.title('食堂中午就餐饼图')
plt.show()


# In[60]:


# 2.2.31晚上食堂分组求和
st_gb_night = data_night['CardCount'].groupby(data_night['Dept']).sum()
# st_gb_night


# In[92]:


# 2.2.32绘制食堂晚上就餐饼图
plt.rcParams['font.sans-serif']='SimHei'   # 显示中文
plt.rcParams['axes.unicode_minus']=False  # 显示负号
fig=plt.figure(figsize=(6,6))
y = data_night['CardCount'].groupby(data_night['Dept']).sum()
x=y.index
plt.pie(y,labels=x,autopct='%.2f%%',)
plt.title('食堂晚上就餐饼图')
plt.show()


# In[146]:


# 2.3绘制折线图
# 2.3.1区分工作日数据和非工作日数据
data_workday = data4.loc[(data4['weekday'].apply(lambda x: x in [6,7])),  :] #工作日数据
data_weekend = data4.loc[(data4['weekday'].apply(lambda x: x in [1,2,3,4,5])),  :] #非工作日数据
data_weekend.head(5)


# In[110]:


# 2.3.2分别区分每个小时的数据
workday_y=data4['CardCount'].groupby(data_workday['hour']).sum()
workday_y


# In[148]:


# 2.3.2绘图
# 2.3.2.1绘制食堂工作日就餐时间折线图

plt.rcParams['font.sans-serif']='SimHei'   # 显示中文
plt.rcParams['axes.unicode_minus']=False  # 显示负号
fig=plt.figure(figsize=(8,6))
plt.grid()
y = data4['CardCount'].groupby(data_workday['hour']).sum()
x=y.index
plt.title('食堂工作日就餐时间折线图')   
# 设置x轴的刻度
plt.xticks(range(0,24 )) # 最后一位取不到，所以要加1

plt.xlabel('就餐时间')   # 设置x轴标签
plt.ylabel('就餐人数')  # 设置y轴标签
plt.plot(x,y,c='b')
# plt.savefig('workday.jpg')
plt.show()


# In[147]:


# 2.3.2.2绘制食堂非工作日就餐时间折线图

plt.rcParams['font.sans-serif']='SimHei'   # 显示中文
plt.rcParams['axes.unicode_minus']=False  # 显示负号
fig=plt.figure(figsize=(8,6))
plt.grid()
y = data4['CardCount'].groupby(data_weekend['hour']).sum()
x=y.index
plt.title('食堂非工作日就餐时间折线图')
# 设置x轴的刻度
plt.xticks(range(0,24 )) # 最后一位取不到，所以要加1
plt.xlabel('就餐时间')   # 设置x轴标签
plt.ylabel('就餐人数')  # 设置y轴标签
plt.plot(x,y,c='c')
# plt.savefig('weekend.jpg')
plt.show()

