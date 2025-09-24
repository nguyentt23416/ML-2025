import pandas_read_xml as pdx
import pandas as pd
from bs4 import BeautifulSoup

#df=pd.read_csv("D:/Pycharm Projects/ML/Day 2/data/SalesTransactions.txt",encoding='utf-8', dtype='unicode',sep='/t',low_memory=False)
#df1=pd.read_csv("D:/Pycharm Projects/ML/Day 2/data/SalesTransactions.csv", encoding='utf-8',dtype='unicode',low_memory=False)
#df2=pd.read_json("D:/Pycharm Projects/ML/Day 2/data/SalesTransactions.json",encoding='utf-8',dtype='unicode')

#with open('D:/Pycharm Projects/ML/Day 2/data/SalesTransactions.xml','r') as f:
    #data=f.read()
#bs_data=BeautifulSoup(data,'xml')
#UelSample=bs_data.find_all('UelSample')
#print(UelSample)

#df=pdx.read_xml("D:/Pycharm Projects/ML/Day 2/data/SalesTransactions.xml",['UelSample','SalesItem'])
#print(df)
#print(df.iloc[0])
#data=df.iloc[0]

#print(data[0])
#print(data[1])
#print(data[1]["OrderID"])

dataframe=pd.read_excel("d:/Pycharm Projects/ML/Day 2/data/SalesTransactions.xlsx")
print(dataframe)