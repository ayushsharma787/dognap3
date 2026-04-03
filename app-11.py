import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Premium Dog Analytics", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("dog_data.xlsx")

df = load_data()

st.sidebar.title("Filters")
age = st.sidebar.multiselect("Age Group", df["age_group"].unique(), default=df["age_group"].unique())
region = st.sidebar.multiselect("Region", df["region"].unique(), default=df["region"].unique())

df = df[(df["age_group"].isin(age)) & (df["region"].isin(region))]

st.title("🐶 Premium Dog Owner Analytics Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Users", len(df))
col2.metric("Avg Spend", f"₹{df['monthly_spend_inr'].mean():,.0f}")
col3.metric("Avg Dogs", round(df["num_dogs"].mean(), 2))
col4.metric("Adoption Rate", f"{(df['app_use_likelihood']=='Yes').mean()*100:.1f}%")

st.subheader("Spending Distribution")
fig1 = px.histogram(df, x="monthly_spend_inr", nbins=30)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Region vs Spend")
fig2 = px.bar(df.groupby("region")["monthly_spend_inr"].mean().reset_index(),
              x="region", y="monthly_spend_inr", color="monthly_spend_inr")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Adoption Intent")
fig3 = px.pie(df, names="app_use_likelihood")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Age vs Spend")
fig4 = px.box(df, x="age_group", y="monthly_spend_inr", color="age_group")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)
