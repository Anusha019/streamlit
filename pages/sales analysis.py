import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
from datetime import datetime
import time

st.title("Sales Analyzer")

df=pd.read_csv('Input_Sales_Data_v2.csv')
df['Date'] = pd.to_datetime(df['Date'])
min_date = df['Date'].min().to_pydatetime()
max_date = df['Date'].max().to_pydatetime()

col1, col2 = st.columns(2)
min,max=col1.slider('Select Date Range',min_value=min_date,max_value=max_date,value=(min_date,max_date))
a=col2.selectbox('Select Category',options=('Category_0','Category_1'))

res = df.loc[(df['Date']>=min)&(df['Date']<=max)&(df['Category']==a)]

df1=res.groupby('Manufacturer')[['Volume','Value']].sum().sort_values(by='Value',ascending=False).reset_index()

# Get the top 5 manufacturers for the selected period
top_manufacturers=df1['Manufacturer'].head(5).unique()

st.write('### Total sold Volume and price from selected date')

# Calculate market share based on value
total_value = df1['Value'].sum()
df1['Market Share'] = (df1['Value'] / total_value) * 100
df1.rename(columns={"Volume":"Total Sales Volume","Value":"Total Sales Value"}, inplace=True)
df1 = df1.style.format({
    'Total Sales Volume': '{:,.0f}',
    'Total Sales Value': '{:,.0f}',
    'Total Market Share': '{:.2f}%'
})

# cmap = sns.color_palette("crest_r", as_cmap=True)
background_gradient = df1.background_gradient(subset=['Market Share'], cmap='YlGnBu')

st.dataframe(df1, width=800)

# Group the data by manufacturer and date to calculate the total sales over time
sales = res.groupby(['Manufacturer', 'Date'], as_index=False)['Value'].sum()

st.subheader('Top 5 manufacturers')
plt.figure(figsize=(10, 6))
for i in top_manufacturers:
    manufacturer_data = sales[sales['Manufacturer'] == i]
    plt.plot(manufacturer_data['Date'], manufacturer_data['Value'],label=i)

plt.xlabel('Date')
plt.ylabel('Sales')
plt.title('Sales Trends for Top 5 Manufacturers')
st.pyplot(plt)

st.sidebar.image('logo.png')