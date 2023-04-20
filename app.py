import streamlit as st
import pandas as pd
import plotly_express as px

df = pd.read_csv('vehicles_us.csv')
#seperates manufacturer from overall model field
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])
#creates column of the year of the posting
df['year'] = pd.DatetimeIndex(df['date_posted']).year
#calculates the age of the vehicle at time of posting
df['age'] = df['year'] - df['model_year']

#creates text header above the dataframe
st.header('Data viewer')
#displays dataframe using streamlit
st.dataframe(df)

st.header ('Fuel Type by Year')

fuel_fig= px.histogram(df, x='fuel',
                      color = 'year',
                      color_discrete_sequence = ['navy', 'darkorange']
                      )
fuel_fig.show()
