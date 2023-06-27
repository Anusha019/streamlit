import streamlit as st
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import time

st.title("Sales Analyzer")

df=pd.read_csv('Input_Sales_Data_v2.csv')
df['Date'] = pd.to_datetime(df['Date'])
min_date = df['Date'].min().to_pydatetime()
max_date = df['Date'].max().to_pydatetime()

min,max=st.slider('Select Date Range',min_value=min_date,max_value=max_date,value=(min_date,max_date))

res = df.loc[(df['Date']>=min)&(df['Date']<=max)]
df1=res.groupby('Manufacturer')[['Volume','Value']].sum().reset_index()

st.write('### Total sold Volume and price from selected date')
st.dataframe(df1)

# Get the top 5 manufacturers for the selected period
top_manufacturers=df1.sort_values('Value').tail(5)['Manufacturer'].unique()

# Group the data by manufacturer and date to calculate the total sales over time
sales = res.groupby(['Manufacturer', 'Date'], as_index=False)['Value'].sum()

st.subheader('Top 5 manufacturers')
plt.figure(figsize=(10, 6))
for i in top_manufacturers:
    manufacturer_data = sales[sales['Manufacturer'] == i]
    st.markdown(i)
    st.line_chart(manufacturer_data,x='Date',y='Value')

st.sidebar.image('logo.png')