import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="Advanced Sales BI Dashboard",
    layout="wide"
)

# -------------------------------------------------------
# DARK PREMIUM STYLE
# -------------------------------------------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #0E1117;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Advanced Sales Business Intelligence Dashboard")

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------
df = pd.read_csv("sales_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# -------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------
st.sidebar.header("Filters")

min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

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

# -------------------------------------------------------
# APPLY FILTERS
# -------------------------------------------------------
filtered_df = df[
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1])) &
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

# -------------------------------------------------------
# KPI CALCULATIONS
# -------------------------------------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)

profit_margin = (total_profit / total_sales * 100) if total_sales != 0 else 0

# Month-over-Month Growth
filtered_df["Month"] = filtered_df["Date"].dt.to_period("M")
monthly_sales = filtered_df.groupby("Month")["Sales"].sum().reset_index()

if len(monthly_sales) > 1:
    last_month = monthly_sales.iloc[-1]["Sales"]
    prev_month = monthly_sales.iloc[-2]["Sales"]
    mom_growth = ((last_month - prev_month) / prev_month * 100) if prev_month != 0 else 0
else:
    mom_growth = 0

# Top Region
top_region = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

top_region_name = top_region.index[0] if not top_region.empty else "N/A"

# -------------------------------------------------------
# KPI DISPLAY
# -------------------------------------------------------
st.subheader("Key Business Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("MoM Growth", f"{mom_growth:.2f}%")
col3.metric("Profit Margin", f"{profit_margin:.2f}%")
col4.metric("Top Region", top_region_name)

st.divider()

# -------------------------------------------------------
# SALES TREND
# -------------------------------------------------------
st.subheader("Sales Trend Over Time")

sales_time = filtered_df.groupby("Date")["Sales"].sum().reset_index()

fig_line = px.line(
    sales_time,
    x="Date",
    y="Sales",
    markers=True,
    title="Sales Trend",
    template="plotly_dark"
)

st.plotly_chart(fig_line, use_container_width=True)

# -------------------------------------------------------
# CATEGORY PERFORMANCE
# -------------------------------------------------------
st.subheader("Category Performance")

category_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()

fig_bar = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category",
    title="Category-wise Sales",
    template="plotly_dark"
)

st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------------------------------------
# REGION CONTRIBUTION
# -------------------------------------------------------
st.subheader("Regional Contribution")

region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()

fig_pie = px.pie(
    region_sales,
    names="Region",
    values="Sales",
    title="Sales by Region",
    template="plotly_dark"
)
