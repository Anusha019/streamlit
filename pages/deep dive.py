import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.title('DEEP DIVE')


df=pd.read_csv('Input_Sales_Data_v2.csv')

# Filter the dataframe  as per applied filters
col1, col2,col3 = st.columns(3)
cat=col1.selectbox('Select Category', df['Category'].unique())
man=col2.selectbox('Select Manufacturer', df['Manufacturer'].unique())
filtered_df = df[(df['Category'] == cat) & (df['Manufacturer'] == man)]
brand=col3.selectbox('Select Brand', filtered_df['Brand'].unique())

filtered_df=filtered_df[filtered_df['Brand'] == brand]

filtered_df=filtered_df.groupby(['Date','Manufacturer','Category','Brand','SKU Name'])['Volume','Value','Price'].sum().reset_index()

st.write('---')

# Calculate YTD volume sales, YTD $ sales, YTD Market share, and #SKUs
volume = filtered_df['Volume'].sum()
sales = filtered_df['Value'].sum()
market_share = sales / df['Value'].sum()
skus = filtered_df['SKU Name'].nunique()

col1, col2,col3,col4 = st.columns(4)
col1.metric('YTD Volume Sales',volume)
col2.metric('YTD $ Sales',f"${sales:,.2f}")
col3.metric('YTD Market Share',f"{market_share:.2%}")
col4.metric('# SKUs',skus)

st.write('---')

# Weekly sales plot and pie chart

filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
filtered_df.set_index('Date', inplace=True)

col1, col2 = st.columns(2)
with col1:
    df1 = filtered_df.resample('W').sum()
    fig,ax1 = plt.subplots(figsize=(10,6))
    ax1.plot(df1.index,df1['Value'], 'r')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Value')

    ax2 = ax1.twinx()
    ax2.plot(df1.index,df1['Volume'], 'm')
    ax2.set_ylabel('Volume Sales')
    plt.title('Weekly Volume Sales and Value Sales for Selected SKUs')
    plt.xticks(rotation=45)
    st.pyplot(fig)
with col2:
    top_10_sku_sales = filtered_df.groupby('SKU Name')['Value'].sum().nlargest(10)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(top_10_sku_sales, labels=top_10_sku_sales.index, autopct='%1.1f%%')
    plt.title('Percentage of Value Sales of Top 10 SKUs within the Brand')
    plt.xticks(rotation=45)
    st.pyplot(fig)



# Trend lines plots

col1, col2 = st.columns(2)
with col1:
    fig,ax1 = plt.subplots(figsize=(10,6))
    ax1.plot(filtered_df.index,filtered_df['Price'], 'c')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')

    ax2 = ax1.twinx()
    ax2.plot(filtered_df.index,filtered_df['Volume'], 'm')
    ax2.set_ylabel('Volume')
    plt.title('Trend lines of Price and volume')
    plt.xticks(rotation=45)
    st.pyplot(fig)
with col2:
    fig,ax1 = plt.subplots(figsize=(10,6))
    ax1.plot(filtered_df.index,filtered_df['Price'], 'c')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')

    ax2 = ax1.twinx()
    ax2.plot(filtered_df.index,filtered_df['Value'], 'r')
    ax2.set_ylabel('Value')
    plt.title('Trend lines of Price and Value')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Multiselect SKUs
selected_skus = st.multiselect('Select SKUs', filtered_df['SKU Name'].unique())

sku_df=filtered_df[filtered_df['SKU Name'].isin(selected_skus)]

col1, col2 = st.columns(2)
with col1:
    sku = sku_df.resample('W').sum()
    fig,ax1 = plt.subplots(figsize=(10,6))
    ax1.plot(sku.index,sku['Value'], 'r')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Value')

    ax2 = ax1.twinx()
    ax2.plot(sku.index,sku['Volume'],'m')
    ax2.set_ylabel('Volume')
    plt.title('Weekly Volume Sales and Value Sales for Selected SKUs')
    plt.xticks(rotation=45)
    st.pyplot(fig)
with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_sales_pm = sku_df.resample('M').mean()['Value']

    ax.bar(range(len(avg_sales_pm)), avg_sales_pm, color='blue')
    ax.set_xlabel('Month')
    ax.set_ylabel('Average $ Value Sales')
    plt.title('Average $ Value Sales per Month for Selected SKUs')
    st.pyplot(fig)


