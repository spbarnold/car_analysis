import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Analysis of Used Car Ads 2018-2019')

df = pd.read_csv('vehicles_us.csv')
#calculating the mean of the model year
med_mod_year = df['model_year'].median()
#calculating the mean of the odometer column
mean_odometer = df['odometer'].median()


#creates text header above the dataframe
st.header('Data viewer')
#replace null values in model_year
df['model_year'] = df['model_year'].fillna(med_mod_year)
#replacing all null values in 'cylinders'
df['cylinders'] = df['cylinders'].fillna(0)
#replacing null values with  unkown in paint_color
df['paint_color'] = df['paint_color'].fillna('Unkown')
#replacing all null values with 0
df['is_4wd'] = df['is_4wd'].fillna(0)
#replacing the null values of odometer with the mean value
df['odometer'] = df['odometer'].fillna(mean_odometer)
#converting float64 to int64 for all data expected to be treated as whole numbers
df['model_year'] = df['model_year'].apply(int)
df['days_listed'] = df['days_listed'].apply(int)
#converting date_posted to date time data type
df['date_posted'] = pd.to_datetime(df['date_posted'], format='%Y-%m-%d')
#creating column for car manufacturer
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])
#extracting year that the car was posted
df['year'] = pd.DatetimeIndex(df['date_posted']).year
#calculating the age of the car
df['age'] = df['year'] - df['model_year']
#converting year to string for plotly-express
df['year'] = df['year'].apply(str)
#displays dataframe using streamlit
st.dataframe(df)

st.header('Car Price by Age')
st.write(px.scatter (df, x='age', y='price', color='year', 
                      color_discrete_sequence = ['navy', 'darkorange'],
                      ))

normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
st.write('Fuel Type of Cars Posted by Year')
st.write(px.histogram(df, x='fuel',
                      color = 'year',
                      color_discrete_sequence = ['navy', 'darkorange'],  
                      histnorm=histnorm
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