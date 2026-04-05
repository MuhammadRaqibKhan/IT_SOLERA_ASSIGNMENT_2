import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv('global_superstore.csv')

# Clean column names
df.columns = df.columns.str.strip().str.replace('.', '_')

# Sidebar filters
region_filter = st.sidebar.multiselect(
    'Select Region',
    df['Region'].unique(),
    default=df['Region'].unique()
)

category_filter = st.sidebar.multiselect(
    'Select Category',
    df['Category'].unique(),
    default=df['Category'].unique()
)

sub_category_filter = st.sidebar.multiselect(
    'Select Sub-Category',
    df['Sub_Category'].unique(),
    default=df['Sub_Category'].unique()
)

# Apply filters
filtered_df = df[
    (df['Region'].isin(region_filter)) &
    (df['Category'].isin(category_filter)) &
    (df['Sub_Category'].isin(sub_category_filter))
]

# KPIs
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()

top_customers = (
    filtered_df.groupby('Customer_Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

# Dashboard
st.title('Global Superstore Dashboard')

st.metric('Total Sales', f"${total_sales:,.2f}")
st.metric('Total Profit', f"${total_profit:,.2f}")

st.subheader('Top 5 Customers by Sales')
st.table(top_customers)

# Charts
st.subheader('Sales by Category')
category_sales = filtered_df.groupby('Category')['Sales'].sum()
st.bar_chart(category_sales)

st.subheader('Profit by Region')
region_profit = filtered_df.groupby('Region')['Profit'].sum()
st.bar_chart(region_profit)

# Plotly chart
fig = px.bar(
    filtered_df.groupby('Sub_Category')['Sales'].sum().reset_index(),
    x='Sub_Category',
    y='Sales',
    color='Sales',
    title='Sales by Sub-Category'
)

st.plotly_chart(fig)