import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("leads.csv")

st.title("📊 Lead Conversion Dashboard")

# Conversion rate
st.metric("Conversion Rate", f"{df['Converted'].mean()*100:.2f}%")

# Lead source chart
fig = px.histogram(df, x='Lead Source', color='Converted')
st.plotly_chart(fig)

# Funnel
total = len(df)
converted = df[df['Converted']==1].shape[0]

funnel = pd.DataFrame({
    'Stage': ['Total Leads', 'Converted'],
    'Count': [total, converted]
})

fig2 = px.funnel(funnel, x='Count', y='Stage')
st.plotly_chart(fig2)

# Sidebar filters
st.sidebar.header("Filter Data")

source = st.sidebar.selectbox("Select Lead Source", df['Lead Source'].dropna().unique())

filtered_df = df[df['Lead Source'] == source]

st.subheader(f"Data for {source}")

st.write(filtered_df.head())

fig = px.histogram(filtered_df, x='Lead Source', color='Converted')
st.plotly_chart(fig)

total_leads = len(filtered_df)
converted = filtered_df['Converted'].sum()
conversion_rate = (converted / total_leads) * 100

st.metric("Total Leads", total_leads)
st.metric("Converted Leads", converted)
st.metric("Conversion Rate", f"{conversion_rate:.2f}%")

import joblib

model = joblib.load("model.pkl")
model_columns = joblib.load("columns.pkl")

st.sidebar.header("Predict Lead Conversion")

time_spent = st.sidebar.slider("Time Spent on Website", 0, 5000, 100)
visits = st.sidebar.slider("Total Visits", 0, 50, 5)

input_data = [[time_spent, visits]]

if st.sidebar.button("Predict"):
    prediction = model.predict(input_data)
    
    if prediction[0] == 1:
        st.success("High chance of conversion ✅")
    else:
        st.error("Low chance of conversion ❌")

input_data = [[time_spent, visits]]

prediction = model.predict(input_data)