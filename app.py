import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title=Sales Dashboard, layout=wide)

st.title(📊 Advanced Sales Analytics Dashboard)

# Load data
df = pd.read_csv(sales_data.csv)
df[Date] = pd.to_datetime(df[Date])

# Sidebar Filters
st.sidebar.header(Filters)

# Date range selector
min_date = df[Date].min()
max_date = df[Date].max()

date_range = st.sidebar.date_input(
    Select Date Range,
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Region filter
region = st.sidebar.multiselect(
    Select Region,
    options=df[Region].unique(),
    default=df[Region].unique()
)

# Category filter
category = st.sidebar.multiselect(
    Select Category,
    options=df[Category].unique(),
    default=df[Category].unique()
)

# Apply filters
filtered_df = df[
    (df[Date] = pd.to_datetime(date_range[0])) &
    (df[Date] = pd.to_datetime(date_range[1])) &
    (df[Region].isin(region)) &
    (df[Category].isin(category))
]

# KPI Section
total_sales = filtered_df[Sales].sum()
total_profit = filtered_df[Profit].sum()
total_orders = len(filtered_df)

col1, col2, col3 = st.columns(3)

col1.metric(💰 Total Sales, f₹{total_sales,.0f})
col2.metric(📈 Total Profit, f₹{total_profit,.0f})
col3.metric(🛒 Total Orders, total_orders)

st.divider()

# Sales Over Time (Interactive Line Chart)
st.subheader(📅 Sales Over Time)

sales_time = filtered_df.groupby(Date)[Sales].sum().reset_index()

fig_line = px.line(
    sales_time,
    x=Date,
    y=Sales,
    markers=True,
    title=Sales Trend
)

st.plotly_chart(fig_line, use_container_width=True)

# Sales by Category (Interactive Bar)
st.subheader(📦 Sales by Category)

category_sales = filtered_df.groupby(Category)[Sales].sum().reset_index()

fig_bar = px.bar(
    category_sales,
    x=Category,
    y=Sales,
    color=Category,
    title=Category-wise Sales
)

st.plotly_chart(fig_bar, use_container_width=True)

# Region Contribution (Interactive Pie)
st.subheader(🌍 Region Contribution)

region_sales = filtered_df.groupby(Region)[Sales].sum().reset_index()

fig_pie = px.pie(
    region_sales,
    names=Region,
    values=Sales,
    title=Sales by Region
)

st.plotly_chart(fig_pie, use_container_width=True)
