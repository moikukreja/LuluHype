import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load synthetic dataset
@st.cache_data
def load_data():
    return pd.read_csv("lulu_synthetic_data.csv")

data = load_data()

st.set_page_config(page_title="Lulu UAE Sales Dashboard", layout="wide")
st.title("📊 Lulu UAE Sales Dashboard")

# Sidebar filters
st.sidebar.header("Filter Data")
location_filter = st.sidebar.multiselect("Select Location", options=data["Location"].unique(), default=data["Location"].unique())
gender_filter = st.sidebar.multiselect("Select Gender", options=data["Gender"].unique(), default=data["Gender"].unique())
category_filter = st.sidebar.multiselect("Select Category", options=data["Category"].unique(), default=data["Category"].unique())
loyalty_filter = st.sidebar.multiselect("Select Loyalty Status", options=data["Loyalty_Status"].unique(), default=data["Loyalty_Status"].unique())

# Apply filters
filtered_data = data[
    (data["Location"].isin(location_filter)) &
    (data["Gender"].isin(gender_filter)) &
    (data["Category"].isin(category_filter)) &
    (data["Loyalty_Status"].isin(loyalty_filter))
]

# KPIs
total_sales = filtered_data["Transaction_Amount"].sum()
avg_transaction = filtered_data["Transaction_Amount"].mean()
total_points = filtered_data["Points_Earned"].sum()

st.markdown("### Key Performance Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales (AED)", f"{total_sales:,.2f}")
col2.metric("Avg Transaction (AED)", f"{avg_transaction:,.2f}")
col3.metric("Total Loyalty Points", f"{total_points:,}")

# Charts
st.markdown("### Sales Breakdown")
fig1, ax1 = plt.subplots()
filtered_data.groupby("Category")["Transaction_Amount"].sum().plot(kind="bar", ax=ax1, color="skyblue")
ax1.set_ylabel("Sales (AED)")
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
filtered_data.groupby("Location")["Transaction_Amount"].sum().plot(kind="pie", autopct="%1.1f%%", ax=ax2)
ax2.set_ylabel("")
st.pyplot(fig2)

st.markdown("### Filtered Dataset Preview")
st.dataframe(filtered_data)
