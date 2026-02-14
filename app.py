import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Analytics Dashboard")

df = pd.read_csv("sales_data.csv")
df['Date'] = pd.to_datetime(df['Date'])

st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df.shape[0]

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"₹{total_sales}")
col2.metric("Total Profit", f"₹{total_profit}")
col3.metric("Total Orders", total_orders)

st.divider()

st.subheader("Sales by Category")
category_sales = filtered_df.groupby("Category")["Sales"].sum()

fig1, ax1 = plt.subplots()
category_sales.plot(kind="bar", ax=ax1)
st.pyplot(fig1)

st.subheader("Sales Over Time")
time_sales = filtered_df.groupby("Date")["Sales"].sum()

fig2, ax2 = plt.subplots()
time_sales.plot(ax=ax2)
st.pyplot(fig2)

st.subheader("Region Contribution")
region_sales = filtered_df.groupby("Region")["Sales"].sum()

fig3, ax3 = plt.subplots()
region_sales.plot(kind="pie", autopct='%1.1f%%', ax=ax3)
ax3.set_ylabel("")
st.pyplot(fig3)
