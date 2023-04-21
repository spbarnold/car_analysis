import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')
#seperates manufacturer from overall model field
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])
#creates column of the year of the posting
df['year'] = pd.DatetimeIndex(df['date_posted']).year
#calculates the age of the vehicle at time of posting
df['age'] = df['year'] - df['model_year']
#converting year to string for plotly-express
df['year'] = df['year'].apply(str)

#creates text header above the dataframe
st.header('Data viewer')
#displays dataframe using streamlit
st.dataframe(df)

st.header('Car Price by Age')
st.write(px.scatter (df, x='age', y='price', color='year', 
                      color_discrete_sequence = ['navy', 'darkorange'],
                    ))

st.write('Fuel Type of Cars Posted by Year')
st.write(px.histogram(df, x='fuel',
                      color = 'year',
                      color_discrete_sequence = ['navy', 'darkorange'],
                       ))

st.write('Compare Prices of Cars versus Fuel Type')
fuel_list = sorted(df['fuel'].unique())
fuel_1 = st.selectbox('Select Fuel 1',
                      fuel_list, index=fuel_list.index('gas'))

fuel_2 = st.selectbox('Select Fuel 2',
                      fuel_list, index=fuel_list.index('hybrid'))
mask_filter = (df['fuel'] == fuel_1) |(df['fuel'] == fuel_2)
df_filtered = df[mask_filter]

st.write(px.histogram(df_filtered,
                      x='price',
                      nbins=50,
                      color='fuel'
                      ))